# Using Word Counter with Cursor MCP

This document explains how to use the Word Counter service with Cursor's MCP (Machine Control Protocol) integration.

## Prerequisites

1. Python 3.x installed
2. Cursor IDE installed
3. Required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

## Setup

1. Start the Word Counter service:
   ```bash
   python word_counter.py --mcp-server-http --api-key test-key-123
   ```
   The service will start on `http://localhost:55000`.

2. The MCP configuration file is located in the `.cursor` directory as `mcp.json`. It is already configured with:
   - Base URL: `http://localhost:55000`
   - API Key: `test-key-123`
   - Endpoint: `/count`

## Testing the Integration

Run the test script to verify the MCP integration:
```bash
python test_cursor_mcp.py
```

This will test:
- Valid file analysis
- Invalid API key handling
- Missing file handling
- Missing file_path handling

## Using in Cursor

### Basic Usage

1. Open a text file in Cursor
2. The MCP integration will be available through Cursor's command palette
3. Use the "Count Words" command to analyze the current file

### Available Commands

- `count`: Analyzes a text file and returns:
  - Number of lines
  - Number of words
  - Number of characters

### Example Response

```json
{
  "result": {
    "lines": 10,
    "words": 46,
    "characters": 247
  }
}
```

### Error Handling

The service returns appropriate error responses:
- 400: Bad Request (missing or invalid file_path)
- 401: Unauthorized (invalid or missing API key)
- 500: Internal Server Error (file not found or other errors)

## Configuration

The `cursor-mcp.json` file can be modified to:
- Change the server URL
- Update the API key
- Add new commands
- Modify request/response schemas

## Troubleshooting

1. **Service not responding**
   - Check if the service is running
   - Verify the port (55000) is not in use
   - Check the API key matches

2. **Invalid responses**
   - Verify the file path is correct
   - Check file permissions
   - Ensure the file is a text file

3. **Authentication errors**
   - Verify the API key in `cursor-mcp.json`
   - Check the service is running with the correct API key

## Security Notes

- The API key is stored in plain text in `cursor-mcp.json`
- For production use, consider:
  - Using environment variables for the API key
  - Implementing proper authentication
  - Using HTTPS
  - Setting up proper access controls 