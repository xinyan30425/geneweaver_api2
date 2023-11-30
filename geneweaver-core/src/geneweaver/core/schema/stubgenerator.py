"""
Stub generator schemas.
这是GeneWeaver程序中用于定义存根生成器（Stub Generator）的模式。

- StubGenerator：这是一个Pydantic模式，用来定义存根生成器的结构。它包含以下字段：
  - id：存根生成器的唯一标识符。
  - name：存根生成器的名称。
  - querystring：存根生成器使用的查询字符串，用于生成特定的数据查询或请求。
  - last_update：存根生成器上次更新的日期。

在GeneWeaver系统中，存根生成器可能用于自动化创建数据查询的过程，帮助用户更快地访问和分析特定类型的基因数据。例如，一个存根生成器可以用于快速生成特定疾病相关基因的查询，用户只需通过简单的界面操作就能执行这些预定义的查询，无需手动编写复杂的查询语句。
"""
from pydantic import BaseModel


class StubGenerator(BaseModel):
    """Stub generator schema."""

    id: int  # noqa: A003
    name: str
    querystring: str
    last_update: str
