"""Enum definitions for parsing 枚举."""
from enum import Enum


class FileType(str, Enum):
    """Enum for file types."""

    TEXT = "txt"
    EXCEL = "xlsx"
    CSV = "csv"


class GeneweaverFileType(str, Enum):
    """
    Enum for geneweaver specific file types.
    - BATCH: 代表批处理文件类型，这种文件包含了多个基因集，用于GeneWeaver项目中的批量数据处理。
    - VALUES: 代表值文件类型，这种文件只包含基因的数值信息，通常用于基因表达量或者其他分析值的记录。

    """

    BATCH = "batch"
    VALUES = "values"
