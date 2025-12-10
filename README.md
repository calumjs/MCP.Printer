# MCP Label Printer

An MCP server for printing labels with QR codes to Brother QL-810W printer via P-touch Editor Lite.

## Requirements

- Brother QL-810W printer connected via USB
- **Editor Lite mode enabled** (green LED on)
- Windows with P-touch Editor Lite drive mounted (D:\)

## Installation

```bash
pip install -e .
```

## MCP Configuration

Add to your MCP config (e.g., `~/.cursor/mcp.json`):

```json
{
  "mcpServers": {
    "label-printer": {
      "command": "mcp-label-printer"
    }
  }
}
```

## Usage

The server exposes one tool:

### `print_label`

Print a label with QR code and text.

**Parameters:**
- `url` (required): URL to encode in QR code
- `issue_number` (required): Issue/PR number (e.g., "#1234")
- `title` (required): Issue/PR title
- `description` (optional): Brief description

**Example:**
```
Print a label for issue #1234 "Fix login bug" with URL https://github.com/org/repo/issues/1234
```

## How It Works

1. Generates a QR code from the URL
2. Creates a label image with QR code + text
3. Converts to Brother QL raster format
4. Writes to `D:\PTLITE.PRN` (P-touch Editor Lite print file)
5. Printer automatically prints when file is written
