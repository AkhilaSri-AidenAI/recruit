from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.schemas import CandidateCreate, CandidateUpdate, AssignCandidate
from app.services import admin_service
from passlib.context import CryptContext
from app.database import get_db
from app.utils.auth import verify_password
from app.models.models import Admin

router = APIRouter(prefix="/admin", tags=["Admin"])
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.get("/candidates")
def get_all_candidates(db: Session = Depends(get_db)):
    return admin_service.get_all_candidates(db)

@router.post("/assign")
def assign_panelist(assign_data: AssignCandidate, db: Session = Depends(get_db)):
    return admin_service.assign_candidate_to_panelist(db, assign_data)

@router.get("/panelists")
def get_all_panelists(db: Session = Depends(get_db)):
    return admin_service.get_all_panelists(db)

@router.post("/login")
def admin_login(email: str, password: str, db: Session = Depends(get_db)):
    admin = db.query(Admin).filter(Admin.email == email).first()
    if not admin or not verify_password(password, admin.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"message": "Login successful"}

@router.post("/register-admin")
def register_admin(name: str, email: str, password: str, department: str, db: Session = Depends(get_db)):
    existing = db.query(Admin).filter(Admin.email == email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_pwd = pwd_context.hash(password)
    new_admin = Admin(
        name=name,
        email=email,
        department=department,
        password_hash=hashed_pwd
    )
    db.add(new_admin)
    db.commit()
    db.refresh(new_admin)
    return {"message": "Admin registered", "admin_id": new_admin.id}
