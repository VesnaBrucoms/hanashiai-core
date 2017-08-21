"""Hanashiai - Core exceptions module."""


class HanashiaiCoreError(Exception):
    """Base error class for all Hanashiai - Core errors."""


class RedditResponseError(HanashiaiCoreError):
    """Raised when there is a failure to connect to Reddit.

    This error is raised when the response from Reddit is anything
    other than 200.

    Args:
        message (str): The error message

    Attributes:
        message (str): The error message
        code (str): The error code
    """

    def __init__(self, message):
        self.message = message
        self.code = "CORE.RDCN"
