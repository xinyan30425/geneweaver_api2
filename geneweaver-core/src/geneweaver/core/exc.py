"""
Custom exceptions for the GeneWeaver project.
这是GeneWeaver项目中自定义异常类的定义，用于在项目中处理特定的错误情况。

- GeneweaverError：这是所有GeneWeaver异常的基类。在GeneWeaver项目中，所有自定义的异常都会从这个基类派生。这样做可以方便地捕获和处理项目中所有特定的异常。

- ExternalAPIError：这是所有外部API异常的基类。当GeneWeaver系统与外部API交互时，如果遇到了API调用错误或其他与外部API交互相关的问题，就会抛出这个异常。从这个基类派生的异常可以包含更详细的错误信息，比如HTTP状态码或API错误消息，以便于调试和错误处理。

在GeneWeaver系统中，当外部API调用失败或返回了不预期的结果时，可以使用ExternalAPIError来标识这些情况，并在系统的不同层次中传播错误信息，比如从网络请求层传播到服务层或用户界面层。这有助于提高代码的可维护性和错误的可追溯性。
"""


class GeneweaverError(Exception):
    """Base class for all Geneweaver exceptions."""

    pass


class ExternalAPIError(GeneweaverError):
    """Base class for all external API exceptions."""

    pass

