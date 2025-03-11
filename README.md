# Codeforces Rank Tracker

A tool to track changes in Codeforces ranks for a list of handles (students).

**Current Version: 1.1.0**

## Features

- Track Codeforces ratings and ranks for multiple users
- Detect and highlight rating/rank changes
- Store historical data for comparison
- Simple command-line interface
- Colorized output for better visualization
- CSV export for further analysis
- Handle validation before adding to tracking list
- Historical rank tracking for specific time periods

## Setup

1. Clone this repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Create a `.env` file with your Codeforces API key and secret (optional but recommended):

   ```
   CODEFORCES_API_KEY=your_api_key_here
   CODEFORCES_SECRET=your_secret_here
   ```

   You can get these from your [Codeforces API settings](https://codeforces.com/settings/api).

   Note: While most basic operations work without authentication, using an API key can help avoid rate limits and access more features.

   A template `.env.example` file is provided. You can copy it to create your `.env` file:

   ```
   cp .env.example .env
   ```

   Then edit the `.env` file with your actual API credentials.

4. Add your students' handles to the `handles.txt` file (one handle per line)

## Usage

### Adding Handles

You can add handles in several ways:

1. **Edit handles.txt directly**:
   Add one handle per line. Lines starting with `#` are treated as comments.

2. **Use the add_handles.py script**:

   ```
   python3 add_handles.py
   ```

   This will prompt you to enter handles one per line. Press Ctrl+D (Unix) or Ctrl+Z (Windows) when done.

3. **Use the validate_handles.py script**:
   ```
   python3 validate_handles.py
   ```
   This will validate the handles against the Codeforces API before adding them.

### Tracking Ranks

Run the tracker:

```
python3 cf_tracker.py
```

This will:

- Fetch the current ratings and ranks for all handles in the list
- Compare them with the previously stored data
- Display the results in a table with colorized output
- Save the current data for future comparison

### Historical Rank Tracking

To track historical ranks for specific time periods (e.g., March 2022, 2023, 2024), use the historical_ranks.py script:

```
python3 historical_ranks.py
```

This will:

- Fetch the complete rating history for each handle
- Find the ratings closest to March of each specified year
- Display the results in a table with colorized output

You can also specify specific handles as command-line arguments:

```
python3 historical_ranks.py tourist Petr ecnerwala
```

The script will show:

- The rating and rank for each handle in March of each year
- The exact date of the contest that determined that rating
- "N/A" if no rating data is available within 3 months of the target date

#### Exporting Historical Data to CSV

To export the historical rank data to a CSV file:

```
python3 export_historical_csv.py
```

This will:

- Fetch the historical data for all handles in your handles.txt file
- Export the data to a CSV file (`historical_codeforces_ranks.csv`)
- Include ratings, ranks, and contest dates for each time period

You can also specify specific handles as command-line arguments:

```
python3 export_historical_csv.py tourist Petr ecnerwala
```

### Exporting Current Data

Export the current tracking data to CSV:

```
python3 export_csv.py
```

This will create a CSV file (`codeforces_ranks.csv`) with the current user data.

## Data Storage

The tool stores user data in a JSON file (`user_data.json`) to track changes between runs. The file contains:

- Handle
- Current rating
- Current rank
- Maximum rating
- Maximum rank
- Last updated timestamp

## Understanding Contest Dates in Historical Data

The "Contest Date" columns in historical data represent the actual dates when the Codeforces contests took place that determined the ratings shown for each time period.

For example, if you see:

```
| Handle | March 2022 Rating | March 2022 Contest Date | March 2023 Rating | March 2023 Contest Date |
|--------|------------------|------------------------|------------------|------------------------|
| user1  | 1500 (Specialist) | 2022-03-15             | 1600 (Expert)     | 2023-02-28             |
```

This means:

- For March 2022: The rating of 1500 was from a contest on March 15, 2022
- For March 2023: The rating of 1600 was from a contest on February 28, 2023 (closest to March)

The script looks for the contest date closest to March 15th of each year, but within a 3-month window (90 days). If a user didn't participate in any contests within that window, you'll see "N/A" in both the rating and contest date columns.

## Rank Colors

The tool uses the following colors for different Codeforces ranks:

- Newbie: Gray
- Pupil: Green
- Specialist: Cyan
- Expert: Blue
- Candidate Master: Purple
- Master: Yellow
- International Master: Yellow
- Grandmaster: Red
- International Grandmaster: Red
- Legendary Grandmaster: Red

## Requirements

- Python 3.6+
- requests
- python-dotenv
- tabulate

## Advanced Usage

### Scheduled Tracking

You can set up a cron job to run the tracker automatically at regular intervals:

```
# Run every day at 8 AM
0 8 * * * cd /path/to/codeforces-rank-tracker && python3 cf_tracker.py
```

### Customization

You can modify the code to:

- Change the output format
- Add more data fields
- Implement additional features like email notifications

## Troubleshooting

- **API Rate Limits**: The Codeforces API has rate limits. If you're tracking many handles, the tool might hit these limits. The code includes delays to mitigate this.
- **Invalid Handles**: If a handle is invalid, the validate_handles.py script will detect it and not add it to the list.
- **Missing Dependencies**: Make sure to install all dependencies listed in requirements.txt.
- **API Authentication**: If you're experiencing issues with API rate limits or need access to more features, make sure to set up your API key and secret in the `.env` file. The application will work without authentication for basic operations, but authenticated requests are more reliable.
- **Large Number of Handles**: If you're tracking a large number of handles (more than 100), the application will process them in smaller chunks to avoid URL length limitations. This might make the process slower, but more reliable. If you're still experiencing issues, you can further reduce the `chunk_size` variable in the code.
- **Special Characters in Handles**: Some Codeforces handles contain special characters like underscores, dots, or hyphens. The application now properly URL-encodes these characters to avoid API errors. If you're still experiencing issues with specific handles, try adding them individually rather than in bulk.

## Version History

- **v1.1.0** - Added historical rank tracking and CSV export for historical data
- **v1.0.0** - Initial release with basic rank tracking functionality

## License

This project is open source and available under the MIT License.
