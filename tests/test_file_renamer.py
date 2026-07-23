from pathlib import Path

import pytest

from developer_toolkit.file_renamer import (
    FileRenamerConfig,
    FileRenamerError,
    apply_renames,
    build_new_name,
    find_files,
    plan_renames,
)


def test_find_files_returns_only_files(tmp_path: Path) -> None:
    file_path = tmp_path / "Project Notes.txt"
    folder_path = tmp_path / "subfolder"

    file_path.write_text("notes", encoding="utf-8")
    folder_path.mkdir()

    result = find_files(tmp_path)

    assert result == [file_path]


def test_find_files_rejects_missing_directory(tmp_path: Path) -> None:
    missing_directory = tmp_path / "missing"

    with pytest.raises(FileRenamerError, match="Directory does not exist"):
        find_files(missing_directory)


def test_build_new_name_replaces_spaces() -> None:
    file_path = Path("Project Notes.txt")
    config = FileRenamerConfig(directory=Path("examples/files"))

    result = build_new_name(file_path, config)

    assert result == Path("Project_Notes.txt")


def test_build_new_name_can_lowercase_name_and_suffix() -> None:
    file_path = Path("Test Image.PNG")
    config = FileRenamerConfig(
        directory=Path("examples/files"),
        lowercase=True,
    )

    result = build_new_name(file_path, config)

    assert result == Path("test_image.png")


def test_build_new_name_can_add_prefix() -> None:
    file_path = Path("Weekly Report.csv")
    config = FileRenamerConfig(
        directory=Path("examples/files"),
        prefix="week2_",
    )

    result = build_new_name(file_path, config)

    assert result == Path("week2_Weekly_Report.csv")


def test_plan_renames_skips_files_that_do_not_need_changes(tmp_path: Path) -> None:
    file_path = tmp_path / "clean_file.txt"
    file_path.write_text("clean", encoding="utf-8")

    config = FileRenamerConfig(directory=tmp_path)
    files = [file_path]

    result = plan_renames(files, config)

    assert result == []


def test_plan_renames_detects_existing_target(tmp_path: Path) -> None:
    original_file = tmp_path / "Project Notes.txt"
    target_file = tmp_path / "Project_Notes.txt"

    original_file.write_text("notes", encoding="utf-8")
    target_file.write_text("existing", encoding="utf-8")

    config = FileRenamerConfig(directory=tmp_path)

    with pytest.raises(FileRenamerError, match="Target file already exists"):
        plan_renames([original_file], config)


def test_apply_renames_dry_run_does_not_rename_file(tmp_path: Path) -> None:
    old_path = tmp_path / "Project Notes.txt"
    new_path = tmp_path / "Project_Notes.txt"

    old_path.write_text("notes", encoding="utf-8")

    apply_renames([(old_path, new_path)], dry_run=True)

    assert old_path.exists()
    assert not new_path.exists()


def test_apply_renames_with_apply_changes_file_name(tmp_path: Path) -> None:
    old_path = tmp_path / "Project Notes.txt"
    new_path = tmp_path / "Project_Notes.txt"

    old_path.write_text("notes", encoding="utf-8")

    apply_renames([(old_path, new_path)], dry_run=False)

    assert not old_path.exists()
    assert new_path.exists()
    assert new_path.read_text(encoding="utf-8") == "notes"