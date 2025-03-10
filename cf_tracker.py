#!/usr/bin/env python3
"""
Codeforces Rank Tracker - Track changes in Codeforces ranks for a list of handles.
"""

import os
import json
import time
import requests
import hashlib
import random
from datetime import datetime
from tabulate import tabulate
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Constants
API_BASE_URL = "https://codeforces.com/api"
HANDLES_FILE = "handles.txt"
USER_DATA_FILE = "user_data.json"
API_KEY = os.getenv("CODEFORCES_API_KEY")
API_SECRET = os.getenv("CODEFORCES_SECRET")
COLORS = {
    "green": "\033[92m",
    "red": "\033[91m",
    "yellow": "\033[93m",
    "blue": "\033[94m",
    "purple": "\033[95m",
    "cyan": "\033[96m",
    "reset": "\033[0m",
    "bold": "\033[1m",
    "gray": "\033[90m"
}

def load_handles():
    """Load Codeforces handles from the handles file."""
    if not os.path.exists(HANDLES_FILE):
        print(f"Error: {HANDLES_FILE} not found. Creating an empty file.")
        with open(HANDLES_FILE, "w") as f:
            f.write("# Add your students' Codeforces handles below (one per line)\n")
        return []
    
    handles = []
    with open(HANDLES_FILE, "r") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                handles.append(line)
    
    return handles

