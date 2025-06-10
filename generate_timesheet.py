#!/usr/bin/env python3
import os
import subprocess
from datetime import datetime, timedelta
import re
from collections import defaultdict
import argparse
import csv
import sys
import pytz

# Configuration
SESSION_TIMEOUT_MINUTES = 60  # Minutes between commits to consider them part of the same work session

def get_git_repos(base_dir):
    """Find git repositories in the specified directory."""
    repos = []
    for item in os.listdir(base_dir):
        full_path = os.path.join(base_dir, item)
        if os.path.isdir(full_path) and os.path.exists(os.path.join(full_path, '.git')):
            repos.append(full_path)
    return repos

def get_git_log(repo_path, since=None, until=None, author=None):
    """Get git log for a repository with author date and commit message."""
    cmd = ['git', 'log', '--pretty=format:%ad|%an|%ae|%s|%h', '--date=iso']
    
    if since:
        cmd.append(f'--since={since}')
    if until:
        cmd.append(f'--until={until}')
    if author:
        cmd.append(f'--author={author}')
    
    try:
        result = subprocess.run(cmd, cwd=repo_path, capture_output=True, text=True)
        if result.returncode == 0:
            return result.stdout.strip().split('\n') if result.stdout.strip() else []
        return []
    except Exception as e:
        print(f"Error getting git log for {repo_path}: {e}")
        return []

def estimate_time_spent(commits, repo_name):
    """Estimate time spent on commits based on commit messages and frequency."""
    if not commits:
        return []
    
    # Parse commit dates and messages
    parsed_commits = []
    for commit in commits:
        if not commit:
            continue
        parts = commit.split('|')
        if len(parts) >= 5:
            date_str, author_name, author_email, message, commit_hash = parts[0], parts[1], parts[2], parts[3], parts[4]
            try:
                date = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S %z')
                parsed_commits.append((date, message, commit_hash, repo_name, author_name, author_email))
            except ValueError:
                continue
    
    # Sort commits by date
    parsed_commits.sort(key=lambda x: x[0])
    
    # Estimate time for each commit
    time_entries = []
    for i, (date, message, commit_hash, repo, author_name, author_email) in enumerate(parsed_commits):
        # Base time: 15 minutes per commit
        time_spent = 15
        
        # Adjust based on commit message
        if re.search(r'fix|bug|issue', message, re.I):
            time_spent += 15
        if re.search(r'feature|implement|add', message, re.I):
            time_spent += 30
        if re.search(r'refactor|clean|improve', message, re.I):
            time_spent += 15
        
        # Check time gap to next commit
        if i < len(parsed_commits) - 1:
            next_date = parsed_commits[i+1][0]
            time_gap = (next_date - date).total_seconds() / 60
            
            # If commits are close together (within the configured session timeout), they're likely part of the same work session
            if time_gap < SESSION_TIMEOUT_MINUTES:
                time_spent = min(time_spent, time_gap)
        
        time_entries.append({
            'date': date,
            'repo': repo,
            'message': message,
            'commit': commit_hash,
            'minutes': time_spent,
            'author_name': author_name,
            'author_email': author_email
        })
    
    return time_entries

def round_to_15_min(minutes):
    """Round minutes to nearest 15-minute increment."""
    return round(minutes / 15) * 15

def convert_to_timezone(date, timezone_str='UTC'):
    """Convert datetime to specified timezone."""
    if date.tzinfo is None:
        date = date.replace(tzinfo=pytz.UTC)
    
    # Handle common timezone aliases
    timezone_aliases = {
        'US/Eastern': 'America/New_York',
        'US/Central': 'America/Chicago',
        'US/Mountain': 'America/Denver',
        'US/Pacific': 'America/Los_Angeles',
        'US/Alaska': 'America/Anchorage',
        'US/Hawaii': 'Pacific/Honolulu'
    }
    
    # Use the alias if available
    tz_name = timezone_aliases.get(timezone_str, timezone_str)
    
    try:
        target_tz = pytz.timezone(tz_name)
    except pytz.exceptions.UnknownTimeZoneError:
        print(f"Warning: Unknown timezone '{timezone_str}'. Falling back to UTC.")
        target_tz = pytz.UTC
        
    return date.astimezone(target_tz)

