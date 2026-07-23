from pathlib import Path

import pytest

from developer_toolkit.csv_cleaner import (
    CsvCleanerConfig,
    CsvCleanerError,
    clean_csv,
    clean_row,
    clean_rows,
    clean_value,
    is_empty_row,
    load_csv,
    save_csv,
)


def test_clean_value_removes_surrounding_spaces() -> None:
    result = clean_value("  Htet  ")

    assert result == "Htet"


def test_clean_row_cleans_keys_and_values() -> None:
    row = {
        " name ": " Htet ",
        " email ": " htet@example.com ",
    }

    result = clean_row(row)

    assert result == {
        "name": "Htet",
        "email": "htet@example.com",
    }


def test_is_empty_row_detects_empty_row() -> None:
    row = {
        "name": "",
        "email": "",
        "role": "",
    }

    assert is_empty_row(row) is True


def test_clean_rows_removes_empty_rows_and_duplicates() -> None:
    rows = [
        {
            " name ": " Htet ",
            " email ": " htet@example.com ",
            " role ": " AI Engineering Trainee ",
        },
        {
            " name ": " Htet ",
            " email ": " htet@example.com ",
            " role ": " AI Engineering Trainee ",
        },
        {
            " name ": " ",
            " email ": " ",
            " role ": " ",
        },
        {
            " name ": " Alice ",
            " email ": " alice@example.com ",
            " role ": " Data Analyst ",
        },
    ]

    result = clean_rows(rows)

    assert result == [
        {
            "name": "Htet",
            "email": "htet@example.com",
            "role": "AI Engineering Trainee",
        },
        {
            "name": "Alice",
            "email": "alice@example.com",
            "role": "Data Analyst",
        },
    ]


def test_clean_rows_can_keep_duplicates() -> None:
    rows = [
        {"name": "Htet", "email": "htet@example.com"},
        {"name": "Htet", "email": "htet@example.com"},
    ]

    result = clean_rows(rows, remove_duplicates=False)

    assert len(result) == 2


def test_load_csv_rejects_missing_file(tmp_path: Path) -> None:
    missing_file = tmp_path / "missing.csv"

    with pytest.raises(CsvCleanerError, match="Input file does not exist"):
        load_csv(missing_file)


def test_load_and_save_csv(tmp_path: Path) -> None:
    input_path = tmp_path / "messy.csv"
    output_path = tmp_path / "cleaned.csv"

    input_path.write_text(
        " name , email , role \n"
        " Htet , htet@example.com , AI Engineering Trainee \n",
        encoding="utf-8",
    )

    rows = load_csv(input_path)
    cleaned_rows = clean_rows(rows)
    save_csv(cleaned_rows, output_path)

    result = output_path.read_text(encoding="utf-8")

    assert output_path.exists()
    assert "name,email,role" in result
    assert "Htet,htet@example.com,AI Engineering Trainee" in result


def test_clean_csv_full_process(tmp_path: Path) -> None:
    input_path = tmp_path / "messy.csv"
    output_path = tmp_path / "cleaned.csv"

    input_path.write_text(
        " name , email , city \n"
        " Htet , htet@example.com , Cambridge \n"
        " Htet , htet@example.com , Cambridge \n"
        " , , \n"
        " Alice , alice@example.com , London \n",
        encoding="utf-8",
    )

    config = CsvCleanerConfig(
        input_path=input_path,
        output_path=output_path,
    )

    clean_csv(config)

    result = output_path.read_text(encoding="utf-8")

    assert output_path.exists()
    assert "Htet,htet@example.com,Cambridge" in result
    assert "Alice,alice@example.com,London" in result
    assert result.count("Htet") == 1