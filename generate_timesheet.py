#!/usr/bin/env python3
"""
Compatibility layer for the old generate_timesheet.py script.
This allows existing code and tests to continue working with the new module structure.
"""

# Import functions from the new module structure
from git_timesheet.git_utils import get_git_repos, get_git_log, estimate_time_spent
from git_timesheet.formatters import format_text, format_csv, format_markdown, format_timesheet
from git_timesheet.timezone_utils import convert_to_timezone, get_timezone_abbr
from git_timesheet.config import get_config
from git_timesheet.cli import main

# For backwards compatibility
if __name__ == "__main__":
    main()