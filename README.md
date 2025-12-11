# MCP Label Printer

An MCP server for printing labels with QR codes to Brother QL-810W printer via P-touch Editor Lite.

## Prerequisites

- **Python 3.10+** - [Download](https://www.python.org/downloads/)
- **Brother QL-810W** printer connected via USB
- **Editor Lite mode enabled** on printer (green LED on)

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/calumjs/MCP.Printer.git
   cd MCP.Printer
   ```

2. **Install the package:**
   ```bash
   pip install -e .
   ```

   This installs all dependencies (Pillow, qrcode, brother_ql, mcp).

3. **Verify installation:**
   ```bash
   python -c "from mcp_label_printer.printer import print_label; print('OK')"
   ```

## Printer Setup

1. Connect Brother QL-810W via USB
2. Press the **Editor Lite button** until the green LED turns ON
3. The printer should appear as a USB drive (usually `D:\`)
4. Verify `D:\PTLITE.PRN` exists

## MCP Configuration

Add to your MCP config file:

**For Cursor** (`~/.cursor/mcp.json`):
```json
{
  "mcpServers": {
    "label-printer": {
      "command": "mcp-label-printer"
    }
  }
}
```

**Alternative** (if command not found):
```json
{
  "mcpServers": {
    "label-printer": {
      "command": "python",
      "args": ["-m", "mcp_label_printer.server"]
    }
  }
}
```

Restart your IDE after adding the config.

## Usage

The server exposes one tool:

### `print_label`

Print a label with QR code and text.

| Parameter | Required | Description |
|-----------|----------|-------------|
| `url` | Yes | URL to encode in QR code |
| `issue_number` | Yes | Issue/PR number (e.g., "#1234") |
| `title` | Yes | Issue/PR title |
| `description` | No | Brief description |

**Example prompt:**
> Print a label for issue #42 "Fix login bug" with URL https://github.com/org/repo/issues/42

## How It Works

1. Generates a QR code from the URL
2. Creates a label image with QR code + text
3. Converts to Brother QL raster format
4. Writes to `D:\PTLITE.PRN` with proper padding (112,640 bytes)
5. Printer automatically prints when file is written

## Troubleshooting

**Nothing prints:**
- Ensure Editor Lite LED is ON (green)
- Check `D:\` drive exists and contains `PTLITE.PRN`
- Try printing from P-touch Editor Lite app to verify printer works

**Command not found:**
- Ensure Python Scripts folder is in PATH
- Use the alternative config with `python -m mcp_label_printer.server`

**Wrong label size:**
- This is configured for 62mm continuous labels (DK-22205)
