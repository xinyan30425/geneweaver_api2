"""
Gene schema.
这些数据结构是用来表示基因信息的，包括基因在数据库中的唯一标识、它的参考ID、所属物种、是否为首选基因等信息。

主要的数据结构有：
- Gene: 基础的基因模式，包含了基因的核心信息。
- GeneRow: 用于数据库行的基因模式，包含了数据库操作所需的额外字段。
- GeneValue: 用于总结基因值的模式，例如可能用于报告或展示在界面上的基因数据。
- GeneDatabase: 基因数据库的模式，描述了基因数据库的基本信息，如名称、简称、所属物种等。
- GeneDatabaseRow: 用于数据库行的基因数据库模式，包含了数据库操作所需的额外字段，如数据库ID、物种ID、准确度等。

在GeneWeaver程序中，这些模式被用来处理和存储基因信息。它们帮助确保基因数据的准确性和一致性，并为程序提供了一个清晰的数据操作接口。这使得程序可以高效地从数据库查询、更新和管理基因信息。
"""
import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class Gene(BaseModel):
    """Gene schema."""

    id: int  # noqa: A003
    reference_id: str
    gene_database: str
    species: str
    preferred: bool
    date: str


class GeneRow(BaseModel):
    """Gene schema for database row."""

    ode_gene_id: int
    ode_ref_id: str
    gdb_id: int
    sp_id: int
    ode_pref: bool
    ode_date: Optional[str]
    old_ode_gene_ids: Optional[List[int]]


class GeneValue(BaseModel):
    """Schema for summary Gene values."""

    gene_id: str = Field(..., alias="gene-id")
    value: str


class GeneDatabase(BaseModel):
    """Gene database schema."""

    name: str
    shortname: str
    species: str
    data: datetime.datetime
    precision: int


class GeneDatabaseRow(BaseModel):
    """Gene database schema for database row."""

    gdb_id: int
    gdb_name: str
    sp_id: int
    gdb_shortname: str
    gdb_date: str
    gdb_precision: int
    gdb_linkout_url: Optional[str]
