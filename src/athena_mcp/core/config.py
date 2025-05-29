"""
Configuration module for AWS Athena MCP Server.

This module centralizes all configuration values and environment variable handling.
"""

import os
from typing import Optional


class AthenaConfig:
    """Configuration class for AWS Athena MCP Server."""

    # Server configuration
    SERVER_NAME = "athena-connector"
    SERVER_VERSION = "1.0.0"

    # AWS configuration
    DEFAULT_REGION = "us-east-1"
    DEFAULT_DATABASE = "default"
    AWS_DATA_CATALOG = "AwsDataCatalog"

    # Display configuration
    MAX_DISPLAY_ROWS = 20

    # Environment variables
    @property
    def aws_access_key_id(self) -> Optional[str]:
        """Get AWS access key ID from environment."""
        return os.getenv("AWS_ACCESS_KEY_ID")

    @property
    def aws_secret_access_key(self) -> Optional[str]:
        """Get AWS secret access key from environment."""
        return os.getenv("AWS_SECRET_ACCESS_KEY")

    @property
    def aws_region(self) -> str:
        """Get AWS region from environment with fallback to default."""
        return os.getenv("AWS_DEFAULT_REGION", os.getenv("AWS_REGION", self.DEFAULT_REGION))

    @property
    def aws_profile(self) -> Optional[str]:
        """Get AWS profile from environment."""
        return os.getenv("AWS_PROFILE")

    @property
    def s3_output_location(self) -> Optional[str]:
        """Get S3 output location from environment."""
        return os.getenv("AWS_S3_OUTPUT_LOCATION")

    def has_explicit_credentials(self) -> bool:
        """Check if explicit AWS credentials are available."""
        return bool(self.aws_access_key_id and self.aws_secret_access_key)

    def has_profile_credentials(self) -> bool:
        """Check if AWS profile is configured."""
        return bool(self.aws_profile)


# Global configuration instance
config = AthenaConfig()
