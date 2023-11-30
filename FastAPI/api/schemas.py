# This will be a base class for gene set attributes shared among different schemas
# schemas.py

from pydantic import BaseModel,Field
from typing import List, Optional, Dict
from .models import RunStatus

from geneweaver_boolean_algebra.src.schema import BooleanAlgebraType

# Add a class for parsing the uploaded file's data
class GeneSetFileRow(BaseModel):
    geneweaver_id: int = Field(..., alias='GeneWeaver ID')
    entrez: int = Field(..., alias='Entrez')
    ensembl_gene: str = Field(..., alias='Ensembl Gene')
    ensembl_protein: str = Field(..., alias='Ensembl Protein')
    ensembl_transcript: str = Field(..., alias='Ensembl Transcript')
    unigene: str = Field(..., alias='Unigene')
    # gene_symbol: Optional[str] = Field(alias='Gene Symbol', default=None)
    mgi: str = Field(..., alias='MGI')
    hgnc: str = Field(..., alias='HGNC')
    print("aaaaaaaaaaaaaaaaaaaaaaaa")
    print(geneweaver_id)
    print("aaaaaaaaaaaaaaaaaaaaaaaa")
    # RGD: str = Field(..., alias='RGD')
    # ZFIN: str = Field(..., alias='ZFIN')
    # FlyBase: str = Field(..., alias='FlyBase')
    # Wormbase: str = Field(..., alias='Wormbase')
    # SGD: str = Field(..., alias='SGD')
    # miRBase: str = Field(..., alias='miRBase')
    # CGNC: str = Field(..., alias='CGNC')

# This class is used to define the structure of the request to create a new geneset
# class GeneSetCreate(BaseModel):
#     name: str
#     description: Optional[str] = None
#     genes: List[str]
    
# This class is used to define the structure of the request to create a new geneset  
class GeneSetCreate(BaseModel):
    geneweaver_id: Optional[int] = Field(alias='GeneWeaver ID')
    entrez: Optional[int] = Field(alias='Entrez')
    ensembl_gene: Optional[str] = Field(alias='Ensembl Gene')
    # gene_symbol: Optional[str] = Field(alias='Gene Symbol')

    # Method to create a GeneSetCreate instance from GeneSetFileRow
    @classmethod
    def from_file_row(cls, row: GeneSetFileRow) -> "GeneSetCreate":
        return cls(
            name=row.GeneWeaver_ID,
            description="Uploaded from file",  # Set a default description or use a field from the file
            genes=row.Entrez.split(';') if row.Entrez else [],  # Assuming genes are separated by semicolons
            # other_fields=row.dict(exclude_unset=True, exclude={'GeneWeaver_ID', 'Entrez', 'Gene_Symbol'})
        )

    class Config:
        allow_population_by_field_name = True  # Allows the use of aliases
        orm_mode = True
    
class GeneSetUpdate(BaseModel):
    gene_weaver_id: Optional[int]
    entrez: Optional[int]
    ensembl_gene: Optional[str]
    # gene_symbol: Optional[str]
    other_fields: Optional[dict]

    class Config:
        orm_mode = True

# This class is used to define the structure of the response when a geneset is returned
class GeneSet(BaseModel):
    id: int
    gene_weaver_id: int
    entrez: Optional[int]
    ensembl_gene: Optional[str]
    # gene_symbol: Optional[str]
    other_fields: Optional[dict]

    class Config:
        orm_mode = True

class BooleanAlgebraInput(BaseModel):
    type: BooleanAlgebraType
    input_genesets: List[List[str]]
    intersection_min: Optional[int] = None 
    intersection_max: Optional[int] = None  
    
class GeneSet(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    genes: List[str]

    class Config:
        orm_mode = True
        
class AnalysisRunSchema(BaseModel):
    id:int
    status: RunStatus
    result: Optional[str] = None
    class Config:
        or_mode = True
    
    
    


