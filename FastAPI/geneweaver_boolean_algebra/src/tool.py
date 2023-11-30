"""Boolean algebra tool.
定义了布尔代数工具的主要逻辑。"""
# ruff: noqa: D102
from __future__ import annotations

from pathlib import Path
from typing import Optional, Type

import sys 
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent / "FastAPI"))

from .symmetric_difference import symmetric_difference
from .union import union
from .intersection import combination_intersection

from geneweaver_tools.src.schema import ToolInput, ToolOutput
from geneweaver_tools.src.abstract import AbstractTool
from geneweaver_tools.src.enum import WorkflowType

from .schema import BooleanAlgebraInput, BooleanAlgebraOutput, BooleanAlgebraType

#根据输入的 BooleanAlgebraInput 对象执行相应的布尔代数操作，并返回 BooleanAlgebraOutput 结果。
class BooleanAlgebra(AbstractTool):
    """Boolean algebra tool."""

    @property
    def tool_input(self: AbstractTool) -> Type[ToolInput]:
        return BooleanAlgebraInput

    @property
    def tool_output(self: AbstractTool) -> Type[ToolOutput]:
        return BooleanAlgebraOutput

    def run(
        self: BooleanAlgebra, tool_input: BooleanAlgebraInput
    ) -> BooleanAlgebraOutput:
        genesets = tool_input.input_genesets
        inputs = tool_input if isinstance(genesets, set) else iterable_to_sets(genesets)

        if tool_input.type is BooleanAlgebraType.UNION:
            return BooleanAlgebraOutput(result=union(*inputs))
        elif tool_input.type is BooleanAlgebraType.INTERSECTION:
            return BooleanAlgebraOutput(
                result=combination_intersection(
                    *inputs,
                    min_size=tool_input.intersection_min,
                    max_size=tool_input.intersection_max,
                )
            )
        elif tool_input.type is BooleanAlgebraType.DIFFERENCE:
            return BooleanAlgebraOutput(result=symmetric_difference(*inputs))

    @property
    def workflow_definition(self: BooleanAlgebra) -> Optional[Path]:
        return Path(__file__).parent / "workflow" / "boolean_algebra.nf"

    @property
    def workflow_type(self: BooleanAlgebra) -> Optional[WorkflowType]:
        return WorkflowType.NEXTFLOW

    @property
    def tool_name(self: AbstractTool) -> str:
        return "Boolean Algebra"
