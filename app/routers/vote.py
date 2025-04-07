from http.client import FOUND
from fastapi import APIRouter, Depends, status, HTTPException, Response
from .. import schemas, database, models, oauth2
from sqlalchemy.orm import Session
from sqlalchemy import select


router = APIRouter(
    prefix="/vote",
    tags=['Vote']
)

@router.post("/",status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(database.get_db), 
         current_user: int = Depends(oauth2.get_current_user)):
    
    post = db.get(models.Post, vote.post_id)

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail = f"Post with id: {vote.post_id} does not exist")
    
    vote_query = db.execute(select(models.Vote).where(
        models.Vote.post_id == vote.post_id, 
        models.Vote.user_id == current_user.id))
    
    found_vote = vote_query.scalars().first()
    if (vote.dir == 1):
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
            detail=f"user {current_user.id} has already voted on post {vote.post_id}")
        new_vote = models.Vote(post_id = vote.post_id, user_id = current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "successfully added vote"}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                 detail="Vote does not exist")
        
        db.delete(found_vote)
        db.commit()
        return {"message": "successfully deleted vote"}
