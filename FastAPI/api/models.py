# models.py

from sqlalchemy import Column, Integer, String, Enum, JSON,ForeignKey
from sqlalchemy.orm import relationship
from pydantic import BaseModel, Field
import enum
from enum import Enum as PyEnum
from .enums import RunStatus
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# Modify GeneSet model as per your requirements  
class GeneSet(Base):
    __tablename__ = "genesets"
    
    id = Column(Integer, primary_key=True) 
    geneweaver_id = Column(Integer, unique=True, index=True)
    entrez = Column(String)
    ensembl_gene = Column(String)
    unigene = Column(String)

# Enum for run status
class RunStatus(enum.Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELED = "canceled"

class AnalysisRun(Base):
    __tablename__ = 'analysis_runs'
    id = Column(Integer, primary_key=True, index=True)
    status = Column(String, default='pending')  # e.g., 'pending', 'running', 'completed', 'failed', 'canceled'
    result = relationship("AnalysisResult", back_populates="run", uselist=False)

class AnalysisResult(Base):
    __tablename__ = 'analysis_results'
    id = Column(Integer, primary_key=True, index=True)
    run_id = Column(Integer, ForeignKey('analysis_runs.id'))
    result_data = Column(JSON)  # Store result as JSON
    run = relationship("AnalysisRun", back_populates="result")