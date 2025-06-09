#!/usr/bin/env python3

import json
import sys
import argparse
from pathlib import Path
from typing import Dict, Any
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
API_KEY = None
DEFAULT_PORT = 55000  # Changed from 5000 to avoid AirPlay conflicts

# Register routes
@app.route('/', methods=['GET', 'POST'])
def root():
    return jsonify({
        "mcpServers": {
            "word-counter": {
                "name": "word-counter",
                "version": "1.0.0",
                "description": "Cursor MCP client configuration for word counter service",
                "url": "http://localhost:55000",
                "transport": {
                    "type": "http",
                    "base_url": "http://localhost:55000",
                    "headers": {
                        "Content-Type": "application/json",
                        "X-API-Key": "test-key-123"
                    }
                },
                "commands": {
                    "count": {
                        "endpoint": "/count",
                        "method": "POST",
                        "description": "Count lines, words, and characters in a text file",
                        "request_schema": {
                            "type": "object",
                            "required": ["file_path"],
                            "properties": {
                                "file_path": {
                                    "type": "string",
                                    "description": "Path to the text file to analyze"
                                }
                            }
                        },
                        "response_schema": {
                            "type": "object",
                            "properties": {
                                "result": {
                                    "type": "object",
                                    "properties": {
                                        "lines": {
                                            "type": "integer",
                                            "description": "Number of lines in the file"
                                        },
                                        "words": {
                                            "type": "integer",
                                            "description": "Number of words in the file"
                                        },
                                        "characters": {
                                            "type": "integer",
                                            "description": "Number of characters in the file"
                                        }
                                    }
                                },
                                "error": {
                                    "type": "string",
                                    "description": "Error message if the request failed"
                                }
                            }
                        }
                    }
                }
            }
        }
    })

@app.route('/count', methods=['POST'])
def count():
    # Check API key if set
    if API_KEY:
        auth_header = request.headers.get('X-API-Key')
        if not auth_header or auth_header != API_KEY:
            return jsonify({'error': 'Invalid API key'}), 401

    # Get request data
    data = request.get_json()
    if not data or 'file_path' not in data:
        return jsonify({'error': 'Missing file_path in request'}), 400

    try:
        stats = count_file_stats(data['file_path'])
        return jsonify({'result': stats})
    except FileNotFoundError as fnf:
        return jsonify({'error': str(fnf)}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def count_file_stats(file_path: str) -> Dict[str, int]:
    """
    Count the number of lines, words, and characters in a text file.
    
    Args:
        file_path (str): Path to the text file
        
    Returns:
        Dict[str, int]: Dictionary containing the counts
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            
        stats = {
            'lines': len(content.splitlines()),
            'words': len(content.split()),
            'characters': len(content)
        }
        
        return stats
    except FileNotFoundError:
        raise FileNotFoundError(f"File '{file_path}' not found")
    except Exception as e:
        raise Exception(str(e))

def run_mcp_server():
    """
    Run the word counter as an MCP server using stdin as transport.
    """
    while True:
        try:
            # Read the input line
            line = sys.stdin.readline()
            if not line:
                break
                
            # Parse the input as JSON
            request = json.loads(line)
            
            # Check if the request has a file_path
            if 'file_path' not in request:
                response = {
                    'error': 'Missing file_path in request'
                }
            else:
                try:
                    # Process the file and get stats
                    stats = count_file_stats(request['file_path'])
                    response = {
                        'result': stats
                    }
                except FileNotFoundError as fnf:
                    response = {'error': str(fnf)}
                except Exception as e:
                    response = {'error': str(e)}
            
            # Send the response
            print(json.dumps(response))
            sys.stdout.flush()
            
        except json.JSONDecodeError:
            response = {
                'error': 'Invalid JSON input'
            }
            print(json.dumps(response))
            sys.stdout.flush()
        except Exception as e:
            response = {
                'error': str(e)
            }
            print(json.dumps(response))
            sys.stdout.flush()

def run_http_server():
    """
    Run the word counter as an HTTP server.
    """
    # Run the Flask app
    app.run(host='0.0.0.0', port=DEFAULT_PORT, debug=True)

def main():
    parser = argparse.ArgumentParser(description='Count lines, words, and characters in a text file')
    parser.add_argument('--mcp-server-stdin', action='store_true',
                      help='Run as MCP server using stdin as transport')
    parser.add_argument('--mcp-server-http', action='store_true',
                      help='Run as MCP server using HTTP transport')
    parser.add_argument('--api-key',
                      help='API key for HTTP server authentication')
    parser.add_argument('--port', type=int, default=DEFAULT_PORT,
                      help=f'Port for HTTP server (default: {DEFAULT_PORT})')
    parser.add_argument('file_path', nargs='?',
                      help='Path to the text file to analyze')
    
    args = parser.parse_args()
    
    if args.mcp_server_stdin:
        run_mcp_server()
    elif args.mcp_server_http:
        global API_KEY
        API_KEY = args.api_key
        run_http_server()
    else:
        if not args.file_path:
            parser.print_help()
            sys.exit(1)
            
        stats = count_file_stats(args.file_path)
        print(json.dumps(stats, indent=2))

if __name__ == "__main__":
    main() 