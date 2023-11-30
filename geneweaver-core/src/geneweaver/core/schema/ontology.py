"""
Ontology schema.
这些模式用于定义GeneWeaver程序中的本体（Ontology）相关数据结构。

- Ontology：一个基础类，用于定义一个本体。包含本体ID（ontology_id）、参考ID（reference_id）、名称（name）、描述（description）、子本体（children）、父本体（parents）、本体数据库ID（ontdb_id）和关系本体ID（ro_ont_id）。本体通常用来表示一组相关概念和它们之间的关系，在GeneWeaver中，本体用于组织和分类基因集数据。

- OntologyDB：本体数据库的模式类。包括本体数据库ID（ontology_db_id）、名称（name）、前缀（prefix）、NCBO ID（用于标识National Center for Biomedical Ontology中的相应本体）、日期（date）、链接外部URL（linkout_url）和NCBO版本ID（ncbo_vid）。

在GeneWeaver系统中，本体和本体数据库的模式用于存储和组织与基因集相关联的本体信息，使得用户能够更加直观和有效地查询和分析基因集数据。本体数据结构允许GeneWeaver保持数据的层次性和关联性，以支持复杂的数据分析和查询。

"""
from typing import List

from pydantic import BaseModel


class Ontology(BaseModel):
    """Ontology schema."""

    ontology_id: int
    reference_id: int
    name: str
    description: str
    children: List["Ontology"]
    parents: List["Ontology"]
    ontdb_id: int
    ro_ont_id: int


class OntologyDB(BaseModel):
    """Ontology database schema."""

    ontology_db_id: int
    name: str
    prefix: str
    ncbo_id: str
    date: str
    linkout_url: str
    ncbo_vid: str
