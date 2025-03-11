# Codeforces Rank Tracker v1.1.0

## New Features in v1.1.0

This release adds historical rank tracking capabilities to the Codeforces Rank Tracker, allowing educators to track their students' progress over time.

### Major New Features

- **Historical Rank Tracking**: Added ability to track ratings and ranks from specific time periods (March 2022, 2023, 2024)
- **Historical Data Export**: Added CSV export functionality for historical data
- **Improved API Handling**: Enhanced error recovery and URL encoding for special characters in handles
- **Better Progress Reporting**: Added more detailed progress information during API requests

### New Scripts

- `historical_ranks.py`: Track ratings and ranks from specific time periods
- `export_historical_csv.py`: Export historical data to CSV

### Improvements

- Reduced API request chunk size for better reliability with large numbers of handles
- Added fallback mechanism for failed API requests
- Improved error reporting and diagnostics
- Enhanced documentation with detailed usage instructions for new features

## Previous Release (v1.0.0)

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
