# Word Counter

A Python CLI application that counts lines, words, and characters in text files. Supports both direct file analysis and MCP server modes with stdin or HTTP transport.

## Setup

1. Create and activate the virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Unix/macOS
# or
.\venv\Scripts\activate  # On Windows
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Direct File Analysis
```bash
python word_counter.py path/to/file.txt
```

### MCP Server with Stdin Transport
```bash
python word_counter.py --mcp-server-stdin
```

### MCP Server with HTTP Transport
```bash
python word_counter.py --mcp-server-http --api-key your-secret-key
```

To make requests to the HTTP server:
```bash
curl -X POST \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-secret-key" \
  -d '{"file_path": "path/to/file.txt"}' \
  http://localhost:5000/count
```

## Response Format

The application returns JSON responses in the following format:

Success:
```json
{
  "result": {
    "lines": 10,
    "words": 46,
    "characters": 247
  }
}
```

Error:
```json
{
  "error": "error message here"
}
``` 