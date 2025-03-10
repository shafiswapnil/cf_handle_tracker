#!/usr/bin/env python3
"""
Utility script to export Codeforces user data to CSV format.
"""

import os
import json
import csv
from datetime import datetime

USER_DATA_FILE = "user_data.json"
CSV_OUTPUT_FILE = "codeforces_ranks.csv"

def export_to_csv():
    """Export user data from JSON to CSV format."""
    if not os.path.exists(USER_DATA_FILE):
        print(f"Error: {USER_DATA_FILE} not found. Run cf_tracker.py first.")
        return
    
    try:
        with open(USER_DATA_FILE, "r") as f:
            user_data = json.load(f)
    except json.JSONDecodeError:
        print(f"Error: {USER_DATA_FILE} is corrupted.")
        return
    
    if not user_data:
        print("No user data found.")
        return
    
    # Prepare data for CSV
    csv_data = []
    for handle, data in user_data.items():
        csv_data.append({
            "Handle": handle,
            "Rating": data.get("rating", 0),
            "Rank": data.get("rank", "unrated"),
            "Max Rating": data.get("max_rating", 0),
            "Max Rank": data.get("max_rank", "unrated"),
            "Last Updated": data.get("last_updated", "")
        })
    
    # Sort by rating (descending)
    csv_data.sort(key=lambda x: x["Rating"], reverse=True)
    
    # Write to CSV
    with open(CSV_OUTPUT_FILE, "w", newline="") as f:
        fieldnames = ["Handle", "Rating", "Rank", "Max Rating", "Max Rank", "Last Updated"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        
        writer.writeheader()
        for row in csv_data:
            writer.writerow(row)
    
    print(f"Data exported to {CSV_OUTPUT_FILE}")
    print(f"Total records: {len(csv_data)}")

if __name__ == "__main__":
    export_to_csv() 