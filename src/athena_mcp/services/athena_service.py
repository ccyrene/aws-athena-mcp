"""
AWS Athena service operations.

This module provides high-level operations for AWS Athena queries and database management.
"""

import asyncio
import logging
from typing import Any, Dict, List

import boto3
from botocore.exceptions import ClientError, NoCredentialsError, PartialCredentialsError
from mcp import types

from ..core.config import config
from ..core.exceptions import (
    AthenaClientError,
    AthenaCredentialsError,
    QueryExecutionError,
    S3ConfigurationError,
)
from ..utils.formatters import AthenaResultFormatter
from ..utils.helpers import (
    create_error_response,
    create_success_response,
    format_aws_error,
    truncate_query_for_log,
)
from ..utils.validators import S3OutputValidator


class AthenaService:
    """Service class for AWS Athena operations."""

    def __init__(self, client: boto3.client, s3_output_location: str):
        """
        Initialize the Athena service.

        Args:
            client: Configured boto3 Athena client
            s3_output_location: S3 location for query results
        """
        self.client = client
        self.s3_output_location = s3_output_location
        self.logger = logging.getLogger(__name__)

    async def list_databases(self) -> List[types.TextContent]:
        """
        List all databases available in Athena.

        Returns:
            List of TextContent with database information

        Raises:
            AthenaClientError: If listing databases fails
        """
        self.logger.info("📚 Listing available databases...")

        try:
            response = self.client.list_databases(CatalogName=config.AWS_DATA_CATALOG)
            databases = response.get("DatabaseList", [])

            if not databases:
                return create_success_response("📚 No databases found.")

            # Format the database list
            db_list = []
            for db in databases:
                db_name = db["Name"]
                description = db.get("Description", "")
                if description:
                    db_list.append(f"• **{db_name}** - {description}")
                else:
                    db_list.append(f"• **{db_name}**")

            result = f"📚 **Available databases ({len(databases)} total):**\n\n"
            result += "\n".join(db_list)

            self.logger.info(f"✅ Listed {len(databases)} databases successfully!")

            return create_success_response(result)

        except ClientError as e:
            error_code = e.response["Error"]["Code"]
            error_message = e.response["Error"]["Message"]
            self.logger.error(f"❌ AWS error listing databases: {error_code} - {error_message}")
            return create_error_response(format_aws_error(error_code, error_message))
        except Exception as e:
            self.logger.error(f"❌ Unexpected error listing databases: {str(e)}")
            return create_error_response(f"❌ Unexpected error listing databases: {str(e)}")

    async def execute_query(
        self, query: str, database: str = config.DEFAULT_DATABASE
    ) -> List[types.TextContent]:
        """
        Execute an Athena query and return formatted results.

        Args:
            query: SQL query to execute
            database: Target database name

        Returns:
            List of TextContent with query results

        Raises:
            S3ConfigurationError: If S3 output location is invalid
            QueryExecutionError: If query execution fails
        """
        truncated_query = truncate_query_for_log(query)
        self.logger.info(f"🔍 Executing query on database '{database}': {truncated_query}")

        # Validate S3 output location
        if not S3OutputValidator.is_valid(self.s3_output_location):
            error_msg = S3OutputValidator.get_error_message(self.s3_output_location)
            return create_error_response(error_msg)

        try:
            # Execute query
            self.logger.info("📤 Sending query to Athena...")
            response = self.client.start_query_execution(
                QueryString=query,
                QueryExecutionContext={"Database": database},
                ResultConfiguration={"OutputLocation": self.s3_output_location},
            )

            query_id = response["QueryExecutionId"]
            self.logger.info(f"📋 Query ID: {query_id}")

            # Wait for completion
            status = await self._wait_for_query_completion(query_id)

            if status == "SUCCEEDED":
                self.logger.info("✅ Query executed successfully!")
                results = self.client.get_query_results(QueryExecutionId=query_id)
                formatted_results = AthenaResultFormatter.format_results(results)

                return create_success_response(
                    f"✅ Query executed successfully:\n\n{formatted_results}"
                )
            else:
                status_response = self.client.get_query_execution(QueryExecutionId=query_id)
                error_reason = status_response["QueryExecution"]["Status"].get(
                    "StateChangeReason", "Unknown error"
                )
                self.logger.error(f"❌ Query failed: {error_reason}")
                raise QueryExecutionError(
                    f"Query failed: {error_reason}", query_id=query_id, error_reason=error_reason
                )

        except QueryExecutionError:
            # Re-raise custom exceptions
            raise
        except ClientError as e:
            error_code = e.response["Error"]["Code"]
            error_message = e.response["Error"]["Message"]
            self.logger.error(f"❌ AWS error: {error_code} - {error_message}")
            return create_error_response(format_aws_error(error_code, error_message))
        except (NoCredentialsError, PartialCredentialsError) as e:
            self.logger.error(f"❌ AWS credentials error: {e}")
            return create_error_response(
                "❌ Error: AWS credentials not found or incomplete. "
                "Configure AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY."
            )
        except Exception as e:
            self.logger.error(f"❌ Unexpected error executing query: {str(e)}")
            return create_error_response(f"❌ Unexpected error executing query: {str(e)}")

    async def describe_database_structure(
        self, database: str = config.DEFAULT_DATABASE
    ) -> List[types.TextContent]:
        """
        Describe the structure of a database by listing its tables.

        Args:
            database: Database name to describe

        Returns:
            List of TextContent with database structure information
        """
        self.logger.info(f"📊 Describing structure of database '{database}'...")

        # Validate S3 output location
        if not S3OutputValidator.is_valid(self.s3_output_location):
            error_msg = S3OutputValidator.get_error_message(self.s3_output_location)
            return create_error_response(error_msg)

        try:
            query = f"SHOW TABLES IN {database}"
            self.logger.info(f"📤 Executing: {query}")
            response = self.client.start_query_execution(
                QueryString=query,
                QueryExecutionContext={"Database": database},
                ResultConfiguration={"OutputLocation": self.s3_output_location},
            )

            query_id = response["QueryExecutionId"]
            self.logger.info(f"📋 Query ID for SHOW TABLES: {query_id}")

            # Wait for completion
            status = await self._wait_for_query_completion(query_id)

            if status == "SUCCEEDED":
                self.logger.info("✅ SHOW TABLES executed successfully!")
                results = self.client.get_query_results(QueryExecutionId=query_id)
                formatted_results = AthenaResultFormatter.format_results(results)

                return create_success_response(
                    f"📊 Tables available in database '{database}':\n\n{formatted_results}"
                )
            else:
                self.logger.error(f"❌ SHOW TABLES failed: {status}")
                return create_error_response(f"❌ Error listing tables: {status}")

        except Exception as e:
            self.logger.error(f"❌ Error describing structure: {str(e)}")
            return create_error_response(f"❌ Error describing structure: {str(e)}")

    async def _wait_for_query_completion(self, query_id: str) -> str:
        """
        Wait for query completion and return final status.

        Args:
            query_id: Athena query execution ID

        Returns:
            str: Final query status
        """
        self.logger.info("⏳ Waiting for query completion...")

        while True:
            status_response = self.client.get_query_execution(QueryExecutionId=query_id)
            status = status_response["QueryExecution"]["Status"]["State"]
            self.logger.debug(f"Current status: {status}")

            if status in ["SUCCEEDED", "FAILED", "CANCELLED"]:
                return status

            await asyncio.sleep(1)
