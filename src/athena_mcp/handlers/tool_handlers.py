"""
MCP tool handlers for AWS Athena operations.

This module contains the handlers for Model Context Protocol tool calls.
"""

import logging
from typing import Any, Dict, List

from mcp import types

from ..core.config import config
from ..core.exceptions import ToolNotFoundError
from ..services.athena_service import AthenaService
from ..utils.helpers import create_error_response


class AthenaToolHandlers:
    """Handler class for Athena MCP tools."""

    def __init__(self, athena_service: AthenaService):
        """
        Initialize the tool handlers.

        Args:
            athena_service: Configured Athena service instance
        """
        self.athena_service = athena_service
        self.logger = logging.getLogger(__name__)

    async def handle_tool_call(
        self, name: str, arguments: Dict[str, Any]
    ) -> List[types.TextContent]:
        """
        Route tool calls to appropriate handlers.

        Args:
            name: Tool name
            arguments: Tool arguments

        Returns:
            List of TextContent responses

        Raises:
            ToolNotFoundError: If the requested tool is not found
        """
        self.logger.info(f"📞 Calling tool: {name} with arguments: {arguments}")

        if self.athena_service is None:
            self.logger.error("❌ Athena service is not available")
            return create_error_response(
                "❌ Error: Athena service not configured. Check AWS credentials."
            )

        # Route to specific handlers
        if name == "list_databases":
            return await self.handle_list_databases()
        elif name == "query_athena":
            return await self.handle_query_athena(arguments)
        elif name == "describe_data_structure":
            return await self.handle_describe_data_structure(arguments)
        else:
            self.logger.error(f"❌ Tool not found: {name}")
            raise ToolNotFoundError(name)

    async def handle_list_databases(self) -> List[types.TextContent]:
        """
        Handle list_databases tool call.

        Returns:
            List of TextContent with database information
        """
        return await self.athena_service.list_databases()

    async def handle_query_athena(self, arguments: Dict[str, Any]) -> List[types.TextContent]:
        """
        Handle query_athena tool call.

        Args:
            arguments: Tool arguments containing query and optional database

        Returns:
            List of TextContent with query results
        """
        query = arguments["query"]
        database = arguments.get("database", config.DEFAULT_DATABASE)

        return await self.athena_service.execute_query(query, database)

    async def handle_describe_data_structure(
        self, arguments: Dict[str, Any]
    ) -> List[types.TextContent]:
        """
        Handle describe_data_structure tool call.

        Args:
            arguments: Tool arguments containing optional database

        Returns:
            List of TextContent with database structure information
        """
        database = arguments.get("database", config.DEFAULT_DATABASE)

        return await self.athena_service.describe_database_structure(database)


def get_tool_definitions() -> List[types.Tool]:
    """
    Get the list of available MCP tools.

    Returns:
        List of Tool definitions
    """
    return [
        types.Tool(
            name="list_databases",
            description="List all available databases in AWS Athena",
            inputSchema={"type": "object", "properties": {}},
        ),
        types.Tool(
            name="query_athena",
            description="Execute SQL queries on AWS Athena for semi-structured data",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "SQL query to execute"},
                    "database": {
                        "type": "string",
                        "description": "Athena database name",
                        "default": config.DEFAULT_DATABASE,
                    },
                },
                "required": ["query"],
            },
        ),
        types.Tool(
            name="describe_data_structure",
            description="Get information about available tables and their structure",
            inputSchema={
                "type": "object",
                "properties": {
                    "database": {
                        "type": "string",
                        "description": "Database to explore",
                        "default": config.DEFAULT_DATABASE,
                    }
                },
            },
        ),
    ]
