"""
Validation utilities for AWS Athena MCP Server.

This module contains validation functions for various inputs and configurations.
"""

from typing import Optional


class S3OutputValidator:
    """Utility class for validating S3 output locations."""

    @staticmethod
    def is_valid(location: Optional[str]) -> bool:
        """
        Validate if the S3 output location is properly formatted.

        Args:
            location: S3 URL to validate

        Returns:
            bool: True if valid, False otherwise
        """
        if not location:
            return False

        if not location.startswith("s3://"):
            return False

        # Check if it has at least bucket name after s3://
        parts = location[5:].split("/", 1)  # Remove s3:// and split
        if not parts[0]:  # Empty bucket name
            return False

        return True

    @staticmethod
    def get_error_message(location: Optional[str]) -> str:
        """
        Get detailed error message for S3 output location validation.

        Args:
            location: S3 URL that failed validation

        Returns:
            str: Detailed error message
        """
        if not location:
            return (
                "❌ Error: AWS_S3_OUTPUT_LOCATION environment variable is required to execute queries. "
                "Please configure it in your MCP settings.\n\n"
                "Example: s3://your-bucket/athena-results/"
            )
        elif not location.startswith("s3://"):
            return (
                f"❌ Error: AWS_S3_OUTPUT_LOCATION must start with 's3://'. "
                f"Current value: '{location}'\n\n"
                "Example: s3://your-bucket/athena-results/"
            )
        else:
            return (
                f"❌ Error: Invalid AWS_S3_OUTPUT_LOCATION format: '{location}'\n\n"
                "Example: s3://your-bucket/athena-results/"
            )


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


def validate_query_length(query: str, max_length: int = 10000) -> bool:
    """
    Validate if a query is within acceptable length limits.

    Args:
        query: SQL query to validate
        max_length: Maximum allowed query length

    Returns:
        bool: True if valid, False otherwise
    """
    return len(query.strip()) <= max_length
