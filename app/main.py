#!/usr/bin/env python3
"""
Main CLI application entry point.
"""

import argparse
import sys


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
    
    args = parser.parse_args()
    
    if args.verbose:
        print("Verbose mode enabled")
    
    print("Hello from Python CLI!")
    return 0


if __name__ == "__main__":
    sys.exit(main())