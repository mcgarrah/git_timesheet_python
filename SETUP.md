# Generate Git Timesheet (GGTS) Setup

This document explains how to set up the Generate Git Timesheet (GGTS) tool in a Python virtual environment.

## Prerequisites

- Python 3.6 or higher
- Git

## Setup Instructions

### 1. Clone the repository (if you haven't already)

```bash
git clone https://github.com/mcgarrah/git_timesheet_python
cd git_timesheet_python
```

### 2. Create a virtual environment

#### On Linux/macOS:

```bash
# Create a virtual environment
python3 -m venv .venv

# Activate the virtual environment
source .venv/bin/activate
```

#### On Windows:

```bash
# Create a virtual environment
python -m venv .venv

# Activate the virtual environment
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Verify installation

```bash
ggts --help
```

## Usage

Once set up, you can use the timesheet generator as described in the [README.md](README.md) documentation.

### Basic example:

```bash
ggts --since="2 weeks ago" --timezone="US/Eastern"
```

## Deactivating the virtual environment

When you're done using the tool, you can deactivate the virtual environment:

```bash
deactivate
```
