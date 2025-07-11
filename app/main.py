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
        help="HackerOne report ID to fetch"
    )
    parser.add_argument(
        "--output",
        "-o",
        help="Output file path to save JSON result"
    )
    
    args = parser.parse_args()
    
    verbose = args.verbose or os.environ.get("VERBOSE")
    if verbose:
        print("Verbose mode enabled")

    res = requests.get(f'https://hackerone.com/reports/{args.report}.json')
    if res.status_code == 200:
        json_data = res.json()
        formatted_json = json.dumps(json_data, indent=2)
        
        if args.output:
            # Save to file
            with open(args.output, 'w') as f:
                f.write(formatted_json)
            if verbose:
                print(f"Report saved to {args.output}")
        else:
            # Print to stdout (existing behavior)
            print(formatted_json)
    else:
        print("Failed to fetch report")
        if verbose:
            print('Response:' + res.text)
    return 0


if __name__ == "__main__":
    sys.exit(main())