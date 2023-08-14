from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import schemas, database, models, oauth2


router = APIRouter(
    prefix="/vote",
    tags=['Vote']
)


@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(database.get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    candidate = db.query(models.Candidate).filter(models.Candidate.id == vote.candidate_id).first()

    if not candidate:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Candidate with id: {vote.candidate_id} does not exist")

    vote_query = db.query(models.Vote).filter(
        models.Vote.user_id == current_user.id)
    
    found_vote = vote_query.first()

    if vote.dir == 1:  # User wants to vote
        
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f"User {current_user.id} has already voted on Candidate {vote.candidate_id}")
        
        candidate.votes += 1  # Increment votes for the candidate
        new_vote = models.Vote(candidate_id=vote.candidate_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "Successfully cast vote"}
    else:  # User wants to remove vote

        if not found_vote:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=f"User {current_user.id} has not voted on Candidate {vote.candidate_id}")

        candidate.votes -= 1  # Decrement votes for the candidate
        vote_query.delete(synchronize_session=False)
        db.commit()

        return {"message": "Successfully deleted vote"}
