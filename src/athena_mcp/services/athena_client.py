"""
AWS Athena client service.

This module provides factory and management functionality for AWS Athena clients.
"""

import logging
from typing import Optional

import boto3
from botocore.exceptions import ClientError, NoCredentialsError, PartialCredentialsError

from ..core.config import config
from ..core.exceptions import AthenaClientError, AthenaCredentialsError


class AthenaClientFactory:
    """Factory class for creating AWS Athena clients with different authentication methods."""

    @staticmethod
    def create_client() -> boto3.client:
        """
        Create an AWS Athena client using available credentials.

        Returns:
            boto3.client: Configured Athena client

        Raises:
            AthenaClientError: If client creation fails
            AthenaCredentialsError: If credentials are invalid or missing
        """
        logger = logging.getLogger(__name__)

        try:
            if config.has_explicit_credentials():
                logger.info("Using explicit AWS credentials")
                return boto3.client(
                    "athena",
                    aws_access_key_id=config.aws_access_key_id,
                    aws_secret_access_key=config.aws_secret_access_key,
                    region_name=config.aws_region,
                )
            elif config.has_profile_credentials():
                logger.info(f"Using AWS profile: {config.aws_profile}")
                session = boto3.Session(profile_name=config.aws_profile)
                return session.client("athena", region_name=config.aws_region)
            else:
                logger.info("Using default AWS credentials")
                return boto3.client("athena", region_name=config.aws_region)

        except (NoCredentialsError, PartialCredentialsError) as e:
            logger.error(f"AWS credentials error: {e}")
            raise AthenaCredentialsError(f"AWS credentials not found or incomplete: {e}") from e
        except Exception as e:
            logger.error(f"Error creating Athena client: {e}")
            raise AthenaClientError(f"Failed to create Athena client: {e}") from e


class AthenaClientManager:
    """Manager class for Athena client lifecycle and connectivity testing."""

    def __init__(self, client: boto3.client):
        """
        Initialize the Athena client manager.

        Args:
            client: Configured boto3 Athena client
        """
        self.client = client
        self.logger = logging.getLogger(__name__)

    async def test_connectivity(self) -> dict:
        """
        Test connectivity with AWS Athena and return database information.

        Returns:
            dict: Connectivity test results with database count and names

        Raises:
            AthenaClientError: If connectivity test fails
        """
        try:
            self.logger.info("🔍 Testing connectivity with AWS Athena...")
            databases = self.client.list_databases(CatalogName=config.AWS_DATA_CATALOG)
            db_count = len(databases.get("DatabaseList", []))

            self.logger.info(
                f"✅ Connection with AWS Athena established successfully! Found {db_count} databases."
            )

            # Log available databases
            db_names = []
            if db_count > 0:
                db_names = [db["Name"] for db in databases["DatabaseList"][:5]]  # Only first 5
                self.logger.info(f"📚 First databases: {', '.join(db_names)}")
                if db_count > 5:
                    self.logger.info(f"📚 ... and {db_count - 5} more databases")

            return {"connected": True, "database_count": db_count, "database_names": db_names}

        except ClientError as e:
            error_code = e.response["Error"]["Code"]
            error_message = e.response["Error"]["Message"]
            self.logger.error(f"❌ AWS error in connectivity: {error_code} - {error_message}")
            raise AthenaClientError(
                f"AWS connectivity error ({error_code}): {error_message}"
            ) from e
        except (NoCredentialsError, PartialCredentialsError) as e:
            self.logger.error(f"❌ Error: AWS credentials issue - {e}")
            raise AthenaCredentialsError(f"AWS credentials issue: {e}") from e
        except Exception as e:
            self.logger.warning(f"⚠️ Warning: Could not test initial connectivity: {e}")
            raise AthenaClientError(f"Connectivity test failed: {e}") from e
