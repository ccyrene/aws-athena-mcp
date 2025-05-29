"""
Utility functions for AWS Athena MCP Server.

This module contains helper functions and utilities used across the application.
"""

import logging
import sys
from typing import Any, Dict, Optional

from mcp import types


def setup_logging(name: str = "athena-mcp") -> logging.Logger:
    """
    Setup logging configuration for the application.

    Args:
        name: Logger name

    Returns:
        logging.Logger: Configured logger instance
    """
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        stream=sys.stderr,  # MCP captures stderr for logs
        force=True,
    )
    return logging.getLogger(name)


def create_error_response(message: str) -> list[types.TextContent]:
    """
    Create a standardized error response for MCP tools.

    Args:
        message: Error message to display

    Returns:
        List of TextContent with error message
    """
    return [types.TextContent(type="text", text=message)]


def create_success_response(message: str) -> list[types.TextContent]:
    """
    Create a standardized success response for MCP tools.

    Args:
        message: Success message to display

    Returns:
        List of TextContent with success message
    """
    return [types.TextContent(type="text", text=message)]


def truncate_query_for_log(query: str, max_length: int = 100) -> str:
    """
    Truncate a SQL query for logging purposes.

    Args:
        query: SQL query string
        max_length: Maximum length for the truncated query

    Returns:
        str: Truncated query string
    """
    if len(query) <= max_length:
        return query
    return query[:max_length] + "..."


def format_aws_error(error_code: str, error_message: str) -> str:
    """
    Format AWS error messages in a standardized way.

    Args:
        error_code: AWS error code
        error_message: AWS error message

    Returns:
        str: Formatted error message
    """
    return f"❌ AWS error ({error_code}): {error_message}"


def validate_database_name(database_name: Optional[str]) -> bool:
    """
    Validate if a database name is valid.

    Args:
        database_name: Database name to validate

    Returns:
        bool: True if valid, False otherwise
    """
    if not database_name:
        return False

    # Basic validation: no empty strings, no special characters except underscore
    if not database_name.replace("_", "").isalnum():
        return False

    return True


def sanitize_query(query: str) -> str:
    """
    Basic sanitization for SQL queries (remove potential harmful patterns).

    Note: This is a basic sanitization. For production use, consider more robust
    SQL injection prevention mechanisms.

    Args:
        query: SQL query to sanitize

    Returns:
        str: Sanitized query
    """
    # Remove leading/trailing whitespace
    query = query.strip()

    # Basic checks for obviously dangerous patterns
    dangerous_patterns = [
        "DROP DATABASE",
        "DROP TABLE",
        "DELETE FROM",
        "TRUNCATE",
        "ALTER TABLE",
        "CREATE USER",
        "DROP USER",
        "GRANT",
        "REVOKE",
    ]

    query_upper = query.upper()
    for pattern in dangerous_patterns:
        if pattern in query_upper:
            logging.getLogger(__name__).warning(
                f"Potentially dangerous SQL pattern detected: {pattern}"
            )

    return query
