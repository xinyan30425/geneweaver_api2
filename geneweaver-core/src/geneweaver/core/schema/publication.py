"""
Publication schemas.
这些模式是GeneWeaver程序中定义出版物（Publication）相关数据结构的。

- PublicationInfo：这是一个基础类，用于定义出版物的上传信息（但没有包含唯一标识ID）。它包含作者（authors），标题（title），摘要（abstract），期刊名称（journal），卷号（volume），页码（pages），出版月份（month），出版年份（year），以及PubMed ID（pubmed_id）。这个模式用于在GeneWeaver系统中上传新的出版物信息，通常是与特定的基因集或研究结果相关联的。

- Publication：这个类是PublicationInfo的扩展，增加了出版物的唯一标识ID（id）。这个ID用于在GeneWeaver系统中唯一标识一个出版物实体，使得可以轻松地引用、搜索和管理相关的出版物。

在GeneWeaver系统中，这些出版物模式允许用户将具体的科研论文与基因集、分析结果等数据关联起来，为生物医学研究提供文献支持和引用的功能。
"""
from typing import Optional

from pydantic import BaseModel


class PublicationInfo(BaseModel):
    """Publication upload schema (no ID)."""

    authors: str
    title: str
    abstract: str
    journal: Optional[str] = None
    volume: Optional[str] = None
    pages: str
    month: str
    year: int
    pubmed_id: int


class Publication(PublicationInfo):
    """Publication schema (with ID)."""

    id: int  # noqa: A003
