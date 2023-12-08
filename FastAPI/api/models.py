# models.py
# Defines the data models for the application. 
# These are typically classes that SQLAlchemy uses to map objects to database tables. 
# Each class corresponds to a table in the database, and each attribute represents a column.

from sqlalchemy import Column, Integer, String, Enum, DateTime, JSON,ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class BooleanAlgebraType(Enum):
    INTERSECTION = "intersection"
    UNION = "union"
    DIFFERENCE = "difference"
 
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
    run_id = Column(Integer, ForeignKey('analysis_runs.id'))
    status = Column(Enum(RunStatus), default=RunStatus.PENDING)
    start_time = Column(DateTime(timezone=True), server_default=func.now())  # Auto-set at creation
    end_time = Column(DateTime(timezone=True))  # Set when analysis completes or fails
    result = relationship("AnalysisResult", back_populates="run", uselist=False)
    

class AnalysisResult(Base):
    __tablename__ = 'analysis_results'
    id = Column(Integer, primary_key=True, index=True)
    run_id = Column(Integer, ForeignKey('analysis_runs.id'))
    result_data = Column(JSON)  # Store result as JSON
    run = relationship("AnalysisRun", back_populates="result")