#!/usr/bin/env python3
"""
Utility script to add multiple Codeforces handles to the handles.txt file.
"""

import os
import sys

HANDLES_FILE = "handles.txt"

def add_handles():
    """Add multiple handles to the handles.txt file."""
    print("Enter Codeforces handles (one per line). Press Ctrl+D (Unix) or Ctrl+Z (Windows) when done:")
    
    # Read handles from stdin
    handles = []
    try:
        for line in sys.stdin:
            handle = line.strip()
            if handle:
                handles.append(handle)
    except KeyboardInterrupt:
        print("\nOperation cancelled.")
        return
    
    if not handles:
        print("No handles provided. Exiting.")
        return
    
    # Read existing handles to avoid duplicates
    existing_handles = set()
    if os.path.exists(HANDLES_FILE):
        with open(HANDLES_FILE, "r") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#"):
                    existing_handles.add(line)
    
    # Add new handles
    new_handles = [h for h in handles if h not in existing_handles]
    
    if not new_handles:
        print("All handles already exist in the file. No changes made.")
        return
    
    # Append new handles to the file
    with open(HANDLES_FILE, "a") as f:
        for handle in new_handles:
            f.write(f"{handle}\n")
    
    print(f"Added {len(new_handles)} new handles to {HANDLES_FILE}.")
    print(f"Total handles in file: {len(existing_handles) + len(new_handles)}")

if __name__ == "__main__":
    add_handles() 