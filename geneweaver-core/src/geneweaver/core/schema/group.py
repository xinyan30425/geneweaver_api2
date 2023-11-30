"""
Group schemas.
这个模块定义了与用户组（Group）相关的数据结构。

在GeneWeaver程序中，用户组是一种可以包含多个用户的实体，这些用户可以共享和管理基因集数据。这些数据结构用于描述组的详细信息，例如组的ID、名称、是否为私有组、创建日期等。

主要的数据结构有：
- Group: 用户组的基本信息模式，包括组的ID、名称、是否为私有组、创建日期和相关的存根生成器。
- UserAdminGroup: 用户管理组的模式，用于表示用户的管理权限以及组是否对外公开。

通过这些数据结构，GeneWeaver能够管理用户组的信息，允许用户创建和管理自己的组，分享基因集给组内的其他成员，以及控制数据的访问权限。这些功能对于协作研究和数据共享非常有用。

"""
import datetime
from typing import List

from geneweaver.core.schema.stubgenerator import StubGenerator
from pydantic import BaseModel


class Group(BaseModel):
    """Group schema."""

    id: int  # noqa: A003
    name: str
    private: bool
    created: datetime.date
    stubgenerators: List[StubGenerator]


class UserAdminGroup(BaseModel):
    """User admin group schema."""

    name: str
    public: bool
    created: datetime.date