def load_previous_data():
    """Load previously stored user data."""
    if not os.path.exists(USER_DATA_FILE):
        return {}
    
    try:
        with open(USER_DATA_FILE, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        print(f"Error: {USER_DATA_FILE} is corrupted. Creating a new one.")
        return {}

def save_user_data(data):
    """Save user data to the JSON file."""
    with open(USER_DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

def get_user_info(handles):
    """Fetch user information from Codeforces API."""
    if not handles:
        return {}
    
    # Reduce chunk size to avoid URL length limitations
    # Codeforces API has limitations on URL length
    chunk_size = 20  # Reduced from 100 to 20
    all_user_info = {}
    
    print(f"Processing {len(handles)} handles in chunks of {chunk_size}...")
    
    for i in range(0, len(handles), chunk_size):
        chunk = handles[i:i+chunk_size]
        handles_param = ";".join(chunk)
        
        print(f"Processing handles {i+1}-{min(i+chunk_size, len(handles))} of {len(handles)}...")
        
        try:
            # Basic request without authentication (works for most cases)
            url = f"{API_BASE_URL}/user.info?handles={handles_param}"
            
            # If API key and secret are available, use authenticated request
            if API_KEY and API_SECRET:
                url = create_authenticated_url("user.info", {"handles": handles_param})
            
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            
            if data["status"] == "OK":
                for user in data["result"]:
                    handle = user["handle"]
                    max_rank = user.get("maxRank", "unrated")
                    
                    # Fix for when maxRank is the same as handle (happens with tourist)
                    if max_rank == handle:
                        # Use the current rank or determine based on max rating
                        max_rank = user.get("rank", "unrated")
                        
                        # If max rating is higher than current rating, it's likely legendary grandmaster
                        if user.get("maxRating", 0) >= 3000:
                            max_rank = "legendary grandmaster"
                    
                    all_user_info[handle] = {
                        "handle": handle,
                        "rating": user.get("rating", 0),
                        "rank": user.get("rank", "unrated"),
                        "max_rating": user.get("maxRating", 0),
                        "max_rank": max_rank,
                        "last_updated": datetime.now().isoformat()
                    }
            else:
                print(f"API Error: {data.get('comment', 'Unknown error')}")
            
            # Be nice to the API - increase delay between requests
            time.sleep(2)  # Increased from 1 to 2 seconds
            
        except requests.exceptions.RequestException as e:
            print(f"Request Error: {e}")
            print(f"Failed to process handles: {', '.join(chunk)}")
            # Continue with the next chunk
    
    return all_user_info

def create_authenticated_url(method_name, params=None):
    """Create an authenticated URL for Codeforces API."""
    if not API_KEY or not API_SECRET:
        print("Warning: API key or secret not found. Using unauthenticated request.")
        query_params = "&".join([f"{k}={v}" for k, v in (params or {}).items()])
        return f"{API_BASE_URL}/{method_name}?{query_params}"
    
    if params is None:
        params = {}
    
    # Add authentication parameters
    params["apiKey"] = API_KEY
    params["time"] = str(int(time.time()))
    
    # Generate random string for additional security
    rand = str(random.randint(100000, 999999))
    
    # Create signature string
    param_strings = []
    for key in sorted(params.keys()):
        param_strings.append(f"{key}={params[key]}")
    
    signature_string = f"{rand}/{method_name}?{'&'.join(param_strings)}#{API_SECRET}"
    
    # Calculate SHA512 hash
    signature = hashlib.sha512(signature_string.encode()).hexdigest()
    
    # Build the final URL
    query_params = "&".join([f"{k}={v}" for k, v in params.items()])
    return f"{API_BASE_URL}/{method_name}?{query_params}&apiSig={rand}{signature}"

def compare_data(current_data, previous_data):
    """Compare current and previous data to detect changes."""
    results = []
    
    for handle, current in current_data.items():
        previous = previous_data.get(handle, {})
        
        # Calculate changes
        rating_change = current.get("rating", 0) - previous.get("rating", 0) if previous else 0
        rank_changed = previous and current.get("rank") != previous.get("rank")
        
        # Format the change indicators
        if rating_change > 0:
            rating_change_str = f"{COLORS['green']}+{rating_change}{COLORS['reset']}"
        elif rating_change < 0:
            rating_change_str = f"{COLORS['red']}{rating_change}{COLORS['reset']}"
        else:
            rating_change_str = "0"
        
        rank_indicator = ""
        if rank_changed:
            # Determine if the rank change is an improvement
            rank_order = ["unrated", "newbie", "pupil", "specialist", "expert", "candidate master", 
                         "master", "international master", "grandmaster", "international grandmaster", "legendary grandmaster"]
            
            current_rank_idx = rank_order.index(current.get("rank", "unrated")) if current.get("rank", "unrated") in rank_order else -1
            previous_rank_idx = rank_order.index(previous.get("rank", "unrated")) if previous.get("rank", "unrated") in rank_order else -1
            
            if current_rank_idx > previous_rank_idx:
                rank_indicator = f" {COLORS['green']}↑{COLORS['reset']}"
            elif current_rank_idx < previous_rank_idx:
                rank_indicator = f" {COLORS['red']}↓{COLORS['reset']}"
        
        # Color the rank
        rank_color = get_rank_color(current.get("rank", "unrated"))
        colored_rank = f"{rank_color}{current.get('rank', 'unrated')}{COLORS['reset']}"
        
        results.append({
            "Handle": handle,
            "Rating": current.get("rating", 0),
            "Change": rating_change_str,
            "Rank": colored_rank + rank_indicator,
            "Max Rating": current.get("max_rating", 0),
            "Last Updated": format_date(current.get("last_updated", ""))
        })
    
    # Sort by rating (descending)
    results.sort(key=lambda x: x["Rating"], reverse=True)
    return results

def get_rank_color(rank):
    """Get the color code for a Codeforces rank."""
    rank_colors = {
        "newbie": COLORS["gray"],
        "pupil": COLORS["green"],
        "specialist": COLORS["cyan"],
        "expert": COLORS["blue"],
        "candidate master": COLORS["purple"],
        "master": COLORS["yellow"],
        "international master": COLORS["yellow"],
        "grandmaster": COLORS["red"],
        "international grandmaster": COLORS["red"],
        "legendary grandmaster": COLORS["red"]
    }
    
    return rank_colors.get(rank.lower(), COLORS["reset"])

def format_date(iso_date):
    """Format ISO date string to a more readable format."""
    try:
        dt = datetime.fromisoformat(iso_date)
        return dt.strftime("%Y-%m-%d %H:%M")
    except (ValueError, TypeError):
        return "N/A"

def main():
    """Main function to run the Codeforces rank tracker."""
    print(f"{COLORS['bold']}Codeforces Rank Tracker{COLORS['reset']}")
    print("Loading handles...")
    handles = load_handles()
    
    if not handles:
        print(f"No handles found in {HANDLES_FILE}. Please add some handles and try again.")
        return
    
    print(f"Found {len(handles)} handles. Fetching data from Codeforces API...")
    
    # Load previous data
    previous_data = load_previous_data()
    
    # Get current data
    current_data = get_user_info(handles)
    
    if not current_data:
        print("Failed to fetch data from Codeforces API. Please try again later.")
        return
    
    # Compare and display results
    results = compare_data(current_data, previous_data)
    
    print("\nResults:")
    print(tabulate(results, headers="keys", tablefmt="pretty"))
    
    # Save current data for future comparison
    save_user_data(current_data)
    print(f"\nData saved to {USER_DATA_FILE}")

if __name__ == "__main__":
    main() 