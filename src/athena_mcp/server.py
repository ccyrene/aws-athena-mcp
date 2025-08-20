"""
Main AWS Athena MCP Server.

This module contains the main server class that orchestrates all components
and handles the MCP protocol communication.
"""

import asyncio
import logging
from typing import Optional

from mcp import server
from mcp.server import NotificationOptions, Server

from .core.config import config
from .core.exceptions import AthenaClientError, AthenaCredentialsError
from .handlers.tool_handlers import AthenaToolHandlers, get_tool_definitions
from .services.athena_client import AthenaClientFactory, AthenaClientManager
from .services.athena_service import AthenaService
from .utils.helpers import setup_logging


class AthenaMCPServer:
    """Main MCP server class for AWS Athena integration."""

    def __init__(self):
        """Initialize the MCP server."""
        self.server = Server(config.SERVER_NAME)
        self.logger = setup_logging()
        self.athena_service: Optional[AthenaService] = None
        self.tool_handlers: Optional[AthenaToolHandlers] = None

        # Initialize components
        self._initialize_services()
        self._register_handlers()

    def _initialize_services(self) -> None:
        """Initialize the Athena service and related components."""
        self.logger.info("Starting athena-mcp...")

        try:
            # Create Athena client
            athena_client = AthenaClientFactory.create_client()
            client_manager = AthenaClientManager(athena_client)

            # Create Athena service
            self.athena_service = AthenaService(athena_client, config.s3_output_location)

            # Create tool handlers
            self.tool_handlers = AthenaToolHandlers(self.athena_service)

            # Note: Connectivity test will be done when the event loop is running

        except (AthenaClientError, AthenaCredentialsError) as e:
            self.logger.error(f"❌ Failed to initialize Athena services: {e}")
            # Don't raise here to allow server to start and report the error via tools
        except Exception as e:
            self.logger.error(f"❌ Unexpected error during initialization: {e}")

    def _register_handlers(self) -> None:
        """Register MCP server handlers."""

        @self.server.list_tools()
        async def handle_list_tools():
            """Handle list_tools MCP call."""
            return get_tool_definitions()

        @self.server.call_tool()
        async def handle_call_tool(name: str, arguments: dict):
            """Handle call_tool MCP calls."""
            if self.tool_handlers is None:
                self.logger.error("❌ Tool handlers not initialized")
                from .utils.helpers import create_error_response

                return create_error_response(
                    "❌ Error: Server not properly initialized. Check AWS credentials and configuration."
                )

            return await self.tool_handlers.handle_tool_call(name, arguments)

    async def run(self) -> None:
        """Run the MCP server."""
        self.logger.info("🚀 Starting MCP Athena server...")
        try:
            async with server.stdio.stdio_server() as (read_stream, write_stream):
                self.logger.info("📡 Stdio server started, waiting for connections...")
                await self.server.run(
                    read_stream,
                    write_stream,
                    self.server.create_initialization_options()
                )
        except Exception as e:
            self.logger.error(f"❌ Critical server error: {e}")
            import traceback

            self.logger.error(f"❌ Traceback: {traceback.format_exc()}")
            raise


def main() -> None:
    """Main entry point for the application."""
    server = AthenaMCPServer()

    try:
        asyncio.run(server.run())
    except KeyboardInterrupt:
        logging.getLogger("athena-mcp").info("🛑 Server stopped by user")
    except Exception as e:
        logger = logging.getLogger("athena-mcp")
        logger.error(f"❌ Fatal error in main: {e}")
        import traceback

        logger.error(f"❌ Traceback: {traceback.format_exc()}")
        raise


if __name__ == "__main__":
    main()
