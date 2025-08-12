from fastapi import APIRouter,Depends, HTTPException,status
from schemas import CreateTag
from dependencies import get_db, get_current_user
from sqlalchemy.orm import Session
from models import Blog , Users,Tags
from sqlalchemy import and_

router = APIRouter()

@router.post("/create-tags/",status_code=status.HTTP_201_CREATED)
def create_tags(tag: CreateTag, db: Session= Depends(get_db),current_user: Users = Depends(get_current_user)):
    
    tag_existence = db.query(Tags).filter(Tags.name == tag.name).first()

    if tag_existence:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail=f"Tag {tag.name} already exists")
    new_tag = Tags(**tag.dict())
    db.add(new_tag)
    db.commit()
    db.refresh(new_tag)
    return {"data":new_tag, "message": "Tag created successfully"}

@router.get("/getall-tags/", status_code=status.HTTP_200_OK)
def read_all_tags(db: Session= Depends(get_db)):
    all_tags = db.query(Tags).all()
    return {"data": all_tags}

@router.delete("/del-tag/{tag_id}/", status_code=status.HTTP_200_OK)
def delete_tag(tag_id: int, db: Session= Depends(get_db)):
    tag = db.query(Tags).filter(Tags.id == tag_id).first()
    if not tag:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Tag with id {tag_id} doesnt exists!")
    db.delete(tag)
    db.commit()
    return {"message": f"Tag '{tag.name}' deleted successfully"}

    