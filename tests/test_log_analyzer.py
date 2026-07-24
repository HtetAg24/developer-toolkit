import json
from pathlib import Path

import pytest

from developer_toolkit.log_analyzer import (
    LogAnalyzerConfig,
    LogAnalyzerError,
    LogRecord,
    analyze_lines,
    analyze_log,
    filter_records_by_level,
    load_log_lines,
    parse_log_line,
    save_summary_json,
)


def test_load_log_lines_reads_file(tmp_path: Path) -> None:
    log_path = tmp_path / "app.log"
    log_path.write_text(
        "2026-07-23 09:00:01 INFO Application started\n",
        encoding="utf-8",
    )

    result = load_log_lines(log_path)

    assert result == ["2026-07-23 09:00:01 INFO Application started"]


def test_load_log_lines_rejects_missing_file(tmp_path: Path) -> None:
    missing_file = tmp_path / "missing.log"

    with pytest.raises(LogAnalyzerError, match="Input file does not exist"):
        load_log_lines(missing_file)


def test_parse_log_line_returns_log_record() -> None:
    line = "2026-07-23 09:07:03 ERROR Database connection failed"

    result = parse_log_line(line)

    assert result == LogRecord(
        timestamp="2026-07-23 09:07:03",
        level="ERROR",
        message="Database connection failed",
    )


def test_parse_log_line_rejects_malformed_line() -> None:
    line = "malformed line"

    with pytest.raises(ValueError, match="expected format"):
        parse_log_line(line)


def test_parse_log_line_rejects_unknown_level() -> None:
    line = "2026-07-23 09:00:01 NOTICE Something happened"

    with pytest.raises(ValueError, match="Unknown log level"):
        parse_log_line(line)


def test_analyze_lines_counts_levels_and_invalid_lines() -> None:
    lines = [
        "2026-07-23 09:00:01 INFO Application started",
        "2026-07-23 09:05:41 WARNING API response time high",
        "2026-07-23 09:07:03 ERROR Database connection failed",
        "2026-07-23 09:25:00 CRITICAL Payment queue unavailable",
        "malformed line without expected format",
    ]

    result = analyze_lines(lines)

    assert result.total_lines == 5
    assert result.parsed_lines == 4
    assert len(result.invalid_lines) == 1
    assert result.level_counts["INFO"] == 1
    assert result.level_counts["WARNING"] == 1
    assert result.level_counts["ERROR"] == 1
    assert result.level_counts["CRITICAL"] == 1
    assert result.level_counts["DEBUG"] == 0


def test_filter_records_by_level_returns_only_matching_records() -> None:
    records = [
        LogRecord(
            timestamp="2026-07-23 09:00:01",
            level="INFO",
            message="Application started",
        ),
        LogRecord(
            timestamp="2026-07-23 09:07:03",
            level="ERROR",
            message="Database connection failed",
        ),
    ]

    result = filter_records_by_level(records, "ERROR")

    assert result == [
        LogRecord(
            timestamp="2026-07-23 09:07:03",
            level="ERROR",
            message="Database connection failed",
        )
    ]


def test_filter_records_by_level_returns_all_records_when_filter_is_none() -> None:
    records = [
        LogRecord(
            timestamp="2026-07-23 09:00:01",
            level="INFO",
            message="Application started",
        )
    ]

    result = filter_records_by_level(records, None)

    assert result == records


def test_filter_records_by_level_rejects_unknown_level() -> None:
    records = []

    with pytest.raises(LogAnalyzerError, match="Unknown level filter"):
        filter_records_by_level(records, "NOTICE")


def test_save_summary_json_writes_summary_file(tmp_path: Path) -> None:
    lines = [
        "2026-07-23 09:00:01 INFO Application started",
        "2026-07-23 09:07:03 ERROR Database connection failed",
        "bad line",
    ]

    result = analyze_lines(lines)
    output_path = tmp_path / "summary.json"

    save_summary_json(result, output_path)

    saved_data = json.loads(output_path.read_text(encoding="utf-8"))

    assert saved_data == {
        "total_lines": 3,
        "parsed_lines": 2,
        "invalid_line_count": 1,
        "level_counts": {
            "CRITICAL": 0,
            "DEBUG": 0,
            "ERROR": 1,
            "INFO": 1,
            "WARNING": 0,
        },
    }


def test_analyze_log_full_process_saves_json_summary(tmp_path: Path) -> None:
    input_path = tmp_path / "app.log"
    output_path = tmp_path / "summary.json"

    input_path.write_text(
        "2026-07-23 09:00:01 INFO Application started\n"
        "2026-07-23 09:07:03 ERROR Database connection failed\n"
        "malformed line\n",
        encoding="utf-8",
    )

    config = LogAnalyzerConfig(
        input_path=input_path,
        level_filter="ERROR",
        output_path=output_path,
    )

    analyze_log(config)

    saved_data = json.loads(output_path.read_text(encoding="utf-8"))

    assert output_path.exists()
    assert saved_data["total_lines"] == 3
    assert saved_data["parsed_lines"] == 2
    assert saved_data["invalid_line_count"] == 1
    assert saved_data["level_counts"]["ERROR"] == 1