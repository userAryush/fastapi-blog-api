from fastapi import APIRouter,Depends, HTTPException,status
from schemas import CreateBlog
from dependencies import get_db, get_current_user
from sqlalchemy.orm import Session
from models import Blog,Users , Tags

router = APIRouter()

@router.post("/create_post", status_code=status.HTTP_201_CREATED)
def create_blog(blog: CreateBlog, db:Session=Depends(get_db), current_user: Users = Depends(get_current_user)):

    # Create blog without tag_ids
    new_blog = Blog(
        title=blog.title,
        content=blog.content,
        author_id=current_user.id
    )
    
    # If tag_ids are given, fetch Tag objects
    if blog.tag_ids:
        tags = db.query(Tags).filter(Tags.id.in_(blog.tag_ids)).all()
        new_blog.tags = tags  # ✅ assign Tag instances, not IDs

    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    
    return {"data": new_blog}


@router.get("/read_blogs", status_code=status.HTTP_200_OK)
def read_blogs(db:Session=Depends(get_db)):
    blogs = db.query(Blog).all()
    return {"data":blogs}

@router.get("/blog/{blog_id}", status_code=status.HTTP_200_OK)
def read_blog(blog_id:int, db:Session=Depends(get_db)):
    blog = db.query(Blog).filter(Blog.id == blog_id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Blog not found")
    return {"data":blog}

@router.put("/update_blog/{blog_id}",status_code=status.HTTP_200_OK)
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

@router.delete("/delete_blog/{blog_id}", status_code=status.HTTP_200_OK)
def delete_blog(blog_id:int,db:Session=Depends(get_db),current_user: Users = Depends(get_current_user)):
    blog = db.query(Blog).filter(Blog.id == blog_id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Blog not found")
    if blog.username != current_user.username:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You can only delete your own blog")
    db.delete(blog)
    db.commit()

    return {"details":f"{blog_id} deleted successfully!!"}
