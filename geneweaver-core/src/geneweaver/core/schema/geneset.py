"""
Schemas for geneset.
这个模块定义了基因集（Geneset）相关的数据结构。

这些数据结构用于表示基因集的详细信息，包括基因集的名称、缩写、描述、基因数量、阈值类型、创建日期等。

主要的数据结构有：
- Geneset: 基因集基本信息的模式，包括名称、缩写、描述等。
- GenesetGenes: 包含基因集中所有基因的模式。
- GenesetUpload: 基因集上传的模式，用于上传基因集到系统中。
- BatchUpload: 批量上传的模式，用于一次性上传多个基因集。
- GenesetInfo: 基因集详细信息的模式，包含访问次数、来源、分析等信息。
- SimilarGeneset: 类似基因集的模式，用于描述与其他基因集的相似度。
- GenesetRow: 用于数据库行的基因集模式，包含数据库操作所需的额外字段。

在GeneWeaver程序中，这些模式用来处理和存储基因集的信息。它们帮助确保基因集数据的准确性和一致性，并为程序提供了一个清晰的数据操作接口。这使得程序可以高效地从数据库查询、更新和管理基因集信息。
"""
import datetime
from typing import List

from geneweaver.core.enum import GenesetAccess, GenesetScoreType
from geneweaver.core.schema.gene import GeneValue
from pydantic import BaseModel, Field


class Geneset(BaseModel):
    """Geneset schema."""

    name: str
    abbreviation: str
    description: str
    count: int
    threshold_type: int
    threshold: str
    gene_id_type: int
    created: datetime.date
    admin_flag: str
    updated: datetime.datetime
    status: str
    gsv_qual: str
    attribution: int
    is_edgelist: bool


class GenesetGenes(BaseModel):
    """Geneset genes schema."""

    genes: List[GeneValue]


class GenesetUpload(BaseModel):
    """Geneset upload schema."""

    name: str
    label: str
    score_type: GenesetScoreType = Field(..., alias="score-type")
    description: str
    pubmed_id: str = Field(..., alias="pubmed-id")
    access: GenesetAccess
    groups: List[str]
    species: str
    gene_identifier: str = Field(..., alias="gene-identifier")
    gene_list: List[GeneValue] = Field(..., alias="gene-list")


class BatchUpload(BaseModel):
    """Batch upload schema."""

    batch_file: str
    curation_group: List[str]


class GenesetInfo(BaseModel):
    """Geneset info schema."""

    id: int  # noqa: A003
    page_views: int
    referers: List[str]
    analyses: List[str]
    resource_id: int
    last_sim: str
    last_ann: str
    jac_started: str
    jac_completed: str


class SimilarGeneset(Geneset):
    """Schema for similar geneset relation."""

    jax_value: float
    gic_value: float


class GenesetRow(BaseModel):
    """Geneset schema for database row."""

    gs_id: int
    usr_id: int
    file_id: int
    gs_name: str
    gs_abbreviation: str
    pub_id: int
    res_id: int
    cur_id: int
    gs_description: str
    sp_id: int
    gs_count: int
    gs_threshold_type: int
    gs_threshold: str
    gs_groups: str
    gs_attribution_old: str
    gs_uri: str
    gs_gene_id_type: int
    gs_created: datetime.date
    admin_flag: str
    gs_updated: datetime.datetime
    gs_status: str
    gsv_qual: str
    _comments_author: str
    _comments_curator: str
    gs_attribution: int
    gs_is_edgelist: bool
