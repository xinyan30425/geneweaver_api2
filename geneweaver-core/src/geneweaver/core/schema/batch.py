"""
Module for defining schemas for batch endpoints.
这个模块定义了批量上传端点的模式（schema）。

这些类定义了批量上传文件中使用的基因集（geneset）的结构，并且定义了相应的响应格式。

主要的类有：
- BatchResponse: 定义了包含批量上传结果的响应结构。
- GenesetValueInput: 定义了上传的基因集的值。
- GenesetValue: 定义了处理后的基因集的值。
- BatchUploadGeneset: 定义了使用批量上传文件上传的基因集。

这些类中的验证器（validator）函数用于在创建实例时对数据进行处理和验证。例如：
- "score" 验证器用于初始化分数类型，使用 `parse_score` 函数将字符串转换成 GenesetScoreType 对象。
- "private" 验证器将私有字段的字符串转换为布尔值。
- "curation_id" 验证器根据 "private" 值初始化策展ID。如果未指定，默认为私有。

在GeneWeaver程序中，这些模式用于处理和验证通过API上传的基因集数据。通过定义这些结构，程序可以确保上传的数据符合预期格式，并能够有效地处理和存储这些数据。
"""
# ruff: noqa: N805, ANN001, ANN101
from typing import List, Optional

from geneweaver.core.parse.score import parse_score
from geneweaver.core.schema.messages import MessageResponse
from geneweaver.core.schema.score import GenesetScoreType
from pydantic import BaseModel, validator


class BatchResponse(BaseModel):
    """Class for defining a response containing batch results."""

    genesets: List[int]
    messages: MessageResponse


class GenesetValueInput(BaseModel):
    """Class for defining a geneset value as uploaded."""

    symbol: str
    value: float


class GenesetValue(BaseModel):
    """Class for defining a geneset value as processed."""

    ode_gene_id: str
    value: float
    ode_ref_id: str
    threshold: bool


class BatchUploadGeneset(BaseModel):
    """Class for defining a geneset uploaded using a batch upload file."""

    score: GenesetScoreType
    # TODO: Use enum from core
    species: str
    gene_id_type: str
    pubmed_id: str
    private: bool = True
    curation_id: Optional[int] = None
    abbreviation: str
    name: str
    description: str
    values: List[GenesetValueInput]

    @validator("score", pre=True)
    def initialize_score(cls, v) -> GenesetScoreType:
        """Initialize score type."""
        return parse_score(v)

    @validator("private", pre=True)
    def private_to_bool(cls, v) -> bool:
        """Convert private str to bool."""
        return v.lower() != "public"

    @validator("curation_id", pre=True)
    def curation_id_to_int(cls, v, values) -> int:
        """Initialize curation id based on `private` value."""
        if not v:
            # If the geneset is private, it should be set to have
            # curation tier 5, otherwise it should be set to have
            # curation tier 4.
            # It should default to private if not specified.
            return 5 if values.get("private", True) else 4
        return v
