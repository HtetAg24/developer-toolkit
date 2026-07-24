import argparse
import json
import logging
from collections import Counter
from dataclasses import dataclass
from pathlib import Path


VALID_LOG_LEVELS = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}


class LogAnalyzerError(Exception):
    """Base exception for log analyzer errors."""


@dataclass
class LogRecord:
    """A parsed log record."""

    timestamp: str
    level: str
    message: str


@dataclass
class LogAnalysisResult:
    """Summary result from log analysis."""

    total_lines: int
    parsed_lines: int
    invalid_lines: list[str]
    level_counts: dict[str, int]
    records: list[LogRecord]


@dataclass
class LogAnalyzerConfig:
    """Configuration options for log analysis."""

    input_path: Path
    level_filter: str | None = None
    output_path: Path | None = None


def setup_logging() -> None:
    """Configure logging for the log analyzer."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(levelname)s: %(message)s",
    )


def load_log_lines(input_path: Path) -> list[str]:
    """Load log lines from a file."""
    if not input_path.exists():
        raise LogAnalyzerError(f"Input file does not exist: {input_path}")

    if not input_path.is_file():
        raise LogAnalyzerError(f"Input path is not a file: {input_path}")

    return input_path.read_text(encoding="utf-8").splitlines()


def parse_log_line(line: str) -> LogRecord:
    """Parse one log line into a LogRecord."""
    parts = line.strip().split(maxsplit=3)

    if len(parts) != 4:
        raise ValueError("Log line does not match expected format.")

    date_part = parts[0]
    time_part = parts[1]
    level = parts[2].upper()
    message = parts[3]

    if level not in VALID_LOG_LEVELS:
        raise ValueError(f"Unknown log level: {level}")

    timestamp = f"{date_part} {time_part}"

    return LogRecord(
        timestamp=timestamp,
        level=level,
        message=message,
    )


def analyze_lines(lines: list[str]) -> LogAnalysisResult:
    """Analyze raw log lines."""
    records = []
    invalid_lines = []

    for line in lines:
        try:
            record = parse_log_line(line)
            records.append(record)

        except ValueError:
            invalid_lines.append(line)

    level_counter = Counter(record.level for record in records)

    level_counts = {
        level: level_counter.get(level, 0)
        for level in sorted(VALID_LOG_LEVELS)
    }

    return LogAnalysisResult(
        total_lines=len(lines),
        parsed_lines=len(records),
        invalid_lines=invalid_lines,
        level_counts=level_counts,
        records=records,
    )


def filter_records_by_level(
    records: list[LogRecord],
    level_filter: str | None,
) -> list[LogRecord]:
    """Filter log records by level."""
    if level_filter is None:
        return records

    level = level_filter.upper()

    if level not in VALID_LOG_LEVELS:
        raise LogAnalyzerError(f"Unknown level filter: {level_filter}")

    return [record for record in records if record.level == level]


def print_summary(result: LogAnalysisResult) -> None:
    """Print a readable log summary."""
    print("\nLog Summary")
    print("-----------")
    print(f"Total lines: {result.total_lines}")
    print(f"Parsed lines: {result.parsed_lines}")
    print(f"Invalid lines: {len(result.invalid_lines)}")

    print("\nLevel counts")
    print("------------")

    for level, count in result.level_counts.items():
        print(f"{level}: {count}")


def print_records(records: list[LogRecord], level_filter: str | None) -> None:
    """Print filtered log records."""
    if level_filter is None:
        return

    print(f"\nRecords matching level: {level_filter.upper()}")
    print("--------------------------------")

    if not records:
        print("No records found.")
        return

    for record in records:
        print(f"{record.timestamp} {record.level} {record.message}")


def save_summary_json(result: LogAnalysisResult, output_path: Path) -> None:
    """Save log summary as a JSON file."""
    output_path.parent.mkdir(parents=True, exist_ok=True)

    summary = {
        "total_lines": result.total_lines,
        "parsed_lines": result.parsed_lines,
        "invalid_line_count": len(result.invalid_lines),
        "level_counts": result.level_counts,
    }

    output_path.write_text(
        json.dumps(summary, indent=4),
        encoding="utf-8",
    )


def analyze_log(config: LogAnalyzerConfig) -> None:
    """Run the full log analysis process."""
    logging.info("Loading log file: %s", config.input_path)

    lines = load_log_lines(config.input_path)
    result = analyze_lines(lines)

    filtered_records = filter_records_by_level(
        result.records,
        config.level_filter,
    )

    print_summary(result)
    print_records(filtered_records, config.level_filter)

    if config.output_path is not None:
        save_summary_json(result, config.output_path)
        logging.info("Saved summary JSON: %s", config.output_path)

    logging.info("Log analysis completed")


def build_parser() -> argparse.ArgumentParser:
    """Build the command-line argument parser."""
    parser = argparse.ArgumentParser(
        description="Analyze log files and summarize log levels."
    )

    parser.add_argument(
        "input_file",
        help="Path to the log file to analyze.",
    )

    parser.add_argument(
        "--level",
        help="Optional log level filter, such as INFO, WARNING, ERROR or CRITICAL.",
    )

    parser.add_argument(
        "-o",
        "--output",
        help="Optional path to save summary as JSON.",
    )

    return parser


def main() -> None:
    setup_logging()

    parser = build_parser()
    args = parser.parse_args()

    config = LogAnalyzerConfig(
        input_path=Path(args.input_file),
        level_filter=args.level,
        output_path=Path(args.output) if args.output else None,
    )

    try:
        analyze_log(config)

    except LogAnalyzerError as error:
        logging.error("%s", error)


if __name__ == "__main__":
    main()