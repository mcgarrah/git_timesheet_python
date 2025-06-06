# Git Timesheet Generator

A Python script to generate timesheets from git commit history, specifically filtering for commits by a particular author.

## Overview

This script analyzes git commit history across multiple repositories and:
- Filters commits by author name/email
- Estimates time spent on each commit (in 15-minute increments)
- Adjusts time based on commit message keywords
- Groups work by day and week
- Formats output as a readable timesheet

## Usage

```bash
./generate_timesheet.py [options]
```

### Options

- `--base-dir PATH`: Base directory containing git repositories (default: current directory)
- `--since DATE`: Show commits more recent than a specific date (e.g., "2 weeks ago")
- `--until DATE`: Show commits older than a specific date
- `--repos REPO [REPO ...]`: Specific repository names to include
- `--output FORMAT`: Output format (text or csv, default: text)
- `--author PATTERN`: Filter commits by author (default: "mcgarrah")

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

### Generate timesheet for all specified repositories

```bash
./generate_timesheet.py --repos food_service_nutrition food-intelligence-app gpcc gs1_gpc_python gs1_gpc_gtin oneworldsync_client oneworldsync_python oneworldsync_python_medium oneworldsync_python_tinydb shiny-quiz shiny-shop usda_fdc_python --since="1 month ago"
```

## Output Format

The timesheet is organized by:
- Weeks
- Days within each week
- Repositories worked on each day
- Individual commits with time estimates and author information

Each commit is assigned a time estimate based on:
- Base time: 15 minutes per commit
- Additional time for features, bug fixes, or refactoring
- Adjustments based on time between commits

## Time Estimation Logic

- Base time: 15 minutes per commit
- Bug fixes/issues: +15 minutes
- New features/implementations: +30 minutes
- Refactoring/improvements: +15 minutes
- Commits close together (within 30 minutes) are considered part of the same work session