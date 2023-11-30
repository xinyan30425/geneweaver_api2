#endpoint.py

from typing import List
from fastapi import APIRouter, Depends, HTTPException, Body, File,UploadFile,HTTPException
from sqlalchemy.orm import Session
# Importing CRUD operations and schema models from the local modules.
from .crud import get_geneset, get_genesets, create_geneset, update_geneset, delete_geneset,perform_boolean_algebra
from .schemas import GeneSetCreate, GeneSetUpdate, GeneSet,GeneSetFileRow,AnalysisRunSchema
from .database import get_db 
import csv
import io
from .database import SessionLocal,get_db
from pydantic import ValidationError


# Adding the path to sys.path allows Python to find modules in a different directory.
import sys 
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent / "FastAPI"))
# Importing the BooleanAlgebra tool and input schema for boolean algebra operations.
from geneweaver_boolean_algebra.src.tool import BooleanAlgebra
from geneweaver_boolean_algebra.src.schema import BooleanAlgebraInput

# Creating an API router which will contain all the endpoint definitions.
router = APIRouter()

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

# Defining an endpoint for performing boolean algebra operations on genesets.
@router.post("/boolean-algebra/", response_model=GeneSet)
def boolean_algebra_endpoint(
    operation: str = Body(..., embed=True),
    geneset_ids: List[int] = Body(..., embed=True),
    db: Session = Depends(get_db)
):
    result_genes = crud.perform_boolean_algebra(db, operation, geneset_ids)

    if result_genes is None:
        raise HTTPException(status_code=404, detail="One or more GeneSets not found")

    return GeneSet(
        id=0,  # ID set to 0 or another placeholder value
        name=f"Result of {operation}",
        description="Result of Boolean Algebra operation",
        genes=result_genes
    )
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
                unigene=row.get('Unigene', ''),
                # gene_symbol=gene_symbol_list,
                mgi=row.get('MGI', ''),
                hgnc=row.get('HGNC', ''),
            )
            create_geneset(db, geneset_create)

        except ValidationError as e:
            # Handle the validation error
            print(f"Validation error for row: {row}, Error: {e}")

    return {"status": "success", "filename": file.filename}

# Endpoint to create an analysis run
@router.post("/analysis-runs/", response_model=AnalysisRunSchema)
def create_run_endpoint(db: Session = Depends(get_db)):
    return create_analysis_run(db)

# Endpoint to get all analysis runs
@router.get("/analysis-runs/", response_model=List[AnalysisRunSchema])
def get_all_runs_endpoint(db: Session = Depends(get_db)):
    return get_all_runs(db)

# Endpoint to get a specific run by ID
@router.get("/analysis-runs/{run_id}", response_model=AnalysisRunSchema)
def get_run_endpoint(run_id: int, db: Session = Depends(get_db)):
    run = get_run(db, run_id)
    if not run:
        raise HTTPException(status_code=404, detail="Analysis run not found")
    return run

# Endpoint to cancel a run
@router.delete("/analysis-runs/{run_id}", response_model=AnalysisRunSchema)
def cancel_run_endpoint(run_id: int, db: Session = Depends(get_db)):
    run = cancel_run(db, run_id)
    if not run:
        raise HTTPException(status_code=404, detail="Analysis run not found or not cancellable")
    return run

    

