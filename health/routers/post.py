from typing import List
from fastapi import APIRouter, Depends, status, HTTPException
from .. import schemas, database, models
from sqlalchemy.orm import Session

router = APIRouter()

# method from database.py
get_db = database.get_db


@router.get('/post', response_model=List[schemas.ShowPost], tags=['posts'])
def all_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts


@router.post('/post', status_code=status.HTTP_201_CREATED, tags=['posts'])
def create_post(request: schemas.Post, db: Session = Depends(get_db)):
    new_post = models.Post(title=request.title, body=request.body, user_id=1)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.delete('/post/{id}', status_code=status.HTTP_204_NO_CONTENT, tags=['posts'])
def destroy_post(id, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id)
    if not post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")
    post.delete(synchronize_session=False)  # flag
    db.commit()
    return 'done'


@router.put('/post/{id}', status_code=status.HTTP_202_ACCEPTED, tags=['posts'])
def update_post(id: int, request: schemas.Post, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id)
    if not post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")
    post.update(request.dict())  # flag
    db.commit()
    return 'updated'


@router.get('/post/{id}', response_model=schemas.ShowPost, tags=['posts'])  # don't use List for non List results
def post_by_id(id, db: Session = Depends(get_db)):
    posts = db.query(models.Post).filter(models.Post.id == id).first()
    if not posts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} is not available")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'detail': f"Post with id {id} is not available"}
    return posts