from fastapi import APIRouter,Depends, HTTPException,status
from schemas import CreateBlog, CreateCategory
from dependencies import get_db, get_current_user
from sqlalchemy.orm import Session
from models import Blog,Users , Tags, PostLike, BlogCategory

router = APIRouter()

@router.post("/create-category/", status_code=status.HTTP_201_CREATED)
def create_category(category:CreateCategory,db:Session=Depends(get_db), current_user: Users=Depends(get_current_user)):
    category_existense = db.query(BlogCategory).filter(BlogCategory.name ==category.name).first()
    if category_existense:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Category with this name already exists!")
    new_category = BlogCategory(**category.dict())
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return {"msg": f"{category.name} created!"}
 
@router.get("/get-all-categories/", status_code=status.HTTP_200_OK)
def read_categories(db:Session=Depends(get_db)) :
    categories = db.query(BlogCategory).all()
    return {"data":categories}
   
@router.post("/create_post/", status_code=status.HTTP_201_CREATED)
def create_blog(blog: CreateBlog, db:Session=Depends(get_db), current_user: Users = Depends(get_current_user)):

    # Create blog without tag_ids
    new_blog = Blog(
        title=blog.title,
        content=blog.content,
        author_id=current_user.id,
        category_id=blog.category_id
    )
    
    # If tag_ids are given, fetch Tag objects
    if blog.tag_ids:
        tags = db.query(Tags).filter(Tags.id.in_(blog.tag_ids)).all()
        new_blog.tags = tags  # ✅ assign Tag instances, not IDs

    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    
    return {"data": new_blog}


@router.get("/read_blogs/", status_code=status.HTTP_200_OK)
def read_blogs(db:Session=Depends(get_db)):
    blogs = db.query(Blog).all()
    return {"data":blogs}

@router.get("/blog/{blog_id}/", status_code=status.HTTP_200_OK)
def read_blog(blog_id:int, db:Session=Depends(get_db)):
    blog = db.query(Blog).filter(Blog.id == blog_id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Blog not found")
    likes = len(blog.likes)
    return { "id": blog.id,
        "title": blog.title,
        "content": blog.content,
        "author": blog.author.username,
        "created_at": blog.created_at,
        "like_count": likes}

@router.put("/update_blog/{blog_id}/",status_code=status.HTTP_200_OK)
def update_blog(updated_blog: CreateBlog,blog_id:int, db:Session=Depends(get_db),current_user: Users = Depends(get_current_user)):
    
    # db.query(Blog).filter(Blog.id == blog_id).update(updated_blog.dict())
    # db.commit()

    blog = db.query(Blog).filter(Blog.id == blog_id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Blog not found")
    if blog.username != current_user.username:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You can only edit your own blog")
    for key, value in updated_blog.dict().items():
        setattr(blog, key, value)  # updates fields on the same object

    db.commit()
    db.refresh(blog)

    return {"details":f"{blog_id} updated successfully!!","data":blog}

@router.delete("/delete_blog/{blog_id}/", status_code=status.HTTP_200_OK)
def delete_blog(blog_id:int,db:Session=Depends(get_db),current_user: Users = Depends(get_current_user)):
    blog = db.query(Blog).filter(Blog.id == blog_id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Blog not found")
    if blog.author_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You can only delete your own blog")
    db.delete(blog)
    db.commit()

    return {"details":f"{blog_id} deleted successfully!!"}


##                        like unlike blog logic

@router.post("/like/{blog_id}/")
def like_blog(blog_id:int, db:Session=Depends(get_db),current_user: Users=Depends(get_current_user)):
    blog = db.query(Blog).filter(Blog.id == blog_id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Blog not found")
    
    existing_like = db.query(PostLike).filter(PostLike.post_id==blog_id, PostLike.user_id==current_user.id).first()
    if existing_like:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You have already liked this blog")
    like = PostLike(
        post_id=blog_id,
        user_id=current_user.id
    )
    db.add(like)
    db.commit()
    return {"details":f"{current_user.id} liked post {blog_id}!!"}

@router.delete("/like/{blog_id}/")
def dislike_blog(blog_id:int, db:Session=Depends(get_db),current_user: Users=Depends(get_current_user)):
    blog = db.query(Blog).filter(Blog.id == blog_id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Blog not found")
    
    existing_like = db.query(PostLike).filter(PostLike.post_id==blog_id, PostLike.user_id==current_user.id)
    if not existing_like:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You have not liked this blog")

    db.delete(existing_like)
    db.commit()
    return {"details":f"{current_user.id} disliked post {blog_id}!!"}

