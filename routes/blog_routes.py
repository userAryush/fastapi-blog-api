from fastapi import APIRouter,Depends, HTTPException,status
from schemas import CreateBlog
from dependencies import get_db
from sqlalchemy.orm import Session
from models import Blog


router = APIRouter()

@router.post("/create_post", status_code=status.HTTP_201_CREATED)
def create_blog(blog: CreateBlog, db:Session=Depends(get_db)):
    new_blog = Blog(**blog.dict())
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return {"data":new_blog}

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

@router.put("/update_blog/{blog_id}",status_code=status.HTTP_202_ACCEPTED)
def update_blog(updated_blog: CreateBlog,blog_id:int, db:Session=Depends(get_db)):
    
    # db.query(Blog).filter(Blog.id == blog_id).update(updated_blog.dict())
    # db.commit()

    blog = db.query(Blog).filter(Blog.id == blog_id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Blog not found")
    for key, value in updated_blog.dict().items():
        setattr(blog, key, value)  # updates fields on the same object

    db.commit()
    db.refresh(blog)

    return {"details":f"{blog_id} updated successfully!!","data":blog}

@router.delete("/delete_blog/{blog_id}", status_code=status.HTTP_200_OK)
def delete_blog(blog_id:int,db:Session=Depends(get_db)):
    blog = db.query(Blog).filter(Blog.id == blog_id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Blog not found")
    db.delete(blog)
    db.commit()

    return {"details":f"{blog_id} deleted successfully!!"}