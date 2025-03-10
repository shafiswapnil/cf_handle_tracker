# Codeforces Rank Tracker

A tool to track changes in Codeforces ranks for a list of handles (students).

## Features

- Track Codeforces ratings and ranks for multiple users
- Detect and highlight rating/rank changes
- Store historical data for comparison
- Simple command-line interface
- Colorized output for better visualization
- CSV export for further analysis
- Handle validation before adding to tracking list

## Setup

1. Clone this repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Create a `.env` file with your Codeforces API key (if needed)
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

### Exporting Data

Export the data to CSV:

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

## License

This project is open source and available under the MIT License.
