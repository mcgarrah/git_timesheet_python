# TODO List for Generate Git Timesheet (GGTS)

## Needed

- [ ] Github Actions for CICD/Release
- [ ] PyPi release support
- [ ] ReadTheDocs release support

## Features

- [ ] Add support for custom time estimation rules
- [x] Create a configuration file for default settings
- [ ] Add HTML output format option
- [ ] Support for multiple authors in a single report
- [ ] Add weekly summary view option
- [ ] Implement project categorization based on repository or commit tags
- [ ] Add interactive mode for manual time adjustments

## Improvements

- [ ] Optimize performance for large repositories
- [ ] Add more timezone handling options
- [ ] Improve commit message parsing for better time estimation
- [ ] Add option to exclude certain repositories or file types
- [ ] Support for remote Github/GitLab/etc repositories
- [ ] Simple WebUI maybe / like the interactive mode above ?!?
- [ ] Convert to a pypi python package with a cli

## Documentation

- [ ] Create comprehensive user guide
  - [ ] Sphinx documentation builder
  - [ ] Sphinx hosted with Github Pages
- [ ] Add examples for all output formats
- [ ] Document time estimation algorithm
- [ ] Add installation instructions for dependencies

## Testing

- [x] Add unit tests
- [ ] Create test fixtures for different repository structures
- [ ] Test with various timezone configurations
