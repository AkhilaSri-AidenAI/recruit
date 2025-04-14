from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import CandidateCreate, CandidateOut, CandidateUpdate
from app.services.core import create_candidate, get_candidate_status, update_candidate
import logging
import traceback

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/candidate", tags=["Candidate"])

@router.post("/submit", response_model=CandidateOut, status_code=status.HTTP_201_CREATED)
def submit_candidate(data: CandidateCreate, db: Session = Depends(get_db)):
    try:
        logger.info(f"Received candidate submission request: {data.dict()}")
        result = create_candidate(db, data)
        logger.info(f"Candidate submission successful: {result.id}")
        return result
    except Exception as e:
        error_msg = f"Error in submit_candidate: {str(e)}\n{traceback.format_exc()}"
        logger.error(error_msg)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create candidate: {str(e)}"
        )

@router.get("/{candidate_id}/status", response_model=CandidateOut)
def status_check(candidate_id: int, db: Session = Depends(get_db)):
    try:
        logger.info(f"Checking status for candidate ID: {candidate_id}")
        result = get_candidate_status(db, candidate_id)
        if not result:
            logger.warning(f"Candidate not found: {candidate_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Candidate with ID {candidate_id} not found"
            )
        logger.info(f"Status check successful for candidate {candidate_id}")
        return result
    except HTTPException:
        raise
    except Exception as e:
        error_msg = f"Error in status_check: {str(e)}\n{traceback.format_exc()}"
        logger.error(error_msg)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get candidate status: {str(e)}"
        )

@router.put("/{candidate_id}", response_model=CandidateOut)
def update_candidate_info(candidate_id: int, data: CandidateUpdate, db: Session = Depends(get_db)):
    try:
        logger.info(f"Updating candidate {candidate_id} with data: {data.dict(exclude_unset=True)}")
        result = update_candidate(db, candidate_id, data)
        if not result:
            logger.warning(f"Candidate not found for update: {candidate_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Candidate with ID {candidate_id} not found"
            )
        logger.info(f"Update successful for candidate {candidate_id}")
        return result
    except HTTPException:
        raise
    except Exception as e:
        error_msg = f"Error in update_candidate_info: {str(e)}\n{traceback.format_exc()}"
        logger.error(error_msg)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update candidate: {str(e)}"
        )
