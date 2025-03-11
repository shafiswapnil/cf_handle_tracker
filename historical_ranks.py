#!/usr/bin/env python3

import os
import sys
import json
import time
import hashlib
import random
import requests
from datetime import datetime
import calendar
from dotenv import load_dotenv
from tabulate import tabulate
import urllib.parse

# Load environment variables from .env file
load_dotenv()

# Constants
API_KEY = os.getenv("CODEFORCES_API_KEY")
SECRET = os.getenv("CODEFORCES_SECRET")
HANDLES_FILE = "handles.txt"

# ANSI color codes for different ranks
RANK_COLORS = {
    "newbie": "\033[90m",  # Gray
    "pupil": "\033[92m",  # Green
    "specialist": "\033[96m",  # Cyan
    "expert": "\033[94m",  # Blue
    "candidate master": "\033[95m",  # Purple
    "master": "\033[93m",  # Yellow
    "international master": "\033[93m",  # Yellow
    "grandmaster": "\033[91m",  # Red
    "international grandmaster": "\033[91m",  # Red
    "legendary grandmaster": "\033[91m",  # Red
}
RESET_COLOR = "\033[0m"  # Reset color

def create_authenticated_url(method_name, params=None):
    """Create an authenticated URL for the Codeforces API."""
    if params is None:
        params = {}
    
    if not API_KEY or not SECRET:
        # If API credentials are not available, return a non-authenticated URL
        base_url = f"https://codeforces.com/api/{method_name}"
        if params:
            query_string = "&".join([f"{k}={urllib.parse.quote(str(v))}" for k, v in params.items()])
            return f"{base_url}?{query_string}"
        return base_url
    
    # Add authentication parameters
    unix_time = int(time.time())
    params["apiKey"] = API_KEY
    params["time"] = unix_time
    
    # Create a random string for the API signature
    rand = random.randint(100000, 999999)
    
    # Create the API signature
    sorted_params = sorted(params.items())
    signature_string = f"{rand}/{method_name}?"
    signature_string += "&".join([f"{k}={urllib.parse.quote(str(v))}" for k, v in sorted_params])
    signature_string += f"#{SECRET}"
    
    # Calculate the API signature
    signature = hashlib.sha512(signature_string.encode()).hexdigest()
    
    # Create the final URL
    base_url = f"https://codeforces.com/api/{method_name}"
    query_string = "&".join([f"{k}={urllib.parse.quote(str(v))}" for k, v in params.items()])
    query_string += f"&apiSig={rand}{signature}"
    
    return f"{base_url}?{query_string}"

def get_rating_history(handle):
    """Get the rating history for a user."""
    url = create_authenticated_url("user.rating", {"handle": handle})
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        if data["status"] == "OK":
            return data["result"]
        else:
            print(f"Error fetching rating history for {handle}: {data.get('comment', 'Unknown error')}")
            return []
    except requests.exceptions.RequestException as e:
        print(f"Request Error: {e}")
        # Try individual request without authentication as fallback
        try:
            fallback_url = f"https://codeforces.com/api/user.rating?handle={urllib.parse.quote(handle)}"
            response = requests.get(fallback_url)
            response.raise_for_status()
            data = response.json()
            
            if data["status"] == "OK":
                return data["result"]
            else:
                print(f"Error fetching rating history for {handle}: {data.get('comment', 'Unknown error')}")
                return []
        except requests.exceptions.RequestException as e2:
            print(f"Fallback Request Error: {e2}")
            return []

def get_rank_from_rating(rating):
    """Get the rank name based on the rating."""
    if rating < 1200:
        return "newbie"
    elif rating < 1400:
        return "pupil"
    elif rating < 1600:
        return "specialist"
    elif rating < 1900:
        return "expert"
    elif rating < 2100:
        return "candidate master"
    elif rating < 2300:
        return "master"
    elif rating < 2400:
        return "international master"
    elif rating < 2600:
        return "grandmaster"
    elif rating < 3000:
        return "international grandmaster"
    else:
        return "legendary grandmaster"

def colorize_rank(rank):
    """Add color to a rank string."""
    rank_lower = rank.lower()
    color = RANK_COLORS.get(rank_lower, "")
    return f"{color}{rank}{RESET_COLOR}"

def find_closest_rating(rating_history, target_date):
    """Find the rating closest to the target date."""
    if not rating_history:
        return None
    
    target_timestamp = int(target_date.timestamp())
    
    # Sort by time difference to target date
    closest = min(rating_history, key=lambda x: abs(x["ratingUpdateTimeSeconds"] - target_timestamp))
    
    # Check if the closest rating is within 3 months of the target date
    time_diff = abs(closest["ratingUpdateTimeSeconds"] - target_timestamp)
    if time_diff > 7776000:  # 90 days in seconds
        return None
    
    return closest

def get_historical_ratings(handle, years):
    """Get historical ratings for a handle for specific months in different years."""
    rating_history = get_rating_history(handle)
    if not rating_history:
        return None
    
    results = []
    
    for year in years:
        # Create a date object for March 15 of the specified year
        target_date = datetime(year, 3, 15)
        closest_rating = find_closest_rating(rating_history, target_date)
        
        if closest_rating:
            rating = closest_rating["newRating"]
            rank = get_rank_from_rating(rating)
            contest_date = datetime.fromtimestamp(closest_rating["ratingUpdateTimeSeconds"])
            
            results.append({
                "year": year,
                "rating": rating,
                "rank": rank,
                "contest_date": contest_date.strftime("%Y-%m-%d")
            })
        else:
            results.append({
                "year": year,
                "rating": None,
                "rank": None,
                "contest_date": None
            })
    
    return results

def load_handles():
    """Load handles from the handles file."""
    if not os.path.exists(HANDLES_FILE):
        print(f"Error: {HANDLES_FILE} not found.")
        return []
    
    with open(HANDLES_FILE, "r") as f:
        handles = [line.strip() for line in f if line.strip() and not line.strip().startswith("#")]
    
    return handles

def main():
    """Main function."""
    if len(sys.argv) > 1:
        handles = [handle.strip() for handle in sys.argv[1:]]
    else:
        handles = load_handles()
    
    if not handles:
        print("No handles provided. Please add handles to handles.txt or provide them as command-line arguments.")
        return
    
    # Target years for March
    years = [2022, 2023, 2024]
    
    table_data = []
    
    for handle in handles:
        print(f"Fetching historical data for {handle}...")
        historical_data = get_historical_ratings(handle, years)
        
        if historical_data:
            row = [handle]
            
            for data in historical_data:
                if data["rating"] is not None:
                    rank_display = colorize_rank(data["rank"].title())
                    row.append(f"{data['rating']} ({rank_display})")
                    row.append(data["contest_date"])
                else:
                    row.append("N/A")
                    row.append("N/A")
            
            table_data.append(row)
        else:
            row = [handle] + ["N/A", "N/A"] * len(years)
            table_data.append(row)
        
        # Add a small delay to avoid hitting API rate limits
        time.sleep(1)
    
    # Create headers for the table
    headers = ["Handle"]
    for year in years:
        headers.extend([f"March {year}", "Contest Date"])
    
    # Print the table
    print("\nHistorical Codeforces Ratings for March:")
    print(tabulate(table_data, headers=headers, tablefmt="grid"))

if __name__ == "__main__":
    main() 