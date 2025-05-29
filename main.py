#!/usr/bin/env python3
"""
Entry point for AWS Athena MCP Server.

This is the main entry point that starts the MCP server with the new modular architecture.
"""

import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from athena_mcp.server import main

if __name__ == "__main__":
    main() 