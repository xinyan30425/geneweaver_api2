# models.py

from sqlalchemy import Column, Integer, String, Enum, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from .database import Base
from pydantic import BaseModel, Field
import enum
from enum import Enum as PyEnum
from .enums import RunStatus


Base = declarative_base()

# Enum for run status
class RunStatus(enum.Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELED = "canceled"
    
# AnalysisRun model to track analysis runs
class AnalysisRun(Base):
    __tablename__ = "analysis_runs"
    
    id = Column(Integer, primary_key=True, index=True)
    status = Column(Enum(RunStatus), default=RunStatus.PENDING)
    result = Column(String)  # Store the result as a JSON string

    # Define relationships if needed
    # user_id = Column(Integer, ForeignKey("users.id"))
    # user = relationship("User", back_populates="analysis_runs")

# Modify GeneSet model as per your requirements  
class GeneSet(Base):
    __tablename__ = "genesets"
    
    id = Column(Integer, primary_key=True) 
    geneweaver_id = Column(Integer, unique=True, index=True)
    entrez = Column(String)
    ensembl_gene = Column(String)
    unigene = Column(String)

    

    # If you want to link to AnalysisRun
    # run_id = Column(Integer, ForeignKey("analysis_runs.id"))
    # run = relationship("AnalysisRun", back_populates="genesets")