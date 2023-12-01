# crud.py
from typing import List,Set,Dict
from datetime import datetime
from sqlalchemy.orm import Session
from . import models, schemas
from .schemas import GeneSetCreate
from uuid import uuid4
from .models import AnalysisRun,AnalysisResult,RunStatus
from .database import SessionLocal
from fastapi import APIRouter, Depends, HTTPException, Body, File,UploadFile,HTTPException,BackgroundTasks
from .models import BooleanAlgebraType
from .models import GeneSet as SQLAGeneSet
from sqlalchemy import func,Column, Integer, String, JSON  # Import JSON from sqlalchemy
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

# # db.query(models.GeneSet) creates a SQLAlchemy query object to query the GeneSet model.
# def get_genesets(db: Session, skip: int = 0, limit: int = 100):
#     return db.query(models.GeneSet).offset(skip).limit(limit).all()

#creates a new geneset in the database
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
    new_run = models.AnalysisRun()
    db.add(new_run)
    db.commit()
    db.refresh(new_run)
    return new_run

def extract_genes_from_json(json_data: str) -> Set[str]:
    # Convert JSON string to a Python object (list in this case)
    data = json.loads(json_data)
    # Extract the unigene list and convert it to a set
    return set(data['unigene'])

def get_geneset_unigenes(db: Session, gene_weaver_id: int) -> Set[str]:
    # Fetch the geneset by GeneWeaver ID and extract the unigenes
    geneset = db.query(SQLAGeneSet).filter(SQLAGeneSet.geneweaver_id == gene_weaver_id).first()
    if geneset and geneset.unigene:
        return extract_genes_from_json(geneset.unigene)
    else:
        raise HTTPException(status_code=404, detail=f"GeneSet with GeneWeaver ID {gene_weaver_id} not found or unigene data is empty")


def perform_boolean_algebra_analysis(task_id: int, db: Session, gene_weaver_ids: List[int], operation: str):
    # Convert GeneWeaver IDs to gene sets (sets of unigene values)
    update_run_status_and_time(db, task_id, RunStatus.RUNNING)
    
    try:
        geneset_sets = [get_geneset_unigenes(db, gene_weaver_id) for gene_weaver_id in gene_weaver_ids]
    
        if operation == "intersection":
            result = set.intersection(*geneset_sets)
        elif operation == "union":
            result = set.union(*geneset_sets)
        elif operation == "difference":
            result = set.symmetric_difference(*geneset_sets)
        else:
            raise ValueError(f"Unsupported operation: {operation}")

        # Save the result to the database
        save_analysis_result(db, task_id, list(result))
        update_run_status_and_time(db, task_id, RunStatus.COMPLETED, end_time=True)
        
    except Exception as e:
        # In case of error, set the status to FAILED
        update_run_status_and_time(db, task_id, RunStatus.FAILED, end_time=True)
        raise e
        
    
def get_run(db: Session, run_id: int):
    return db.query(models.AnalysisRun).filter(models.AnalysisRun.id == run_id).first()

def update_run_status_and_time(db: Session, run_id: int, status: str, start_time: bool = False, end_time: bool = False):
    """Update the status and time fields of an analysis run."""
    run = db.query(AnalysisRun).filter(AnalysisRun.id == run_id).first()
    if run:
        run.status = status
        if start_time:
            run.start_time = datetime.utcnow()  # Set start time to the current time
        if end_time:
            run.end_time = datetime.utcnow()  # Set end time to the current time
        db.commit()
        
def get_all_runs(db: Session):
    return db.query(models.AnalysisRun).all()


def cancel_run(db: Session, run_id: int):
    # Fetch the analysis run from the database
    run = db.query(AnalysisRun).filter(AnalysisRun.id == run_id).first()

    # Check if the run exists and is in a state that can be canceled
    if run and run.status in [RunStatus.PENDING, RunStatus.RUNNING]:
        # Update the status to 'canceled'
        run.status = RunStatus.CANCELED
        db.commit()
        return run
    elif run is None:
        # If the run does not exist, return None
        return None
    else:
        # If the run is in a state that cannot be canceled, raise an exception
        raise HTTPException(status_code=400, detail="Run cannot be canceled in its current state")


def save_analysis_result(db: Session, run_id: int, result_data: List[str]):
    # Convert the result data to a JSON string
    result_json = json.dumps({"result":result_data})

    # Create a new AnalysisResult instance
    new_result = AnalysisResult(run_id=run_id,result_data=result_json)

    # Add the new result to the database session
    db.add(new_result)

    # Update the run status and end_time
    run = db.query(AnalysisRun).filter(AnalysisRun.id == run_id).first()
    if run:
        run.status = RunStatus.COMPLETED
        run.end_time = func.now()
        db.commit()

def get_run_result(db: Session, run_id: int):
    return db.query(models.AnalysisResult).filter(models.AnalysisResult.run_id == run_id).first()