# TODO List for Generate Git Timesheet (GGTS)

## Needed

- [x] Verify the python library works for all existing use-cases
- [ ] Github Actions for Package release to PyPi
- [ ] Github Actions for ReadTheDocs release
- [ ] Add type hints to all functions for better IDE support
- [ ] Create a proper CHANGELOG.md file

## Features

- [ ] Add support for custom time estimation rules
- [x] Create a configuration file for default settings
- [ ] Add HTML output format option
- [ ] Support for multiple authors in a single report
- [ ] Add weekly summary view option
- [ ] Implement project categorization based on repository or commit tags
- [ ] Add interactive mode for manual time adjustments
- [ ] Export to calendar format (iCal/ICS) for integration with calendar apps
- [ ] Add option to group by project/client using repository naming patterns

## Improvements

- [ ] Optimize performance for large repositories
- [ ] Add more timezone handling options
- [ ] Improve commit message parsing for better time estimation
- [ ] Add option to exclude certain repositories or file types
- [ ] Support for remote Github/GitLab/etc repositories
- [ ] Simple WebUI maybe / like the interactive mode above ?!?
- [x] Convert to a pypi python package with a cli
- [ ] Migrate from pytz to zoneinfo (Python 3.9+) for timezone handling
- [ ] Add progress bar for long-running operations
- [ ] Implement caching for git log data to speed up repeated runs

## Documentation

- [ ] Create comprehensive user guide
  - [ ] Sphinx documentation builder
  - [ ] Sphinx hosted with Github Pages
- [ ] Add examples for all output formats
- [ ] Document time estimation algorithm
- [ ] Add installation instructions for dependencies
- [ ] Create API documentation for library users
- [ ] Add badges to README.md (PyPI version, build status, etc.)

## Testing

- [x] Add unit tests
- [ ] Create test fixtures for different repository structures
- [ ] Test with various timezone configurations
- [ ] Add integration tests with CI/CD pipeline
- [ ] Implement test coverage reporting
- [ ] Add property-based testing for edge cases

## Code Quality

- [ ] Add pre-commit hooks for code formatting and linting
- [ ] Implement static type checking with mypy
- [ ] Set up code quality tools (black, flake8, isort)
- [ ] Add docstrings to all public functions and classes
- [ ] Refactor time estimation logic into a more modular design
