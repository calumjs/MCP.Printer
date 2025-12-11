#!/usr/bin/env python3
"""
Test script for MCP Label Printer
Run this to verify your printer is working correctly.
"""

from mcp_label_printer.printer import print_label

# Test print
result = print_label(
    url="https://github.com/calumjs/MCP.Printer",
    issue_number="#1",
    title="Test Label",
    description="Printer working!"
)

print(result)

