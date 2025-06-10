# Git Timesheet Generator

A Python script to generate timesheets from git commit history, specifically filtering for commits by a particular author.

## Overview

This script analyzes git commit history across multiple repositories and:
- Filters commits by author name/email
- Estimates time spent on each commit (in 15-minute increments)
- Adjusts time based on commit message keywords
- Groups work by day and week
- Formats output as a readable timesheet

## Requirements

- Python 3.6+
- pytz library (`pip install pytz`)

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/timesheets.git
cd timesheets

# Install dependencies
pip install -r requirements.txt

# Make the script executable
chmod +x generate_timesheet.py
```

## Usage

```bash
./generate_timesheet.py [options]
```

### Options

- `--base-dir PATH`: Base directory containing git repositories (default: current directory)
- `--since DATE`: Show commits more recent than a specific date (e.g., "2 weeks ago")
- `--until DATE`: Show commits older than a specific date
- `--repos REPO [REPO ...]`: Specific repository names to include
- `--output FORMAT`: Output format (text, csv, markdown, or md, default: text)
- `--author PATTERN`: Filter commits by author (default: "mcgarrah")
- `--timezone TIMEZONE`: Timezone for dates (e.g., "US/Eastern", "EST", "EDT", default: UTC)
- `--output-file PATH`: Write output to file instead of stdout
- `--session-timeout MINUTES`: Minutes between commits to consider them part of the same work session (default: 60)

## Examples

### Generate timesheet for the last 2 weeks

```bash
./generate_timesheet.py --since="2 weeks ago"
```

### Generate timesheet for specific repositories

```bash
./generate_timesheet.py --repos food_service_nutrition food-intelligence-app gpcc --since="1 month ago"
```

### Generate timesheet for a specific date range

```bash
./generate_timesheet.py --since="2023-01-01" --until="2023-01-31"
```

### Generate timesheet with specific author pattern

```bash
./generate_timesheet.py --author="michael mcgarrah" --since="2 weeks ago"
```

### Generate timesheet in US Eastern timezone

```bash
./generate_timesheet.py --since="1 month ago" --timezone="US/Eastern"
```

### Generate CSV output for spreadsheet import

```bash
./generate_timesheet.py --since="1 month ago" --output=csv --output-file=timesheet.csv
```

### Generate markdown output for pretty formatting

```bash
./generate_timesheet.py --since="1 month ago" --output=markdown --output-file=timesheet.md
```

### Generate timesheet for all specified repositories

```bash
./generate_timesheet.py --repos food_service_nutrition food-intelligence-app gpcc gs1_gpc_python gs1_gpc_gtin oneworldsync_client oneworldsync_python oneworldsync_python_medium oneworldsync_python_tinydb shiny-quiz shiny-shop usda_fdc_python --since="1 month ago"
```

## Output Formats

### Text Format
Plain text output organized by weeks and days, showing detailed commit information with timezone abbreviations.

### CSV Format
Comma-separated values format suitable for importing into spreadsheet applications like Excel or Google Sheets. Includes timezone information for each entry.

### Markdown Format
Pretty markdown format with tables organized by week, suitable for viewing in markdown readers or converting to HTML. Includes time ranges and timezone abbreviations for each task to better understand work sessions.

## Time Estimation Logic

- Base time: 15 minutes per commit
- Bug fixes/issues: +15 minutes
- New features/implementations: +30 minutes
- Refactoring/improvements: +15 minutes
- Commits close together (within 60 minutes by default) are considered part of the same work session

## Timezone Support

The script supports various timezone formats:
- IANA timezone names (e.g., "America/New_York")
- Common US timezone aliases (e.g., "US/Eastern")
- Short timezone abbreviations (e.g., "EST", "EDT")
- Prefixed short timezone abbreviations (e.g., "US/EST")

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.