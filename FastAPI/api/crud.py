# crud.py
from typing import List,Set,Dict
from . import schemas
from sqlalchemy.orm import Session
from . import models
from .schemas import GeneSetCreate, GeneSet
from uuid import uuid4
from .models import AnalysisRun
from .database import SessionLocal
from .models import AnalysisRun
from sqlalchemy import Column, Integer, String, JSON  # Import JSON from sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
import json


import sys 
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent / "FastAPI"))
from geneweaver_boolean_algebra.src.tool import BooleanAlgebra
from geneweaver_boolean_algebra.src.schema import BooleanAlgebraInput

# retrieves a single geneset by its geneset_id from the database
def get_geneset(db: Session, geneset_id: int):
    return db.query(models.GeneSet).filter(models.GeneSet.geneweaver_id == geneset_id).first() 
# db.query(models.GeneSet) creates a SQLAlchemy query object to query the GeneSet model.
#.filter(models.GeneSet.id == geneset_id) filters the query to only include the geneset with the matching ID.
#.first() returns the first result of the query or None if no result is found.

# db.query(models.GeneSet) creates a SQLAlchemy query object to query the GeneSet model.
def get_genesets(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.GeneSet).offset(skip).limit(limit).all()

#creates a new geneset in the database
# def create_geneset(db: Session, geneset: schemas.GeneSetCreate):
#     db_geneset = models.GeneSet(**geneset.dict()) #creates a dictionary of the new data, excluding any fields that were not set 
#     db.add(db_geneset)
#     db.commit()
#     db.refresh(db_geneset)
#     return db_geneset

def create_geneset(db: Session, geneset: GeneSetCreate):
    try:
        unigene_json = json.dumps({"unigene":geneset.unigene})
        db_geneset = models.GeneSet(
            geneweaver_id=geneset.geneweaver_id,
            entrez=geneset.entrez,
            ensembl_gene=geneset.ensembl_gene,
            unigene=unigene_json,
        )
        print(f"Unigene JSON: {unigene_json}")
        db.add(db_geneset)
        db.commit()
        db.refresh(db_geneset)
        return db_geneset
    except Exception as e:
        db.rollback()
        raise e

def get_geneset(db: Session, geneset_id: int):
    db_geneset = db.query(models.GeneSet).filter(models.GeneSet.geneweaver_id == geneset_id).first()
    if db_geneset:
        # Convert JSON string back to a list
        db_geneset.unigene = json.loads(db_geneset.unigene)
    return db_geneset


# updates an existing geneset identified by geneset_id with the data in geneset (an instance of GeneSetUpdate).
def update_geneset(db: Session, geneset_id: int, geneset: schemas.GeneSetUpdate):
    db_geneset = get_geneset(db, geneset_id)
    if db_geneset:
        update_data = geneset.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_geneset, key, value)

        db.commit()
        db.refresh(db_geneset)
    return db_geneset

# Deletes the geneset with the given geneset_id from the database.
def delete_geneset(db: Session, geneset_id: int):
    db_geneset = get_geneset(db, geneset_id)
    if db_geneset:
        db.delete(db_geneset)
        db.commit()
        return db_geneset


# performs a boolean algebra operation specified by operation on a list of genesets identified by geneset_ids.
def perform_boolean_algebra(db: Session, operation: str, geneset_ids: List[int]) -> Set[str]:
    # Fetch gene sets from the database
    gene_sets = [get_geneset(db,geneset_id) for geneset_id in geneset_ids]
    
    # Prepare input for the Boolean Algebra tool
    tool_input = BooleanAlgebraInput(
        type=BooleanAlgebraType[operation.upper()],
        input_genesets=[geneset.genes for geneset in gene_sets]
    )
    
    # Instantiate the tool and run the operation
    boolean_algebra_tool = BooleanAlgebra()
    result = boolean_algebra_tool.run(tool_input)
    
    return result.result_geneset_ids


# CRUD functions for analysis runs
def create_analysis_run(db: Session):
    new_run = AnalysisRun(status=RunStatus.PENDING)
    db.add(new_run)
    db.commit()
    db.refresh(new_run)
    return new_run

def get_all_runs(db: Session):
    return db.query(AnalysisRun).all()

def get_run(db: Session, run_id: int):
    return db.query(AnalysisRun).filter(AnalysisRun.id == run_id).first()

def cancel_run(db: Session, run_id: int):
    run = get_run(db, run_id)
    if run and run.status == RunStatus.RUNNING:
        run.status = RunStatus.CANCELED
        db.commit()
    return run
