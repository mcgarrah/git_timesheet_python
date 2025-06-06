#!/usr/bin/env python3
import os
import subprocess
from datetime import datetime, timedelta
import re
from collections import defaultdict
import argparse

def get_git_repos(base_dir):
    """Find git repositories in the specified directory."""
    repos = []
    for item in os.listdir(base_dir):
        full_path = os.path.join(base_dir, item)
        if os.path.isdir(full_path) and os.path.exists(os.path.join(full_path, '.git')):
            repos.append(full_path)
    return repos

def get_git_log(repo_path, since=None, until=None):
    """Get git log for a repository with author date and commit message."""
    cmd = ['git', 'log', '--pretty=format:%ad|%s|%h', '--date=iso']
    
    if since:
        cmd.append(f'--since={since}')
    if until:
        cmd.append(f'--until={until}')
    
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
        if len(parts) >= 3:
            date_str, message, commit_hash = parts[0], parts[1], parts[2]
            try:
                date = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S %z')
                parsed_commits.append((date, message, commit_hash, repo_name))
            except ValueError:
                continue
    
    # Sort commits by date
    parsed_commits.sort(key=lambda x: x[0])
    
    # Estimate time for each commit
    time_entries = []
    for i, (date, message, commit_hash, repo) in enumerate(parsed_commits):
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
            
            # If commits are close together (within 30 minutes), they're likely part of the same work session
            if time_gap < 30:
                time_spent = min(time_spent, time_gap)
        
        time_entries.append({
            'date': date,
            'repo': repo,
            'message': message,
            'commit': commit_hash,
            'minutes': time_spent
        })
    
    return time_entries

def round_to_15_min(minutes):
    """Round minutes to nearest 15-minute increment."""
    return round(minutes / 15) * 15

def format_timesheet(time_entries, output_format='text'):
    """Format time entries into a weekly timesheet."""
    if not time_entries:
        return "No git activity found in the specified time period."
    
    # Group by week and day
    weeks = defaultdict(lambda: defaultdict(list))
    for entry in time_entries:
        date = entry['date']
        week_start = (date - timedelta(days=date.weekday())).strftime('%Y-%m-%d')
        day = date.strftime('%Y-%m-%d')
        weeks[week_start][day].append(entry)
    
    result = []
    
    # Format as text
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
                    result.append(f"    {commit_time} - {time_str} - {entry['message'][:60]} ({entry['commit'][:7]})")
            
        result.append(f"\nWeek Total: {week_total/60:.2f} hours\n")
        result.append("=" * 80)
    
    return "\n".join(result)

def main():
    parser = argparse.ArgumentParser(description='Generate a timesheet from git commit history')
    parser.add_argument('--base-dir', default=os.getcwd(), help='Base directory containing git repositories')
    parser.add_argument('--since', help='Show commits more recent than a specific date (e.g., "2 weeks ago")')
    parser.add_argument('--until', help='Show commits older than a specific date')
    parser.add_argument('--repos', nargs='+', help='Specific repository names to include')
    parser.add_argument('--output', choices=['text', 'csv'], default='text', help='Output format')
    
    args = parser.parse_args()
    
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
        commits = get_git_log(repo, args.since, args.until)
        time_entries = estimate_time_spent(commits, repo_name)
        all_time_entries.extend(time_entries)
    
    # Sort all entries by date
    all_time_entries.sort(key=lambda x: x['date'])
    
    # Format and print timesheet
    timesheet = format_timesheet(all_time_entries, args.output)
    print(timesheet)

if __name__ == "__main__":
    main()