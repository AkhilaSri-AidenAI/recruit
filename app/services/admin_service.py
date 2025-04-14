from sqlalchemy.orm import Session
from app.models.models import Candidate, Panelist
from app.schemas.schemas import AssignCandidate

def get_all_candidates(db: Session):
    return db.query(Candidate).all()

def get_all_panelists(db: Session):
    panelists = db.query(Panelist).all()
    result = []
    for p in panelists:
        assigned = len(p.candidates)
        result.append({
            "id": p.id,
            "name": p.name,
            "department": p.department,
            "assigned_count": assigned
        })
    return result

def assign_candidate_to_panelist(db: Session, data: AssignCandidate):
    candidate = db.query(Candidate).filter_by(id=data.candidate_id).first()
    if not candidate:
        return {"error": "Candidate not found"}
    candidate.panelist_id = data.panelist_id
    db.commit()
    db.refresh(candidate)
    return {"message": "Candidate assigned successfully"}
