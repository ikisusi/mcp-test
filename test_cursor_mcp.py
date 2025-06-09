#!/usr/bin/env python3

import json
import requests
import sys
from pathlib import Path

def test_mcp_connection():
    """Test the MCP connection to the word counter service."""
    # Load MCP configuration
    with open('cursor-mcp.json', 'r') as f:
        config = json.load(f)
    
    base_url = config['transport']['base_url']
    headers = config['transport']['headers']
    endpoint = config['commands']['count']['endpoint']
    
    # Test cases
    test_cases = [
        {
            "name": "Valid file",
            "file_path": "sample.txt",
            "expected_status": 200
        },
        {
            "name": "Invalid API key",
            "file_path": "sample.txt",
            "headers": {"Content-Type": "application/json", "X-API-Key": "wrong-key"},
            "expected_status": 401
        },
        {
            "name": "Missing file",
            "file_path": "nonexistent.txt",
            "expected_status": 500
        },
        {
            "name": "Missing file_path",
            "file_path": None,
            "expected_status": 400
        }
    ]
    
    print("Testing MCP connection to word counter service...")
    print(f"Base URL: {base_url}")
    print("-" * 50)
    
    for test in test_cases:
        print(f"\nTest: {test['name']}")
        
        # Prepare request
        test_headers = test.get('headers', headers)
        body = {"file_path": test['file_path']} if test['file_path'] else {}
        
        try:
            # Make request
            response = requests.post(
                f"{base_url}{endpoint}",
                headers=test_headers,
                json=body
            )
            
            # Check status code
            status_match = response.status_code == test['expected_status']
            print(f"Status: {response.status_code} (Expected: {test['expected_status']})")
            print(f"Status match: {'✓' if status_match else '✗'}")
            
            # Print response
            print("Response:")
            print(json.dumps(response.json(), indent=2))
            
        except requests.exceptions.RequestException as e:
            print(f"Error: {str(e)}")
            print("✗ Connection failed")
        
        print("-" * 50)

def main():
    try:
        test_mcp_connection()
    except Exception as e:
        print(f"Error running tests: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main() 