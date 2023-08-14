from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List, Optional

from sqlalchemy import func
# from sqlalchemy.sql.functions import func
from .. import models, schemas, oauth2
from ..database import get_db


router = APIRouter(
    prefix="/candidates",
    tags=['Candidates']
)


@router.get("/", response_model=List[schemas.Candidate])
def get_candidates(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 10):

    # change candidates display?
    candidates = db.query(models.Candidate).order_by(models.Candidate.votes.desc()).limit(limit).all()
    return candidates


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Candidate)
def create_candidate(candidate: schemas.CandidateCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    # Add party affiliation
    new_candidate = models.Candidate(owner_id=current_user.id, **candidate.model_dump())
    db.add(new_candidate)
    db.commit()
    db.refresh(new_candidate)

    return new_candidate 


@router.get("/{id}", response_model=schemas.Candidate)
def get_candidate(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    # Query and retrieve the candidate object and vote count tuple
    candidate = db.query(models.Candidate).filter(models.Candidate.id == id).first()

    if not candidate:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"candidate with id: {id} was not found")
    
    # Print the candidate object to verify its structure
    print(f'candidate: {candidate}')
    
    return candidate


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_candidate(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    candidate_query = db.query(models.Candidate).filter(models.Candidate.id == id)

    candidate = candidate_query.first()

    if candidate == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"candidate with id: {id} does not exist")

    if candidate.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")

    candidate_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.Candidate)
def update_candidate(id: int, updated_post: schemas.CandidateCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    candidate_query = db.query(models.Candidate).filter(models.Candidate.id == id)

    candidate = candidate_query.first()

    if candidate == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"candidate with id: {id} does not exist")

    if candidate.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")

    candidate_query.update(updated_post.model_dump(), synchronize_session=False)
    db.commit()

    return candidate_query.first()
