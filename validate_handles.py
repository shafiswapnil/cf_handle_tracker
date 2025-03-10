#!/usr/bin/env python3
"""
Utility script to validate Codeforces handles before adding them to the handles.txt file.
"""

import os
import sys
import requests
import time
import hashlib
import random
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

HANDLES_FILE = "handles.txt"
API_BASE_URL = "https://codeforces.com/api"
API_KEY = os.getenv("CODEFORCES_API_KEY")
API_SECRET = os.getenv("CODEFORCES_SECRET")

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

def validate_handles():
    """Validate Codeforces handles and add valid ones to the handles.txt file."""
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
    
    # Filter out handles that already exist
    new_handles = [h for h in handles if h not in existing_handles]
    
    if not new_handles:
        print("All handles already exist in the file. No changes made.")
        return
    
    print(f"Validating {len(new_handles)} new handles...")
    
    # Validate handles with the Codeforces API
    valid_handles = []
    invalid_handles = []
    
    # Process handles in chunks to avoid API rate limits and URL length limitations
    chunk_size = 20  # Reduced from 100 to 20
    
    print(f"Processing {len(new_handles)} handles in chunks of {chunk_size}...")
    
    for i in range(0, len(new_handles), chunk_size):
        chunk = new_handles[i:i+chunk_size]
        handles_param = ";".join(chunk)
        
        print(f"Processing handles {i+1}-{min(i+chunk_size, len(new_handles))} of {len(new_handles)}...")
        
        try:
            # Basic request without authentication (works for most cases)
            url = f"{API_BASE_URL}/user.info?handles={handles_param}"
            
            # If API key and secret are available, use authenticated request
            if API_KEY and API_SECRET:
                url = create_authenticated_url("user.info", {"handles": handles_param})
            
            response = requests.get(url)
            
            if response.status_code == 200:
                data = response.json()
                if data["status"] == "OK":
                    # All handles in this chunk are valid
                    valid_handles.extend(chunk)
                else:
                    # Some error occurred, treat all as invalid for now
                    invalid_handles.extend(chunk)
            elif response.status_code == 400:
                # This usually means some handles are invalid
                data = response.json()
                error_msg = data.get("comment", "")
                
                # Try to extract the invalid handle from the error message
                # Example error: "handles: User with handle invalid_handle not found"
                if "not found" in error_msg:
                    parts = error_msg.split("handle ")
                    if len(parts) > 1:
                        invalid_handle = parts[1].split(" ")[0]
                        invalid_handles.append(invalid_handle)
                        # The rest are potentially valid
                        valid_handles.extend([h for h in chunk if h != invalid_handle])
                    else:
                        # Can't determine which is invalid, validate one by one
                        for handle in chunk:
                            if validate_single_handle(handle):
                                valid_handles.append(handle)
                            else:
                                invalid_handles.append(handle)
                else:
                    # Can't determine which is invalid, validate one by one
                    for handle in chunk:
                        if validate_single_handle(handle):
                            valid_handles.append(handle)
                        else:
                            invalid_handles.append(handle)
            else:
                print(f"API Error: Status code {response.status_code}")
                # Validate one by one as a fallback
                for handle in chunk:
                    if validate_single_handle(handle):
                        valid_handles.append(handle)
                    else:
                        invalid_handles.append(handle)
            
            # Be nice to the API - increase delay between requests
            time.sleep(2)  # Increased from 1 to 2 seconds
            
        except requests.exceptions.RequestException as e:
            print(f"Request Error: {e}")
            print(f"Failed to process handles: {', '.join(chunk)}")
            # Validate one by one as a fallback
            for handle in chunk:
                if validate_single_handle(handle):
                    valid_handles.append(handle)
                else:
                    invalid_handles.append(handle)
    
    # Remove duplicates while preserving order
    valid_handles = list(dict.fromkeys(valid_handles))
    invalid_handles = list(dict.fromkeys(invalid_handles))
    
    # Report results
    if valid_handles:
        print(f"\nValid handles ({len(valid_handles)}):")
        for handle in valid_handles:
            print(f"  ✓ {handle}")
        
        # Append valid handles to the file
        with open(HANDLES_FILE, "a") as f:
            for handle in valid_handles:
                f.write(f"{handle}\n")
        
        print(f"\nAdded {len(valid_handles)} new handles to {HANDLES_FILE}.")
    else:
        print("\nNo valid handles found.")
    
    if invalid_handles:
        print(f"\nInvalid handles ({len(invalid_handles)}):")
        for handle in invalid_handles:
            print(f"  ✗ {handle}")
    
    print(f"\nTotal handles in file: {len(existing_handles) + len(valid_handles)}")

def validate_single_handle(handle):
    """Validate a single Codeforces handle."""
    try:
        # Basic request without authentication (works for most cases)
        url = f"{API_BASE_URL}/user.info?handles={handle}"
        
        # If API key and secret are available, use authenticated request
        if API_KEY and API_SECRET:
            url = create_authenticated_url("user.info", {"handles": handle})
        
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            return data["status"] == "OK"
        
        return False
    except requests.exceptions.RequestException:
        return False

if __name__ == "__main__":
    validate_handles() 