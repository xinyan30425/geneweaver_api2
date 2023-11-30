"""
Exceptions related to file parsing.
与文件解析相关的异常类，用于GeneWeaver程序中处理特定的错误情况。
"""


class UnsupportedFileTypeError(Exception):
    """
    Custom exception for when a file type is not supported.
    当程序尝试处理一个不支持的文件类型时，会抛出这个自定义异常。
    """

    pass


class EmptyFileError(UnsupportedFileTypeError):
    """Custom exception for when a file is empty.

    Attributes
    ----------
        file_path -- the path of the file that is empty
        message -- explanation of the error
    """

    def __init__(
        self: "EmptyFileError", file_path: str, message: str = "File is empty."
    ) -> None:
        """Initialize the exception."""
        self.file_path = file_path
        self.message = message
        super().__init__(self.message)

    def __str__(self: "EmptyFileError") -> str:
        """Return a string representation of the exception."""
        return f"{self.file_path} -> {self.message}"


class NotAHeaderRowError(Exception):
    """
    Raised when a row is not a header row.
    当程序预期应该读取到一个表头行(header row)但实际上没有找到时
    """

    pass


class InvalidBatchValueLineError(Exception):
    """
    Raised when a value line is invalid.
    当程序预期应该读取到一个表头行(header row)但实际上没有找到时
    """

    pass


class MultiLineStringError(Exception):
    """
    Raised when a string is multiline (but shouldn't be).
    当一个字符串中包含了多行（但预期应该是单行）时
    """

    pass


class IgnoreLineError(Exception):
    """
    Raised when a line should be ignored.
    当文件中的某一行应该被忽略时,比如，某些行可能只是注释或者不包含有用数据。
    """

    pass


class MissingRequiredHeaderError(Exception):
    """
    Raised when a required header is missing.
    当文件中缺少必需的表头信息时
    """

    pass


class InvalidScoreThresholdError(Exception):
    """
    Raised when a score threshold is invalid.
    当分数阈值(score threshold)无效或不符合预期格式时
    """

    pass