def format_timesheet(time_entries, output_format='text', timezone_str='UTC'):
    """Format time entries into a weekly timesheet."""
    if not time_entries:
        return "No git activity found in the specified time period."
        
    # Filter for entries with "mcgarrah" in author name or email
    filtered_entries = [entry for entry in time_entries 
                       if 'mcgarrah' in entry['author_name'].lower() or 
                          'mcgarrah' in entry['author_email'].lower() or
                          'michael mcgarrah' in entry['author_name'].lower()]
    
    if not filtered_entries:
        return "No git activity found for the specified author in the given time period."
        
    time_entries = filtered_entries
    
    # Convert dates to specified timezone
    for entry in time_entries:
        entry['date'] = convert_to_timezone(entry['date'], timezone_str)
    
    # Group by week and day
    weeks = defaultdict(lambda: defaultdict(list))
    for entry in time_entries:
        date = entry['date']
        week_start = (date - timedelta(days=date.weekday())).strftime('%Y-%m-%d')
        day = date.strftime('%Y-%m-%d')
        weeks[week_start][day].append(entry)
    
    if output_format == 'text':
        return format_text(weeks)
    elif output_format == 'csv':
        return format_csv(weeks, time_entries)
    elif output_format in ['markdown', 'md']:
        return format_markdown(weeks)
    else:
        return format_text(weeks)  # Default to text

def format_text(weeks):
    """Format timesheet as plain text."""
    result = []
    
    for week_start, days in sorted(weeks.items()):
        result.append(f"\nWeek of {week_start}")
        result.append("=" * 80)
        
        week_total = 0
        for day, entries in sorted(days.items()):
            day_date = datetime.strptime(day, '%Y-%m-%d')
            day_name = day_date.strftime('%A')
            day_total = sum(entry['minutes'] for entry in entries)
            week_total += day_total
            
            result.append(f"\n{day_name}, {day} - Total: {day_total/60:.2f} hours")
            result.append("-" * 80)
            
            # Group by repository
            repos = defaultdict(list)
            for entry in entries:
                repos[entry['repo']].append(entry)
            
            for repo, repo_entries in sorted(repos.items()):
                repo_name = os.path.basename(repo)
                repo_total = sum(entry['minutes'] for entry in repo_entries)
                result.append(f"\n  {repo_name} - {repo_total/60:.2f} hours")
                
                for entry in repo_entries:
                    time_str = f"{entry['minutes']/60:.2f}h"
                    commit_time = entry['date'].strftime('%H:%M')
                    result.append(f"    {commit_time} - {time_str} - {entry['message'][:60]} ({entry['commit'][:7]}) - {entry['author_name']}")
            
        result.append(f"\nWeek Total: {week_total/60:.2f} hours\n")
        result.append("=" * 80)
    
    return "\n".join(result)

def format_csv(weeks, time_entries):
    """Format timesheet as CSV."""
    output = []
    
    # Write to string buffer
    output.append("Date,Day,Week,Start Time,Duration (min),Duration (hours),Repository,Commit,Message,Author")
    
    for entry in sorted(time_entries, key=lambda x: x['date']):
        date = entry['date']
        week_start = (date - timedelta(days=date.weekday())).strftime('%Y-%m-%d')
        day_name = date.strftime('%A')
        date_str = date.strftime('%Y-%m-%d')
        time_str = date.strftime('%H:%M')
        repo_name = os.path.basename(entry['repo'])
        
        # Escape any commas in the message
        message = entry['message'].replace('"', '""')
        
        line = f'"{date_str}","{day_name}","{week_start}","{time_str}",{entry["minutes"]},{entry["minutes"]/60:.2f},"{repo_name}","{entry["commit"][:7]}","{message}","{entry["author_name"]}"'
        output.append(line)
    
    return "\n".join(output)

