"""
Unit tests for validation utilities.
"""

import pytest

from src.athena_mcp.utils.validators import (
    S3OutputValidator,
    validate_database_name,
    validate_query_length,
)


class TestS3OutputValidator:
    """Test cases for S3OutputValidator."""

    def test_valid_s3_url(self):
        """Test valid S3 URLs."""
        assert S3OutputValidator.is_valid("s3://my-bucket/path/")
        assert S3OutputValidator.is_valid("s3://my-bucket")
        assert S3OutputValidator.is_valid("s3://my-bucket/subfolder/results/")

    def test_invalid_s3_url(self):
        """Test invalid S3 URLs."""
        assert not S3OutputValidator.is_valid(None)
        assert not S3OutputValidator.is_valid("")
        assert not S3OutputValidator.is_valid("http://example.com")
        assert not S3OutputValidator.is_valid("s3://")
        assert not S3OutputValidator.is_valid("s3:///path")

    def test_error_messages(self):
        """Test error message generation."""
        # Test None case
        error_msg = S3OutputValidator.get_error_message(None)
        assert "AWS_S3_OUTPUT_LOCATION environment variable is required" in error_msg

        # Test invalid format case
        error_msg = S3OutputValidator.get_error_message("http://example.com")
        assert "must start with 's3://'" in error_msg

        # Test empty bucket case
        error_msg = S3OutputValidator.get_error_message("s3://")
        assert "Invalid AWS_S3_OUTPUT_LOCATION format" in error_msg


class TestDatabaseNameValidator:
    """Test cases for database name validation."""

    def test_valid_database_names(self):
        """Test valid database names."""
        assert validate_database_name("test_db")
        assert validate_database_name("testdb")
        assert validate_database_name("test123")
        assert validate_database_name("TEST_DB")

    def test_invalid_database_names(self):
        """Test invalid database names."""
        assert not validate_database_name(None)
        assert not validate_database_name("")
        assert not validate_database_name("test-db")  # hyphen not allowed
        assert not validate_database_name("test.db")  # dot not allowed
        assert not validate_database_name("test db")  # space not allowed


class TestQueryLengthValidator:
    """Test cases for query length validation."""

    def test_valid_query_lengths(self):
        """Test valid query lengths."""
        assert validate_query_length("SELECT * FROM table")
        assert validate_query_length("SELECT 1", max_length=10)
        assert validate_query_length("   SELECT * FROM table   ")  # with whitespace

    def test_invalid_query_lengths(self):
        """Test invalid query lengths."""
        long_query = "SELECT * FROM table WHERE " + "x = 1 AND " * 1000
        assert not validate_query_length(long_query, max_length=100)
        assert not validate_query_length("SELECT 1234567890", max_length=10)
