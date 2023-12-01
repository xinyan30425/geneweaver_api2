#endpoint.py

from typing import List,Set
from fastapi import APIRouter, Depends, HTTPException, Body, File,UploadFile,HTTPException,BackgroundTasks
from sqlalchemy.orm import Session,joinedload
import json
# Importing CRUD operations and schema models from the local modules.
from .crud import get_geneset, create_geneset, update_geneset, delete_geneset,get_run_result,get_run,get_all_runs,create_analysis_run,perform_boolean_algebra_analysis
from .crud import cancel_run as crud_cancel_run
from .schemas import GeneSetCreate, GeneSetUpdate, GeneSet,BooleanAlgebraRequest,GeneSetFileRow,AnalysisRunSchema,AnalysisResultSchema
from .database import get_db 
import csv
import io
from .database import SessionLocal,get_db
from pydantic import ValidationError
from .models import GeneSet as SQLAGeneSet
from .crud import update_run_status_and_time,get_geneset_unigenes,perform_boolean_algebra_analysis
from .models import AnalysisRun,RunStatus



# Adding the path to sys.path allows Python to find modules in a different directory.
import sys 
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent / "FastAPI"))
# Importing the BooleanAlgebra tool and input schema for boolean algebra operations.
from geneweaver_boolean_algebra.src.tool import BooleanAlgebra,BooleanAlgebraType
from geneweaver_boolean_algebra.src.schema import BooleanAlgebraInput,BooleanAlgebraOutput
from geneweaver_boolean_algebra.src.utils import iterable_to_sets
from geneweaver_boolean_algebra.src.union import union
from geneweaver_boolean_algebra.src.intersection import intersection
from geneweaver_boolean_algebra.src.symmetric_difference import symmetric_difference


# Creating an API router which will contain all the endpoint definitions.
router = APIRouter()

