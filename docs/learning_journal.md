# Learning Journal

## Session 01 - Repository and Environment Setup

#### What was worked on
- The `developer-toolkit` repository was created and cloned locally.
- GitHub SSH authentication was configured and verified.
- Python 3.13.14 was installed and configured using `pyenv`.
- A local virtual environment was created using `.venv`.
- The project folder structure was created with separate folders for source code, tests, documentation, examples, and practice files.
- `.gitignore` was reviewed and updated to exclude `.venv/` and other local/cache files.

#### What was learned
- SSH authentication is a cleaner way to work with GitHub than repeatedly using passwords or personal access tokens.
- `pyenv` can be used to manage project-specific Python versions without changing the system Python.
- A `.python-version` file tells `pyenv` which Python version to use inside a repository.
- A virtual environment keeps project dependencies isolated from the system Python installation.
- A clean folder structure makes the project easier to understand, maintain, and extend.
- `.gitignore` is important for preventing local environment files, credentials, and cache files from being committed.

#### Issues encountered
- HTTPS cloning returned a 403 authentication error.
- Python 3.13 was not installed by default in WSL.
- The virtual environment was initially activated from the wrong folder after restarting the PC.

#### Questions for mentor
- Should SSH be used as the default GitHub authentication method for all repositories? What is the difference with HTTP?
- Is the current folder structure suitable for the `developer-toolkit` repository?


## Session 02 - Python Practice: Lists, Dictionaries, Sorting and Lambda Functions

#### What was worked on
- A small Python practice script was written using a list of dictionaries.
- Each dictionary represented a character with fields such as name, weapon, HP, MP and Luck.
- The list was sorted by values such as `Luck` and `HP`.
- Formatted output was printed using dictionary keys and f-strings.

#### What was learned
- A list can store multiple related items.
- A dictionary stores data as key-value pairs.
- A list of dictionaries is a common structure when working with JSON, APIs, CSV rows and structured records.
- The `sorted()` function can sort a list using a custom key.
- A `lambda` function can be used to tell Python which dictionary value should be used for sorting.
- F-strings make printed output easier to read and format.

#### Issues encountered
- A syntax error occurred when the `sorted()` function call was split incorrectly across lines.
- The variable name `Carry` was initially used, but lowercase naming was more appropriate for normal variables.

#### Questions for mentor
- Should small Python practice scripts be committed as learning evidence?



## Session 03 - JSON Formatter

#### What was worked on
- A JSON Formatter command-line tool was implemented.
- A messy JSON example file was created under `examples/json/`.
- The tool was designed to load JSON from a file, format it, and save the result to a new file.
- Command-line options were added for custom output path, indentation level, and alphabetical key sorting.
- Basic error handling was added for missing files and invalid JSON syntax.

#### What was learned
- The `json` module can be used to load JSON data into Python objects.
- JSON objects are usually converted into Python dictionaries.
- JSON arrays are usually converted into Python lists.
- `json.dumps()` can convert Python data back into formatted JSON text.
- `argparse` can be used to create command-line tools with required and optional arguments.
- `pathlib.Path` provides a clean way to work with file paths.
- Splitting code into functions makes the program easier to understand, test and maintain.
- Error handling improves the user experience by showing clear messages instead of raw tracebacks.

#### Issues encountered
- Running the script without an input file produced an argument error because `input_file` was required.
- A filename typo occurred when trying to open `messy_formated.json` instead of `messy_formatted.json`.

#### Questions for mentor
- Should generated example output files be committed, or should they be generated locally only?


### Session 04 - Password Generator

#### What was worked on
- A Password Generator command-line tool was implemented.
- The tool was designed to generate secure random passwords using Python's `secrets` module.
- Command-line options were added for password length, number of passwords, and character type selection.
- Basic validation and error handling were added.

#### What was learned
- The `secrets` module is more suitable than `random` for security-sensitive random values.
- The `string` module provides useful predefined character groups such as lowercase letters, uppercase letters, digits, and punctuation.
- Boolean command-line flags can be handled with `argparse` using `action="store_true"`.
- Validation helps prevent invalid inputs such as zero-length passwords or no selected character types.
- Splitting logic into functions makes the code easier to understand and maintain.

#### Issues encountered
- Currently none

#### Questions for mentor
- Is terminal output sufficient for this tool, or should it support saving generated passwords to a local file?
- Are there preferred password policy rules that should be followed in real life scenarios other than what was applied in this tool?


## Session 05 - Pytest Tests for Developer Tools

#### What was worked on
- Automated tests were added for the JSON Formatter and Password Generator tools.
- `pytest` was installed and added to `requirements.txt`.
- A `pyproject.toml` file was added to configure the project package structure.
- The project was installed in editable mode using `python -m pip install -e .`.
- Tests were written under the `tests/` folder.
- The full test suite was run successfully.

#### What was learned
- `pytest` can be used to test individual functions automatically.
- `assert` statements are used to check expected behaviour.
- `pytest.raises()` can be used to test expected errors.
- `tmp_path` provides a temporary directory for safely testing file input/output.
- Installing the project in editable mode allows test files to import source code from the `src/` folder.
- Automated tests make the project more reliable and easier to review.

#### Test results
- 10 tests were collected.
- 10 tests passed.
- JSON Formatter tests passed successfully.
- Password Generator tests passed successfully.

#### Issues encountered
- No test failure was encountered during the first full test run.
- The test setup required adding `pyproject.toml` so the package could be imported cleanly from the `src/` layout.

#### Questions for mentor
- As this is my first time usiing `pytest`, I tried it with much support from AI. But tried to understand each and every line of code. If possible, I want a feed back on the quality of the code written and the performance of `pytest`.


## Session 06 - CSV Cleaner

#### What was worked on
- A CSV Cleaner command-line tool was implemented.
- A messy CSV example file was created under `examples/csv/`.
- The tool was designed to load CSV data, clean rows, remove empty rows, remove duplicate rows, and save the cleaned result.
- Type hints were added to make function inputs and outputs clearer.
- A `dataclass` was used to store CSV cleaner configuration.
- Logging was added to show progress during execution.
- A custom exception class was added for CSV cleaner-specific errors.
- Automated pytest tests were added for the CSV Cleaner.

#### What was learned
- Python's built-in `csv` module can be used to read and write CSV files.
- `csv.DictReader` reads CSV rows as dictionaries.
- `csv.DictWriter` writes dictionaries back into CSV format.
- `dataclass` can be used to group related configuration values cleanly.
- Logging is more professional than using `print()` for application progress messages.
- Custom exceptions make tool-specific errors clearer.
- Type hints improve readability and make the code easier to maintain.
- `pytest` can test small cleaning functions and full file input/output workflows.

#### Test results
- 18 tests were collected.
- 18 tests passed.
- 8 CSV Cleaner tests passed.
- Existing JSON Formatter and Password Generator tests continued to pass.

#### Issues encountered
- No test failure was encountered during the full test run.
- Temporary output files should be reviewed before committing so that only useful example files are kept in the repository.

#### Questions for mentor
- Should the CSV Cleaner support more cleaning options, such as lowercasing email addresses or validating required columns?
- Should logging output also be written to a log file?