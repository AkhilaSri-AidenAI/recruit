from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List
from enum import Enum

class StatusEnum(str, Enum):
    processing = "Processing"
    accepted = "Accepted"
    rejected = "Rejected"
    on_hold = "On Hold"

class CandidateCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=100, example="John Doe")
    university: str = Field(..., min_length=3, max_length=100, example="University of XYZ")
    experience: int = Field(..., ge=0, le=30, example=5)  
    contact_info: str = Field(..., pattern=r"^\+?\d{10,15}$", example="+1234567890") 
    resume_url: str = Field(..., pattern=r"^https?://[^\s]+$", example="https://example.com/resume.pdf")
    additional_info: Optional[str] = Field(None, max_length=500, example="GitHub: https://github.com/johndoe")

class CandidateUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    university: Optional[str] = Field(None, min_length=3, max_length=100)
    experience: Optional[int] = Field(None, ge=0, le=30)
    contact_info: Optional[str] = Field(None, pattern=r"^\+?\d{10,15}$")
    resume_url: Optional[str] = Field(None, pattern=r"^https?://[^\s]+$")
    additional_info: Optional[str] = Field(None, max_length=500)
    status: Optional[StatusEnum] = None
    note: Optional[str] = Field(None, max_length=500)
    panelist_id: Optional[int] = None

    class Config:
        from_attributes = True

class CandidateOut(BaseModel):
    id: int
    name: str
    university: str
    experience: int
    contact_info: str
    resume_url: str
    additional_info: Optional[str]
    status: StatusEnum
    note: Optional[str] = None
    panelist_id: Optional[int] = None

    class Config:
        from_attributes = True  

class PanelistOut(BaseModel):
    id: int
    name: str
    department: str
    assigned_count: int

class AssignCandidate(BaseModel):
    candidate_id: int
    panelist_id: int

class PanelistDecision(BaseModel):
    candidate_id: int
    decision: StatusEnum
    note: Optional[str] = Field(None, max_length=500)

class AdminLogin(BaseModel):
    username: str = Field(..., min_length=3, max_length=50, example="admin")
    password: str = Field(..., min_length=8, example="strongpassword123")

class PanelistLogin(BaseModel):
    username: str = Field(..., min_length=3, max_length=50, example="panelist")
    password: str = Field(..., min_length=8, example="strongpassword123")

class PanelistUpdateStatus(BaseModel):
    candidate_id: int
    decision: StatusEnum
    note: Optional[str] = Field(None, max_length=500)
