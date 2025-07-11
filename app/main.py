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
        help="Enable verbose output"
    )
    
    args = parser.parse_args()
    
    verbose = args.verbose or os.environ.get("VERBOSE")
    if verbose:
        print("Verbose mode enabled")

    res = requests.get(f'https://hackerone.com/reports/{args.report}.json')
    if res.status_code == 200:
        result_data = res.json()
        formatted_json = json.dumps(result_data, indent=2)
        print(formatted_json)
        
        # Save result to res.json in current directory
        with open('res.json', 'w') as f:
            f.write(formatted_json)
        
        if verbose:
            print("Result saved to res.json")
    else:
        print("Failed to fetch report")
        if verbose:
            print('Response:' + res.text)
    return 0


if __name__ == "__main__":
    sys.exit(main())