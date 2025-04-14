from sqlalchemy.orm import Session
from app.schemas import CandidateCreate, CandidateUpdate, PanelistDecision, AssignCandidate
from ..models.models import Candidate
import logging
import traceback
from fastapi import HTTPException, status

# Get logger
logger = logging.getLogger(__name__)

def create_candidate(db: Session, data: CandidateCreate):
    try:
        logger.debug(f"Creating candidate with data: {data.dict()}")
        candidate = Candidate(**data.dict())
        db.add(candidate)
        db.commit()
        db.refresh(candidate)
        logger.info(f"Candidate created successfully with ID: {candidate.id}")
        return candidate
    except Exception as e:
        error_msg = f"Error creating candidate: {str(e)}\n{traceback.format_exc()}"
        print(f"ERROR: {error_msg}")  # Direct print to ensure visibility
        logger.error(error_msg)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create candidate: {str(e)}"
        )

def panelist_candidates(db: Session, panelist_id: int):
    try:
        logger.debug(f"Getting candidates for panelist {panelist_id}")
        candidates = db.query(Candidate).filter_by(panelist_id=panelist_id).all()
        logger.info(f"Found {len(candidates)} candidates for panelist {panelist_id}")
        return candidates
    except Exception as e:
        error_msg = f"Error retrieving candidates: {str(e)}\n{traceback.format_exc()}"
        print(f"ERROR: {error_msg}")  # Direct print to ensure visibility
        logger.error(error_msg)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve candidates: {str(e)}"
        )

def update_status(db: Session, data: PanelistDecision):
    try:
        logger.debug(f"Updating status for candidate {data.candidate_id}")
        candidate = db.query(Candidate).filter_by(id=data.candidate_id).first()
        if not candidate:
            logger.warning(f"Candidate not found: {data.candidate_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Candidate with ID {data.candidate_id} not found"
            )
        candidate.status = data.decision
        candidate.note = data.note
        db.commit()
        logger.info(f"Status updated for candidate {candidate.id} to {data.decision}")
        return candidate
    except HTTPException:
        raise
    except Exception as e:
        error_msg = f"Error updating status: {str(e)}\n{traceback.format_exc()}"
        print(f"ERROR: {error_msg}")  # Direct print to ensure visibility
        logger.error(error_msg)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update status: {str(e)}"
        )

def get_candidate_status(db: Session, candidate_id: int):
    try:
        logger.debug(f"Getting status for candidate {candidate_id}")
        candidate = db.query(Candidate).filter_by(id=candidate_id).first()
        if not candidate:
            logger.warning(f"Candidate not found: {candidate_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Candidate with ID {candidate_id} not found"
            )
        logger.info(f"Retrieved status for candidate {candidate_id}: {candidate.status}")
        return candidate
    except HTTPException:
        raise
    except Exception as e:
        error_msg = f"Error getting status: {str(e)}\n{traceback.format_exc()}"
        print(f"ERROR: {error_msg}")  # Direct print to ensure visibility
        logger.error(error_msg)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get status: {str(e)}"
        )

def assign_panelist(db: Session, data: AssignCandidate):
    try:
        logger.debug(f"Assigning panelist {data.panelist_id} to candidate {data.candidate_id}")
        candidate = db.query(Candidate).filter_by(id=data.candidate_id).first()
        if not candidate:
            logger.warning(f"Candidate not found: {data.candidate_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Candidate with ID {data.candidate_id} not found"
            )
        candidate.panelist_id = data.panelist_id
        db.commit()
        logger.info(f"Successfully assigned panelist {data.panelist_id} to candidate {data.candidate_id}")
        return candidate
    except HTTPException:
        raise
    except Exception as e:
        error_msg = f"Error assigning panelist: {str(e)}\n{traceback.format_exc()}"
        print(f"ERROR: {error_msg}")  # Direct print to ensure visibility
        logger.error(error_msg)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to assign panelist: {str(e)}"
        )

def update_candidate(db: Session, candidate_id: int, data: CandidateUpdate):
    try:
        logger.debug(f"Updating candidate {candidate_id} with data: {data.dict(exclude_unset=True)}")
        candidate = db.query(Candidate).filter_by(id=candidate_id).first()
        if not candidate:
            logger.warning(f"Candidate not found: {candidate_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Candidate with ID {candidate_id} not found"
            )
        for key, value in data.dict(exclude_unset=True).items():
            setattr(candidate, key, value)
        db.commit()
        logger.info(f"Successfully updated candidate {candidate_id}")
        return candidate
    except HTTPException:
        raise
    except Exception as e:
        error_msg = f"Error updating candidate: {str(e)}\n{traceback.format_exc()}"
        print(f"ERROR: {error_msg}")  # Direct print to ensure visibility
        logger.error(error_msg)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update candidate: {str(e)}"
        )
