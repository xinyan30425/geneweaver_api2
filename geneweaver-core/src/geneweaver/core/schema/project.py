"""
Project schemas.
这些模式是GeneWeaver程序中定义项目（Project）相关数据结构的。

- Project：这是一个基础类，用于定义一个项目。它包含项目的唯一标识ID（id），项目名称（name），项目所属的组（groups），会话ID（session_id），项目创建时间（created），项目备注（notes），以及项目的星标状态（star）。在GeneWeaver中，项目用于组织和管理与特定研究或分析任务相关联的基因集。

- ProjectCreate：这个类用于创建新项目的数据结构。它仅包含项目名称（name）和项目备注（notes）。当用户想要在GeneWeaver中开始一个新的研究项目时，会使用这个模式来提交必要的信息。

在GeneWeaver系统中，这些项目模式使得用户可以创建、管理、注释并组织他们的研究项目，每个项目可以关联到特定的基因集和分析结果，从而支持更有组织的数据管理和研究过程。
"""
from pydantic import BaseModel


class Project(BaseModel):
    """Project schema."""

    id: int  # noqa: A003
    name: str
    groups: list
    session_id: str
    created: str
    notes: str
    star: str


class ProjectCreate(BaseModel):
    """Project create schema."""

    name: str
    notes: str
