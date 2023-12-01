# This will be a base class for gene set attributes shared among different schemas
# schemas.py

from pydantic import BaseModel,Field
from typing import List, Optional, Dict,Any
from .models import RunStatus

from geneweaver_boolean_algebra.src.schema import BooleanAlgebraType

# Add a class for parsing the uploaded file's data
class GeneSetFileRow(BaseModel):
    geneweaver_id: int = Field(..., alias='GeneWeaver ID')
    entrez: int = Field(..., alias='Entrez')
    ensembl_gene: str = Field(..., alias='Ensembl Gene')
    # ensembl_protein: str = Field(..., alias='Ensembl Protein')
    # ensembl_transcript: str = Field(..., alias='Ensembl Transcript')
    unigene: str = Field(..., alias='Unigene')
    # gene_symbol: Optional[str] = Field(alias='Gene Symbol', default=None)
    # mgi: str = Field(..., alias='MGI')
    # hgnc: str = Field(..., alias='HGNC')

    # RGD: str = Field(..., alias='RGD')
    # ZFIN: str = Field(..., alias='ZFIN')
    # FlyBase: str = Field(..., alias='FlyBase')
    # Wormbase: str = Field(..., alias='Wormbase')
    # SGD: str = Field(..., alias='SGD')
    # miRBase: str = Field(..., alias='miRBase')
    # CGNC: str = Field(..., alias='CGNC')

  
# This class is used to define the structure of the request to create a new geneset  
class GeneSetCreate(BaseModel):
    geneweaver_id: Optional[int] = Field(alias='GeneWeaver ID')
    entrez: Optional[int] = Field(alias='Entrez')
    ensembl_gene: Optional[str] = Field(alias='Ensembl Gene')
    unigene: List[str] = Field(default_factory=list, alias='Unigene')
    # gene_symbol: Optional[str] = Field(alias='Gene Symbol')

    # Method to create a GeneSetCreate instance from GeneSetFileRow
    @classmethod
    def from_file_row(cls, row: GeneSetFileRow) -> "GeneSetCreate":
        # Split 'Unigene' by '|' and convert to a list, ensure to use the correct field name from your CSV
        unigene_list = row.get('Unigene', '').split('|') if row.get('Unigene') else []
        return cls(
            geneweaver_id=row.geneweaver_id,
            entrez=row.entrez,
            ensembl_gene=row.ensembl_gene,
            unigene=unigene_list,  # Use the list created from splitting 'Unigene'
            # You can add other fields here if necessary, matching the row attributes.
        )

    class Config:
        allow_population_by_field_name = True  # Allows the use of aliases
        orm_mode = True
    
class GeneSetUpdate(BaseModel):
    # geneweaver_id: Optional[int]
    entrez: Optional[int]
    ensembl_gene: Optional[str]
    # gene_symbol: Optional[str]
    # other_fields: Optional[dict]

    class Config:
        orm_mode = True


class BooleanAlgebraInput(BaseModel):
    type: BooleanAlgebraType
    input_genesets: List[List[str]]
    intersection_min: Optional[int] = None 
    intersection_max: Optional[int] = None  
    
class GeneSet(BaseModel):
    id: int
    geneweaver_id: int
    entrez: Optional[int]
    ensembl_gene: Optional[str]
    unigene: Optional[dict]

    class Config:
        orm_mode = True
       
class BooleanAlgebraRequest(BaseModel):
    operation: str  # "intersection", "union", or "symmetric_difference"
    gene_weaver_ids: List[int]  # List of GeneWeaver IDs to perform the operation on
 
class AnalysisRunSchema(BaseModel):
    id:int
    status: RunStatus
    result: Optional[str] = None
    class Config:
        or_mode = True
    
class AnalysisRunSchema(BaseModel):
    id: int
    status: str

class AnalysisResultSchema(BaseModel):
    id: int
    run_id: int
    result_data: Optional[Any]
    


