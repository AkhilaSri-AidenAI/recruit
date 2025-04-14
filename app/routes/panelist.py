from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.schemas import PanelistUpdateStatus
from app.services import panelist_service
from app.database import get_db
from app.utils.auth import verify_password
from app.models.models import Panelist

router = APIRouter(prefix="/panelist", tags=["Panelist"])

@router.get("/candidates/{panelist_id}")
def get_assigned_candidates(panelist_id: int, db: Session = Depends(get_db)):
    return panelist_service.get_assigned_candidates(db, panelist_id)

@router.post("/update-status")
def update_candidate_status(data: PanelistUpdateStatus, db: Session = Depends(get_db)):
    return panelist_service.update_candidate_status(db, data)

@router.post("/login")
def panelist_login(username: str, password: str, db: Session = Depends(get_db)):
    panelist = db.query(Panelist).filter(Panelist.username == username).first()
    if not panelist or not verify_password(password, panelist.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"message": "Login successful"}
