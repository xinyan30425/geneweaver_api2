"""
Models needed to work with the legacy API.
这些模型是用来与GeneWeaver程序中的传统API（Legacy API）进行交互的。通过这些模型，用户可以向系统添加新的基因集，同时关联相关的出版物信息。

- AddGenesetByUserPublication: 用于用户添加基因集时关联出版物信息的模式，包括出版物的摘要、作者、期刊、页面、PubMed信息、标题、卷号和年份。

- AddGenesetByUserBase: 添加基因集的基本信息模式，包括基因标识符、基因集缩写、描述、名称、阈值类型、权限、出版物信息和选择的用户组。

- AddGenesetByUser: 用户直接添加基因集的模式。除了基本信息外，还包括基因集的文本内容。

- AddGenesetByUserFile: 用户通过文件添加基因集的模式。除了基本信息外，还包括基因集文件的URL链接。

通过这些模型，GeneWeaver允许用户方便地将新的基因集和相应的出版物信息导入系统，从而支持科研数据的整合和共享。
"""
from typing import List, Optional

from geneweaver.core.enum import GenesetAccess, GenesetScoreType
from pydantic import BaseModel, HttpUrl


class AddGenesetByUserPublication(BaseModel):
    """Publication schema for adding genesets by user."""

    pub_abstract: Optional[str]
    pub_authors: Optional[str]
    pub_journal: Optional[str]
    pub_pages: Optional[str]
    pub_pubmed: Optional[str]
    pub_title: Optional[str]
    pub_volume: Optional[str]
    pub_year: Optional[str]


class AddGenesetByUserBase(BaseModel):
    """Base schema for adding genesets by user."""

    gene_identifier: str
    gs_abbreviation: str
    gs_description: str
    gs_name: str
    gs_threshold_type: GenesetScoreType
    permissions: GenesetAccess
    publication: Optional[AddGenesetByUserPublication]
    select_groups: List[str]
    sp_id: str

    class Config:
        """Pydantic config."""

        use_enum_values = True


class AddGenesetByUser(AddGenesetByUserBase):
    """Schema for adding genesets by user."""

    file_text: str


class AddGenesetByUserFile(AddGenesetByUserBase):
    """Schema for adding genesets by user from file."""

    file_url: HttpUrl
