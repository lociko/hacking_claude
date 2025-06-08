#!/usr/bin/env python3
"""
Main CLI application entry point.
"""

import argparse
import json
import os
import sys
import requests


def main():
    """Main CLI function."""
    parser = argparse.ArgumentParser(description="Python CLI Application")
    parser.add_argument(
        "--version", 
        action="version", 
        version="%(prog)s 1.0.0"
    )
    parser.add_argument(
        "--verbose", 
        "-v", 
        action="store_true", 
        help="Enable verbose output"
    )
    parser.add_argument(
        "--report",
        "-r",
        help="Report ID to fetch"
    )
    
    args = parser.parse_args()
    
    verbose = args.verbose or os.environ.get("VERBOSE")
    if verbose:
        print("Verbose mode enabled")
        # Print environment variables used for debugging
        print(f"Environment variables:")
        print(f"  VERBOSE: {os.environ.get('VERBOSE', 'Not set')}")
        print(f"  H1_API_TOKEN: {'Set' if os.environ.get('H1_API_TOKEN') else 'Not set'}")

    # Check if report ID is provided
    if not args.report:
        print("Error: --report argument is required")
        return 1

    # Prepare headers
    headers = {}
    api_token = os.environ.get('H1_API_TOKEN')
    if api_token:
        headers['API_TOKEN'] = api_token

    try:
        res = requests.get(f'https://hackerone.com/reports/{args.report}.json', headers=headers)
        if res.status_code == 200:
            print(json.dumps(res.json(),indent=2))
        else:
            print("Failed to fetch report")
            if verbose:
                print('Response:' + res.text)
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())