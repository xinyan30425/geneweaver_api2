"""
User related schemas.
这是GeneWeaver程序中与用户相关的数据模式。

- UserRequiredFields：这是用户基本信息的模式，包括以下字段：
  - id：用户的唯一标识符。
  - email：用户的电子邮件地址。
  - prefs：用户的偏好设置，默认为空的JSON字符串。
  - is_guest：标识用户是否为访客，布尔值，默认为False。

- User：基于UserRequiredFields的扩展，增加了一些可选信息：
  - first_name：用户的名字，可选。
  - last_name：用户的姓氏，可选。
  - password：用户的密码，可选。
  - admin：用户的管理员级别，使用枚举AdminLevel表示，默认为普通用户。
  - last_seen：最后一次访问系统的时间和日期，可选。
  - create：用户账号的创建日期，可选。
  - ip_address：用户的IP地址，可选。
  - api_key：用户的API密钥，可选。
  - sso_id：单点登录的用户ID，可选。

- UserFull：User模式的完整版，包括所有用户信息，以及：
  - groups：用户所属的组列表。
  - stubgenerators：用户有权访问的存根生成器列表。

在GeneWeaver系统中，这些模式用于管理用户账号和权限。管理员可以根据这些信息来控制用户的访问权限，追踪用户的活动，以及管理用户的偏好设置等。例如，存根生成器（Stub Generator）可以帮助用户快速生成和访问特定的数据查询，而用户所属的组则可能关联到特定的项目或数据集。

"""
import datetime
from typing import List, Optional

from geneweaver.core.enum import AdminLevel
from geneweaver.core.schema.stubgenerator import StubGenerator
from pydantic import BaseModel


class UserRequiredFields(BaseModel):
    """User schema for required fields."""

    id: int  # noqa: A003
    email: str
    prefs: str = "{}"
    is_guest: bool = False


class User(UserRequiredFields):
    """User schema."""

    first_name: Optional[str] = None
    last_name: Optional[str] = None
    password: Optional[str] = None
    admin: AdminLevel = AdminLevel.NORMAL_USER
    last_seen: Optional[datetime.datetime] = None
    create: Optional[datetime.date] = None
    ip_address: Optional[str] = None
    api_key: Optional[str] = None
    sso_id: Optional[str] = None


class UserFull(User):
    """User schema with full information."""

    groups: List[str]
    stubgenerators: List[StubGenerator]
