"""
Custom exceptions for AWS Athena MCP Server.

This module defines domain-specific exceptions for better error handling and debugging.
"""


class AthenaMCPError(Exception):
    """Base exception for all Athena MCP Server errors."""

    pass


class AthenaClientError(AthenaMCPError):
    """Exception raised when there are issues with the Athena client."""

    pass


class AthenaCredentialsError(AthenaMCPError):
    """Exception raised when there are AWS credentials issues."""

    pass


class S3ConfigurationError(AthenaMCPError):
    """Exception raised when S3 output location is invalid or missing."""

    pass


class QueryExecutionError(AthenaMCPError):
    """Exception raised when Athena query execution fails."""

    def __init__(self, message: str, query_id: str = None, error_reason: str = None):
        """
        Initialize QueryExecutionError.

        Args:
            message: Error message
            query_id: Athena query execution ID
            error_reason: Specific reason for query failure
        """
        super().__init__(message)
        self.query_id = query_id
        self.error_reason = error_reason


class DatabaseNotFoundError(AthenaMCPError):
    """Exception raised when a specified database is not found."""

    def __init__(self, database_name: str):
        """
        Initialize DatabaseNotFoundError.

        Args:
            database_name: Name of the database that was not found
        """
        super().__init__(f"Database '{database_name}' not found")
        self.database_name = database_name


class ToolNotFoundError(AthenaMCPError):
    """Exception raised when a requested tool is not available."""

    def __init__(self, tool_name: str):
        """
        Initialize ToolNotFoundError.

        Args:
            tool_name: Name of the tool that was not found
        """
        super().__init__(f"Tool '{tool_name}' not found")
        self.tool_name = tool_name
