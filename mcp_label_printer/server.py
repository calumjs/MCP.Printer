#!/usr/bin/env python3
"""
MCP Label Printer Server
Prints labels with QR codes to Brother QL-810W via P-touch Editor Lite
"""

import asyncio
import json
from typing import Any
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

from .printer import print_label

# Create MCP server
server = Server("label-printer")


@server.list_tools()
async def list_tools() -> list[Tool]:
    """List available tools."""
    return [
        Tool(
            name="print_label",
            description="Print a label with QR code and text to Brother QL-810W printer. The QR code links to the provided URL, and text shows issue details.",
            inputSchema={
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "URL to encode in QR code (e.g., issue/PR link)"
                    },
                    "issue_number": {
                        "type": "string",
                        "description": "Issue/PR number (e.g., '#1234')"
                    },
                    "title": {
                        "type": "string",
                        "description": "Issue/PR title"
                    },
                    "description": {
                        "type": "string",
                        "description": "Brief description (optional)",
                        "default": ""
                    }
                },
                "required": ["url", "issue_number", "title"]
            }
        )
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict[str, Any]) -> list[TextContent]:
    """Handle tool calls."""
    if name != "print_label":
        return [TextContent(type="text", text=f"Unknown tool: {name}")]
    
    try:
        result = print_label(
            url=arguments["url"],
            issue_number=arguments["issue_number"],
            title=arguments["title"],
            description=arguments.get("description", "")
        )
        return [TextContent(type="text", text=result)]
    except Exception as e:
        return [TextContent(type="text", text=f"Error printing label: {str(e)}")]


async def main():
    """Run the MCP server."""
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


def run():
    """Entry point."""
    asyncio.run(main())


if __name__ == "__main__":
    run()

