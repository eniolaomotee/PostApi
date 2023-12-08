from fastapi import Response, status, HTTPException, Depends, APIRouter
from .. import models, schemas, oauth2
from sqlalchemy.orm import Session
from ..database import get_db


router = APIRouter(
    prefix="/vote",
    tags=['Vote']
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote:schemas.Vote, db:Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    # Query for user trying to vote on a post that doesn't exist

    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {vote.post_id} does not exist")

    # Query if user has voted before
    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)

    found_vote = vote_query.first()
    
    if (vote.dir == 1):
        # User wants to like a post but he can't cause he has already liked it so we find the post and throw an exception
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"user {current_user.id} has already voted on post with {vote.post_id}")
        # But if we didn't find a vote(Meaning user hasn't liked it) then we'd create a new one
        new_vote = models.Vote(post_id = vote.post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message":"successfully added vote"}
    else:
        # If the user provides dir = 0 that means they want to delete a pre existing vote
        if not found_vote:
            # We can't delete a vote that doesn't exist reason we're raising an HTTPException.
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vote does not exist")
        # Then if we did find a vote then we want to delete it so we do the ff:
        vote_query.delete(synchronize_session=False)
        db.commit()

        return{"message":"Successfully deleted vote"}