from fastapi import APIRouter,Depends, HTTPException,status
from schemas import CreateComment, UpdateComment
from dependencies import get_db, get_current_user
from sqlalchemy.orm import Session
from models import Comments,Blog , Users
from sqlalchemy import and_

router = APIRouter()



@router.post("/create-comments/{blog_id}/", status_code=status.HTTP_201_CREATED)
def create_comment(blog_id: int, comment: CreateComment, db: Session = Depends(get_db), current_user: Users = Depends(get_current_user)):
    blog = db.query(Blog).filter(Blog.id == blog_id).first()

    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="This blog does not exist!")
    if blog_id != comment.blog_id or comment.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid blog request! ")
    
    new_comment = Comments(**comment.dict())
    new_comment.user_id = current_user.id
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment

@router.get("/see-all-comments/{blog_id}/", status_code= status.HTTP_200_OK)
def get_comments(blog_id: int, db: Session = Depends(get_db)):
    comments = db.query(Comments).filter(Comments.blog_id == blog_id).all()
    if not comments:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No comments found!")
    return comments

@router.get("/my-comments/{blog_id}/", status_code = status.HTTP_200_OK)
def get_comments_my_per_post(blog_id: int, db: Session = Depends(get_db), current_user: Users = Depends(get_current_user)):
    comments = db.query(Comments).filter(and_(Comments.blog_id == blog_id, Comments.user_id == current_user.id)).all()
    if not comments:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No comments found!")
    return comments

@router.put("/update-comment/{comment_id}/", status_code=status.HTTP_200_OK)
def update_comment(comment_id: int, comment: UpdateComment, db: Session = Depends(get_db), current_user: Users = Depends(get_current_user)):
    existing_comment = db.query(Comments).filter(and_(Comments.id == comment_id,Comments.user_id == current_user.id)).first()
    if not existing_comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")
    existing_comment.content = comment.content
    db.commit()
    db.refresh(existing_comment)
    return existing_comment

