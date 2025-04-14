from sqlalchemy.orm import Session
from app import schemas, models

def panelist_candidates(db: Session, panelist_id: int):
    return db.query(models.Candidate).filter_by(panelist_id=panelist_id).all()

def update_status(db: Session, data: schemas.PanelistDecision):
    candidate = db.query(models.Candidate).filter_by(id=data.candidate_id).first()
    candidate.status = data.decision
    candidate.note = data.note
    db.commit()

def login(db: Session, email: str, password: str):
    panelist = db.query(models.Panelist).filter_by(email=email).first()
    if not panelist or not panelist.verify_password(password):
        return None
    return panelist