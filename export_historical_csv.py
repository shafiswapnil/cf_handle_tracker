#!/usr/bin/env python3

import os
import sys
import csv
import time
from datetime import datetime
from historical_ranks import load_handles, get_historical_ratings, colorize_rank

# Constants
OUTPUT_FILE = "historical_codeforces_ranks.csv"
YEARS = [2022, 2023, 2024]  # Target years for March

def strip_ansi_codes(text):
    """Remove ANSI color codes from text."""
    import re
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    return ansi_escape.sub('', text)

def main():
    """Main function."""
    if len(sys.argv) > 1:
        handles = [handle.strip() for handle in sys.argv[1:]]
    else:
        handles = load_handles()
    
    if not handles:
        print("No handles provided. Please add handles to handles.txt or provide them as command-line arguments.")
        return
    
    # Prepare data for CSV
    csv_data = []
    
    # Create headers
    headers = ["Handle"]
    for year in YEARS:
        headers.extend([f"March {year} Rating", f"March {year} Rank", f"March {year} Contest Date"])
    
    csv_data.append(headers)
    
    # Process each handle
    for i, handle in enumerate(handles):
        print(f"Processing handle {i+1}/{len(handles)}: {handle}")
        
        historical_data = get_historical_ratings(handle, YEARS)
        
        if historical_data:
            row = [handle]
            
            for data in historical_data:
                if data["rating"] is not None:
                    row.append(data["rating"])
                    row.append(strip_ansi_codes(data["rank"].title()))
                    row.append(data["contest_date"])
                else:
                    row.append("")
                    row.append("")
                    row.append("")
            
            csv_data.append(row)
        else:
            # If no data is available, add empty cells
            row = [handle] + ["", "", ""] * len(YEARS)
            csv_data.append(row)
        
        # Add a small delay to avoid hitting API rate limits
        time.sleep(1)
    
    # Write to CSV file
    with open(OUTPUT_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(csv_data)
    
    print(f"\nHistorical data exported to {OUTPUT_FILE}")
    print(f"Total handles processed: {len(handles)}")

if __name__ == "__main__":
    main() 