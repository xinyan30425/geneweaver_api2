"""
Enum classes for the GeneWeaver project.
这些是GeneWeaver项目中用到的枚举类（Enum classes），用于定义系统中使用的一些标准化的选择项。

- CurationAssignment：这是一个枚举类，用于定义文献整理（curation）任务的不同状态。例如：
  - UNASSIGNED（未分配）：任务尚未分配给任何人。
  - ASSIGNED（已分配）：任务已经分配给某人。
  - READY_FOR_REVIEW（准备审查）：任务已完成，准备进行审查。
  - REVIEWED（已审查）：任务已经被审查过。
  - APPROVED（已批准）：任务审查通过，已被批准。

- GenesetScoreTypeStr：这是一个基于字符串的枚举类，用于定义基因集分数的不同类型。例如：
  - P_VALUE（P值）
  - Q_VALUE（Q值）
  - BINARY（二元，即有无，是非）
  - CORRELATION（相关性）
  - EFFECT（效果）

- GenesetScoreType：这是一个基于整数的枚举类，和GenesetScoreTypeStr相对应，也是用于定义基因集分数的不同类型。

- GenesetAccess：这是一个枚举类，用于定义基因集的不同访问类型。例如：
  - PRIVATE（私有）：只有特定用户可以访问的基因集。
  - PUBLIC（公开）：所有用户都可以访问的基因集。

- AnnotationType：这是一个枚举类，用于定义不同类型的注释。例如：
  - MONARCH（君主）
  - NCBO（生物医学本体中心）

- AdminLevel：这是一个枚举类，用于定义不同级别的管理员权限。例如：
  - NORMAL_USER（普通用户）
  - CURATOR（策展人）
  - ADMIN（管理员）
  - ADMIN_WITH_DEBUG（具有调试权限的管理员）

在GeneWeaver系统中，这些枚举类用于在数据库存储、数据处理和用户界面中保持一致性。例如，当一个基因集被创建时，会使用GenesetAccess枚举来设置它的访问级别，或者在用户完成文献整理任务时，会更新任务的状态为CurationAssignment中相应的值。
"""
from enum import Enum


class CurationAssignment(int, Enum):
    """Enum for the different types of curation assignments."""

    UNASSIGNED = 1
    ASSIGNED = 2
    READY_FOR_REVIEW = 3
    REVIEWED = 4
    APPROVED = 5


class GenesetScoreTypeStr(str, Enum):
    """Enum for the different types of geneset scores."""

    P_VALUE = "p-value"
    Q_VALUE = "q-value"
    BINARY = "binary"
    CORRELATION = "correlation"
    EFFECT = "effect"


class GenesetScoreType(int, Enum):
    """Integer based Enum for the different types of geneset scores."""

    P_VALUE = 1
    Q_VALUE = 2
    BINARY = 3
    CORRELATION = 4
    EFFECT = 5


class GenesetAccess(str, Enum):
    """Enum for the different types of geneset access."""

    PRIVATE = "private"
    PUBLIC = "public"


class AnnotationType(str, Enum):
    """Enum for the different types of annotations."""

    MONARCH = "monarch"
    NCBO = "ncbo"


class AdminLevel(int, Enum):
    """Enum for the different levels of admin access."""

    NORMAL_USER = 0
    CURATOR = 1
    ADMIN = 2
    ADMIN_WITH_DEBUG = 3