# Defining an endpoint for uploading genesets through a file.
@router.post("/upload-genesets/", status_code=201)
async def upload_genesets(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if not file.filename.endswith('.txt'):
        raise HTTPException(status_code=400, detail="Invalid file format. Only .txt files are accepted.")
    
    content = await file.read()
    content_str = content.decode("utf-8")
    reader = csv.DictReader(io.StringIO(content_str), delimiter='\t')

    for row in reader:
        try:
            # Assuming 'Entrez' field is an integer and present in every row
            entrez_value = int(row.get('Entrez', '')) if row.get('Entrez', '') else None
            # Parse the 'Unigene' field and convert it to a list
            unigene_list = row.get('Unigene', '').split('|') if row.get('Unigene') else []
            # Split 'Gene Symbol' by pipe character if it exists and is not empty
            # gene_symbol_list = []
            # gene_symbol_str = row.get('Gene Symbol', '')
            # if gene_symbol_str:
            #     if isinstance(gene_symbol_str, list):
            #         # Join the list into a single string
            #         gene_symbol_str = ''.join(gene_symbol_str)
            #     gene_symbol_list.extend(gene_symbol_str.split('|'))
            #     gene_symbol_list.extend(gene_symbol_str.split('-'))   
            # You may need to adjust the following fields to match the columns of your file exactly.
            geneset_create = GeneSetCreate(
                geneweaver_id=int(row.get('GeneWeaver ID', 0)),
                entrez=entrez_value,
                ensembl_gene=row.get('Ensembl Gene', ''),
                ensembl_protein=row.get('Ensembl Protein', ''),
                ensembl_transcript=row.get('Ensembl Transcript', ''),
                unigene=unigene_list
            )
            create_geneset(db, geneset_create)

        except ValidationError as e:
            # Handle the validation error
            print(f"Validation error for row: {row}, Error: {e}")

    return {"status": "success", "filename": file.filename}

# Defining an endpoint to create a new geneset.
@router.post("/genesets/", response_model=GeneSet)
def create_geneset_endpoint(geneset: GeneSetCreate, db: Session = Depends(get_db)):
    return create_geneset(db, geneset)

# Defining an endpoint to read all genesets with pagination.
@router.get("/genesets/", response_model=List[GeneSet])
def read_genesets(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    genesets = get_genesets(db, skip=skip, limit=limit)
    return genesets

# Defining an endpoint to read a specific geneset by its ID.
@router.get("/genesets/{geneset_id}", response_model=GeneSet)
def read_geneset(geneset_id: int, db: Session = Depends(get_db)):
    db_geneset = get_geneset(db, geneset_id)
    if db_geneset is None:
        raise HTTPException(status_code=404, detail="GeneSet not found")
    return db_geneset

# Defining an endpoint to read all genesets with pagination.
@router.get("/genesets/", response_model=List[GeneSet])
def get_all_genesets(db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    genesets = get_genesets(db, skip=skip, limit=limit)
    return genesets

# Defining an endpoint to read a specific geneset by its ID.
@router.get("/genesets/{geneset_id}", response_model=GeneSet)
def get_geneset_endpoint(geneset_id: int, db: Session = Depends(get_db)):
    db_geneset = get_geneset(db, geneset_id)
    if db_geneset is None:
        raise HTTPException(status_code=404, detail="GeneSet not found")
    return db_geneset

# Defining an endpoint to delete a specific geneset by its ID.
@router.delete("/genesets/{geneset_id}", response_model=GeneSet)
def delete_geneset_endpoint(geneset_id: int, db: Session = Depends(get_db)):
    # Attempt to fetch the geneset from the database.
    db_geneset = get_geneset(db, geneset_id=geneset_id) 
    # If the geneset doesn't exist, return a 404 error.
    if db_geneset is None:
        raise HTTPException(status_code=404, detail="GeneSet not found")
    # If the geneset exists, delete it using the CRUD function.
    return delete_geneset(db, geneset_id=geneset_id)

# Defining an endpoint to update a specific geneset by its ID.
@router.put("/genesets/{geneset_id}", response_model=GeneSet)
def update_geneset_endpoint(geneset_id: int, geneset: GeneSetUpdate, db: Session = Depends(get_db)):
    db_geneset = update_geneset(db, geneset_id, geneset)
    if db_geneset is None:
        raise HTTPException(status_code=404, detail="GeneSet not found")
    return db_geneset

   
@router.post("/boolean-algebra/")
async def boolean_algebra_endpoint(
    request: BooleanAlgebraRequest, 
    db: Session = Depends(get_db)):
    
    # Convert GeneWeaver IDs to gene sets (sets of unigene values)
    geneset_sets = [get_geneset_unigenes(db, gene_weaver_id) for gene_weaver_id in request.gene_weaver_ids]
    
    if request.operation == "intersection":
        result = set.intersection(*geneset_sets)
    elif request.operation == "union":
        result = set.union(*geneset_sets)
    elif request.operation == "difference":
        # Symmetric difference in a context of more than 2 sets can be interpreted in different ways,
        # here we use one possible interpretation: elements which are in an odd number of sets
        result = set.symmetric_difference(*geneset_sets)
    else:
        raise HTTPException(status_code=400, detail="Invalid operation")

    return {"result": list(result)}

@router.post("/run-boolean-algebra/")
async def perform_boolean_algebra_endpoint(
    background_tasks: BackgroundTasks,
    request: BooleanAlgebraRequest, 
    db: Session = Depends(get_db)):
    
    # Create a new analysis run and get its ID
    new_run = create_analysis_run(db)
    run_id = new_run.id

    # Add the analysis task to background tasks
    background_tasks.add_task(
        perform_boolean_algebra_analysis, 
        run_id, 
        db, 
        request.gene_weaver_ids, 
        request.operation
    )

    return {"message": "Analysis started", "run_id": run_id}


@router.get("/analysis-runs/", response_model=List[AnalysisRunSchema])
def read_all_runs(db: Session = Depends(get_db)):
    return get_all_runs(db)

@router.get("/analysis-runs/{run_id}", response_model=AnalysisRunSchema)
def read_run(run_id: int, db: Session = Depends(get_db)):
    run = get_run(db, run_id)
    if run is None:
        raise HTTPException(status_code=404, detail="Run not found")
    return run

@router.delete("/analysis-runs/{run_id}", response_model=AnalysisRunSchema)
def cancel_run(run_id: int, db: Session = Depends(get_db)):
    try:
        run_to_cancel = crud_cancel_run(db, run_id)
        if run_to_cancel is None:
            raise HTTPException(status_code=404, detail="Run not found")
        return run_to_cancel
    except HTTPException as e:
        raise e

@router.get("/analysis-runs/{run_id}/result", response_model=AnalysisResultSchema)
def get_result(run_id: int, db: Session = Depends(get_db)):
    result = get_run_result(db, run_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Result not found for the run")
    return result


