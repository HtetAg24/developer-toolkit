# Developer Toolkit

This repository contains small Python command-line tools built during Month One of the Loadberry AI Engineering Trainee Programme.

The purpose of this repository is to practise professional software engineering foundations, including Python, Git, Linux/WSL, command-line tools, JSON handling, file input/output, validation, error handling, documentation, and meaningful Git history.

## Tools Completed

### 1. JSON Formatter

The JSON Formatter is a command-line tool that reads a JSON file, formats it into a readable structure, and saves the result to an output file.

Location: src/developer_toolkit/json_formatter.py

Features:

Reads JSON from a file
Formats JSON with indentation
Supports custom indentation
Supports sorted keys
Supports custom output path
Handles missing files
Handles invalid JSON syntax


### 2. Password Generator

The Password Generator is a command-line tool that generates secure random passwords using Python's secrets module.

Location: src/developer_toolkit/password_generator.py

Features:

Generates secure random passwords
Supports custom password length
Supports generating multiple passwords
Supports excluding lowercase letters
Supports excluding uppercase letters
Supports excluding digits
Supports excluding symbols
Handles invalid password length
Handles invalid character selection


### 3. CSV Cleaner

The CSV Cleaner is a command-line tool that reads a messy CSV file, removes extra spaces, removes empty rows, removes duplicate rows, and saves a cleaned CSV file.

Location: src/developer_toolkit/csv_cleaner.py

Features:

Reads CSV files
Trims spaces from headers and values
Removes empty rows
Removes duplicate rows
Supports custom output path
Supports keeping empty rows
Supports keeping duplicate rows
Uses logging for progress messages
Uses custom exceptions for cleaner error handling


## Setup

Clone the repository:

git clone git@github.com:HtetAg24/developer-toolkit.git
cd developer-toolkit

Create and activate a virtual environment:

python -m venv .venv
source .venv/bin/activate

Install dependencies:

python -m pip install --upgrade pip
python -m pip install -r requirements.txt

Check Python version:

python --version

Expected Python version:

Python 3.13.14


## Running Tests

The project uses `pytest` for automated testing.

Run the full test suite with:

```bash
python -m pytest -v