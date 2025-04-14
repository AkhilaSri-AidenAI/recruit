from sqlalchemy import Column, Integer, String, Enum, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.database import Base
import enum

class StatusEnum(str, enum.Enum):
    processing = "Processing"
    accepted = "Accepted"
    rejected = "Rejected"
    on_hold = "On Hold"

class Candidate(Base):
    __tablename__ = "candidates"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    university = Column(String)
    experience = Column(Integer)
    contact_info = Column(String)
    resume_url = Column(String)
    additional_info = Column(Text)
    status = Column(Enum(StatusEnum), default=StatusEnum.processing)
    panelist_id = Column(Integer, ForeignKey("panelists.id"), nullable=True)
    note = Column(Text, nullable=True)

class Panelist(Base):
    __tablename__ = "panelists"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    department = Column(String)
    candidates = relationship("Candidate", backref="panelist")
    username = Column(String, unique=True)
    password_hash = Column(String)

class Admin(Base):
    __tablename__ = "admins"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True, nullable=False) 
    department = Column(String)
    password_hash = Column(String)
