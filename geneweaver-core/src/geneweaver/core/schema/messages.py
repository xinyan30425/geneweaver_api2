"""
Namespace for defining schemas related to messaging.
这个命名空间用于定义与消息相关的模式。在GeneWeaver程序中，这些模式用于创建和传递不同类型的消息，以便于用户和系统之间的通信。

- MessageType：一个枚举（Enum），定义消息的类型。包括“信息”（INFO）、“警告”（WARNING）和“错误”（ERROR）。

- Message：一个基础类，定义了一条消息。包含消息内容（message），消息类型（message_type），和可选的详细信息（detail）。

- UserMessage：一个派生自Message的类，定义了发送给用户的消息。

- SystemMessage：一个派生自Message的类，定义了发送给系统的消息。

- MessageResponse：一个类，定义了一个包含消息的响应。它可能包含用户消息（user_messages）列表和系统消息（system_messages）列表。

在GeneWeaver系统中，这些模式允许程序以结构化的方式来发送和接收通知，错误警告，以及其他系统信息，有助于提高用户体验和系统的可靠性。
"""
import enum
from typing import List, Optional

from pydantic import BaseModel


class MessageType(enum.Enum):
    """Enum for defining the type of message."""

    INFO = "info"
    WARNING = "warning"
    ERROR = "error"


class Message(BaseModel):
    """Base class for defining a message."""

    message: str
    message_type: MessageType
    detail: Optional[str] = None


class UserMessage(Message):
    """Class for defining a message for a user."""


class SystemMessage(Message):
    """Class for defining a message for the system."""


class MessageResponse(BaseModel):
    """Class for defining a response containing messages."""

    user_messages: Optional[List[UserMessage]] = None
    system_messages: Optional[List[SystemMessage]] = None
