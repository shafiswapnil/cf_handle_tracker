# Codeforces Rank Tracker v1.0.0

## First Stable Release

This is the first stable release of the Codeforces Rank Tracker, a tool designed to track changes in Codeforces ranks for a list of handles (students).

### Features

- Track Codeforces ratings and ranks for multiple users
- Detect and highlight rating/rank changes
- Store historical data for comparison
- Simple command-line interface
- Colorized output for better visualization
- CSV export for further analysis
- Handle validation before adding to tracking list

### Improvements in this Release

- **Improved API Handling**: Added proper URL encoding for handles with special characters
- **Enhanced Error Recovery**: Added individual fallback mechanism for failed API requests
- **Better Authentication**: Improved API authentication signature generation
- **Optimized for Large Lists**: Reduced chunk size and increased delays between requests
- **Detailed Error Reporting**: Added more detailed error messages and progress reporting

### Installation

1. Clone this repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Create a `.env` file with your Codeforces API key and secret (optional but recommended)
4. Add your students' handles to the `handles.txt` file (one handle per line)

### Usage

Run the tracker:

```
python3 cf_tracker.py
```

Export data to CSV:

```
python3 export_csv.py
```

For more details, please refer to the README.md file.
