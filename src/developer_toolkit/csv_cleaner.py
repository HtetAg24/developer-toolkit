import argparse
import csv
import logging
from dataclasses import dataclass
from pathlib import Path


class CsvCleanerError(Exception):
    """Base exception for CSV cleaner errors."""


@dataclass
class CsvCleanerConfig:
    """Configuration options for CSV cleaning."""

    input_path: Path
    output_path: Path
    remove_empty_rows: bool = True
    remove_duplicates: bool = True


def setup_logging() -> None:
    """Configure logging for the CSV cleaner."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(levelname)s: %(message)s",
    )


def clean_value(value: str) -> str:
    """Clean a single CSV value."""
    return value.strip()


def clean_row(row: dict[str, str]) -> dict[str, str]:
    """Clean all values in a CSV row."""
    cleaned_row = {}

    for key, value in row.items():
        clean_key = clean_value(key)
        clean_item = clean_value(value)
        cleaned_row[clean_key] = clean_item

    return cleaned_row


def is_empty_row(row: dict[str, str]) -> bool:
    """Check whether all values in a row are empty."""
    return all(value == "" for value in row.values())


def row_to_tuple(row: dict[str, str]) -> tuple[tuple[str, str], ...]:
    """Convert a row dictionary into a hashable tuple for duplicate checking."""
    return tuple(sorted(row.items()))


def load_csv(input_path: Path) -> list[dict[str, str]]:
    """Load rows from a CSV file."""
    if not input_path.exists():
        raise CsvCleanerError(f"Input file does not exist: {input_path}")

    with input_path.open("r", encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)

        if reader.fieldnames is None:
            raise CsvCleanerError("CSV file has no header row.")

        rows = list(reader)

    return rows


def clean_rows(
    rows: list[dict[str, str]],
    remove_empty_rows: bool = True,
    remove_duplicates: bool = True,
) -> list[dict[str, str]]:
    """Clean CSV rows by trimming spaces, removing empty rows and removing duplicates."""
    cleaned_rows = []
    seen_rows = set()

    for row in rows:
        cleaned_row = clean_row(row)

        if remove_empty_rows and is_empty_row(cleaned_row):
            continue

        if remove_duplicates:
            row_key = row_to_tuple(cleaned_row)

            if row_key in seen_rows:
                continue

            seen_rows.add(row_key)

        cleaned_rows.append(cleaned_row)

    return cleaned_rows


def save_csv(rows: list[dict[str, str]], output_path: Path) -> None:
    """Save cleaned rows to a CSV file."""
    if not rows:
        raise CsvCleanerError("No rows available to save.")

    output_path.parent.mkdir(parents=True, exist_ok=True)

    fieldnames = list(rows[0].keys())

    with output_path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerows(rows)


def clean_csv(config: CsvCleanerConfig) -> None:
    """Run the full CSV cleaning process."""
    logging.info("Loading CSV file: %s", config.input_path)
    rows = load_csv(config.input_path)

    logging.info("Cleaning rows")
    cleaned_rows = clean_rows(
        rows,
        remove_empty_rows=config.remove_empty_rows,
        remove_duplicates=config.remove_duplicates,
    )

    logging.info("Saving cleaned CSV file: %s", config.output_path)
    save_csv(cleaned_rows, config.output_path)

    logging.info("CSV cleaning completed")
    logging.info("Original rows: %s", len(rows))
    logging.info("Cleaned rows: %s", len(cleaned_rows))


def build_parser() -> argparse.ArgumentParser:
    """Build the command-line argument parser."""
    parser = argparse.ArgumentParser(
        description="Clean a CSV file by trimming spaces and removing empty or duplicate rows."
    )

    parser.add_argument(
        "input_file",
        help="Path to the CSV file to clean.",
    )

    parser.add_argument(
        "-o",
        "--output",
        default="examples/csv/cleaned_customers.csv",
        help="Output path for the cleaned CSV file.",
    )

    parser.add_argument(
        "--keep-empty-rows",
        action="store_true",
        help="Keep empty rows instead of removing them.",
    )

    parser.add_argument(
        "--keep-duplicates",
        action="store_true",
        help="Keep duplicate rows instead of removing them.",
    )

    return parser


def main() -> None:
    setup_logging()

    parser = build_parser()
    args = parser.parse_args()

    config = CsvCleanerConfig(
        input_path=Path(args.input_file),
        output_path=Path(args.output),
        remove_empty_rows=not args.keep_empty_rows,
        remove_duplicates=not args.keep_duplicates,
    )

    try:
        clean_csv(config)

    except CsvCleanerError as error:
        logging.error("%s", error)


if __name__ == "__main__":
    main()