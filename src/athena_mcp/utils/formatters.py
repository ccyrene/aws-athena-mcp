"""
Formatting utilities for AWS Athena MCP Server.

This module contains formatting functions for various outputs and data structures.
"""

from typing import Any, Dict

from ..core.config import config


class AthenaResultFormatter:
    """Utility class for formatting Athena query results."""

    @staticmethod
    def format_results(results: Dict[str, Any]) -> str:
        """
        Format Athena results into a readable table.

        Args:
            results: Raw Athena query results

        Returns:
            str: Formatted table string
        """
        rows = results["ResultSet"]["Rows"]

        if not rows:
            return "No results found"

        # First row contains headers
        headers = [col.get("VarCharValue", "") for col in rows[0]["Data"]]

        # Remaining rows contain data
        data_rows = []
        for row in rows[1:]:
            data_rows.append([col.get("VarCharValue", "") for col in row["Data"]])

        # Create formatted table
        result = "| " + " | ".join(headers) + " |\n"
        result += "| " + " | ".join(["---"] * len(headers)) + " |\n"

        for row in data_rows[: config.MAX_DISPLAY_ROWS]:
            result += "| " + " | ".join(row) + " |\n"

        if len(data_rows) > config.MAX_DISPLAY_ROWS:
            result += f"\n... and {len(data_rows) - config.MAX_DISPLAY_ROWS} more rows"

        return result

    @staticmethod
    def format_database_list(databases: list) -> str:
        """
        Format a list of databases into a readable format.

        Args:
            databases: List of database dictionaries from AWS response

        Returns:
            str: Formatted database list
        """
        if not databases:
            return "📚 No databases found."

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

        return result

    @staticmethod
    def format_error_summary(error_code: str, error_message: str, context: str = None) -> str:
        """
        Format error information into a standardized error message.

        Args:
            error_code: AWS error code
            error_message: AWS error message
            context: Optional context information

        Returns:
            str: Formatted error message
        """
        base_message = f"❌ AWS error ({error_code}): {error_message}"

        if context:
            base_message += f"\n\nContext: {context}"

        return base_message