def format_markdown(weeks):
    """Format timesheet as Markdown."""
    result = []
    
    result.append("# Git Activity Timesheet\n")
    
    for week_start, days in sorted(weeks.items()):
        result.append(f"## Week of {week_start}\n")
        
        # Create a table for the week
        result.append("| Day | Date | Time | Repository | Hours | Description |")
        result.append("|-----|------|------|------------|-------|-------------|")
        
        week_total = 0
        
        # Sort days to ensure Monday-Sunday order
        sorted_days = sorted(days.items())
        
        for day, entries in sorted_days:
            day_date = datetime.strptime(day, '%Y-%m-%d')
            day_name = day_date.strftime('%A')
            day_total = sum(entry['minutes'] for entry in entries)
            week_total += day_total
            
            # Group by repository
            repos = defaultdict(list)
            for entry in entries:
                repos[entry['repo']].append(entry)
            
            # First row for the day includes the day name
            first_row = True
            
            for repo, repo_entries in sorted(repos.items()):
                repo_name = os.path.basename(repo)
                repo_total = sum(entry['minutes'] for entry in repo_entries)
                
                # Group entries by similar tasks
                tasks = defaultdict(list)
                for entry in repo_entries:
                    # Use first 30 chars of message as key
                    key = entry['message'][:30]
                    tasks[key].append(entry)
                
                for task_name, task_entries in tasks.items():
                    task_total = sum(entry['minutes'] for entry in task_entries)
                    task_desc = f"{task_name}... ({len(task_entries)} commits)"
                    
                    # Get the time of the first commit in this task group
                    first_commit_time = min(entry['date'] for entry in task_entries).strftime('%H:%M')
                    
                    if first_row:
                        result.append(f"| {day_name} | {day} | {first_commit_time} | {repo_name} | {task_total/60:.2f} | {task_desc} |")
                        first_row = False
                    else:
                        result.append(f"|  | | {first_commit_time} | {repo_name} | {task_total/60:.2f} | {task_desc} |")
            
            # Add day total
            result.append(f"| **Total** | | | | **{day_total/60:.2f}** | |")
            result.append("| | | | | | |")  # Empty row for readability
        
        # Add week total
        result.append(f"| **Week Total** | | | | **{week_total/60:.2f}** | |")
        result.append("\n")
    
    return "\n".join(result)

def main():
    global SESSION_TIMEOUT_MINUTES
    
    parser = argparse.ArgumentParser(description='Generate a timesheet from git commit history')
    parser.add_argument('--base-dir', default=os.getcwd(), help='Base directory containing git repositories')
    parser.add_argument('--since', help='Show commits more recent than a specific date (e.g., "2 weeks ago")')
    parser.add_argument('--until', help='Show commits older than a specific date')
    parser.add_argument('--repos', nargs='+', help='Specific repository names to include')
    parser.add_argument('--output', choices=['text', 'csv', 'markdown', 'md'], default='text', 
                        help='Output format (text, csv, or markdown/md)')
    parser.add_argument('--author', default='mcgarrah', help='Filter commits by author (default: mcgarrah)')
    parser.add_argument('--timezone', default='UTC', help='Timezone for dates (e.g., "US/Eastern", default: UTC)')
    parser.add_argument('--output-file', help='Write output to file instead of stdout')
    parser.add_argument('--session-timeout', type=int, default=SESSION_TIMEOUT_MINUTES, 
                        help=f'Minutes between commits to consider them part of the same work session (default: {SESSION_TIMEOUT_MINUTES})')
    
    args = parser.parse_args()
    
    # Update session timeout if provided via command line
    SESSION_TIMEOUT_MINUTES = args.session_timeout
    
    # Get all git repositories in the base directory
    all_repos = get_git_repos(args.base_dir)
    
    # Filter repositories if specified
    if args.repos:
        repos = []
        for repo_name in args.repos:
            matching_repos = [r for r in all_repos if os.path.basename(r) == repo_name]
            repos.extend(matching_repos)
    else:
        repos = all_repos
    
    if not repos:
        print("No git repositories found.")
        return
    
    print(f"Found {len(repos)} repositories.")
    
    # Collect time entries from all repositories
    all_time_entries = []
    for repo in repos:
        repo_name = os.path.basename(repo)
        print(f"Processing {repo_name}...")
        commits = get_git_log(repo, args.since, args.until, args.author)
        time_entries = estimate_time_spent(commits, repo_name)
        all_time_entries.extend(time_entries)
    
    # Sort all entries by date
    all_time_entries.sort(key=lambda x: x['date'])
    
    # Format timesheet
    timesheet = format_timesheet(all_time_entries, args.output, args.timezone)
    
    # Output the timesheet
    if args.output_file:
        with open(args.output_file, 'w') as f:
            f.write(timesheet)
        print(f"Timesheet written to {args.output_file}")
    else:
        print(timesheet)

if __name__ == "__main__":
    main()