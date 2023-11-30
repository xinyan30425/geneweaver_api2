"""
Pydantic schema for defining score types.
这些模式是GeneWeaver程序中用来定义评分类型（Score Types）的。

- ScoreType：这是一个枚举类（Enum），用于定义评分类型的不同种类。例如，P_VALUE表示P值，Q_VALUE表示Q值，BINARY表示二进制评分（通常是存在/不存在的标记），CORRELATION表示相关性评分，EFFECT表示效果大小评分。

- GenesetScoreType：这是一个Pydantic模式，用来定义具体的评分类型。它包含以下字段：
  - score_type：指定评分类型，必须是ScoreType枚举中的一个。
  - threshold_low：可选字段，如果是双边阈值（例如相关性评分或效果大小评分），则用来表示阈值的下限。
  - threshold：评分的阈值，默认是0.05。对于单边阈值（例如P值或Q值），这表示接受的最大值。

在GeneWeaver系统中，这些评分模式允许用户根据特定的统计标准来筛选和评估基因集。例如，研究者可能只想要P值小于0.05的基因，或者只关心相关性强度在特定范围内的基因。通过这些模式，GeneWeaver能够为用户提供强大的数据筛选和评估功能。
"""
from enum import Enum
from typing import Optional

from pydantic import BaseModel


class ScoreType(Enum):
    """Enum for defining score types."""

    P_VALUE = 1
    Q_VALUE = 2
    BINARY = 3
    CORRELATION = 4
    EFFECT = 5


class GenesetScoreType(BaseModel):
    """Pydantic schema for defining score types."""

    score_type: ScoreType
    threshold_low: Optional[float] = None
    threshold: float = 0.05
