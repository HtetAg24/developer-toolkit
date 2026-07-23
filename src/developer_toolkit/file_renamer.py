import argparse
import logging
from dataclasses import dataclass
from pathlib import Path


class FileRenamerError(Exception):
    """Base exception for file renamer errors."""


@dataclass
class FileRenamerConfig:
    """Configuration options for file renaming."""

    directory: Path
    prefix: str = ""
    lowercase: bool = False
    replace_spaces: bool = True
    dry_run: bool = True


def setup_logging() -> None:
    """Configure logging for the file renamer."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(levelname)s: %(message)s",
    )


def find_files(directory: Path) -> list[Path]:
    """Find files in a directory."""
    if not directory.exists():
        raise FileRenamerError(f"Directory does not exist: {directory}")

    if not directory.is_dir():
        raise FileRenamerError(f"Path is not a directory: {directory}")

    return sorted(path for path in directory.iterdir() if path.is_file())


def build_new_name(file_path: Path, config: FileRenamerConfig) -> Path:
    """Build a new file path based on renaming rules."""
    stem = file_path.stem
    suffix = file_path.suffix

    if config.replace_spaces:
        stem = "_".join(stem.split())

    if config.lowercase:
        stem = stem.lower()
        suffix = suffix.lower()

    if config.prefix:
        stem = f"{config.prefix}{stem}"

    return file_path.with_name(f"{stem}{suffix}")


def plan_renames(
    files: list[Path],
    config: FileRenamerConfig,
) -> list[tuple[Path, Path]]:
    """Create a safe rename plan."""
    rename_plan = []
    planned_targets = set()

    for file_path in files:
        new_path = build_new_name(file_path, config)

        if new_path == file_path:
            continue

        if new_path in planned_targets:
            raise FileRenamerError(f"Duplicate target path planned: {new_path}")

        if new_path.exists():
            raise FileRenamerError(f"Target file already exists: {new_path}")

        planned_targets.add(new_path)
        rename_plan.append((file_path, new_path))

    return rename_plan


def apply_renames(
    rename_plan: list[tuple[Path, Path]],
    dry_run: bool = True,
) -> None:
    """Apply or preview file renames."""
    if not rename_plan:
        logging.info("No files need to be renamed.")
        return

    for old_path, new_path in rename_plan:
        if dry_run:
            logging.info("DRY RUN: %s -> %s", old_path.name, new_path.name)
        else:
            old_path.rename(new_path)
            logging.info("RENAMED: %s -> %s", old_path.name, new_path.name)


def rename_files(config: FileRenamerConfig) -> None:
    """Run the full file renaming process."""
    logging.info("Scanning directory: %s", config.directory)

    files = find_files(config.directory)
    rename_plan = plan_renames(files, config)

    apply_renames(rename_plan, dry_run=config.dry_run)

    logging.info("Files scanned: %s", len(files))
    logging.info("Rename actions planned: %s", len(rename_plan))


def build_parser() -> argparse.ArgumentParser:
    """Build the command-line argument parser."""
    parser = argparse.ArgumentParser(
        description="Batch rename files by replacing spaces, lowercasing names, and adding prefixes."
    )

    parser.add_argument(
        "directory",
        help="Directory containing files to rename.",
    )

    parser.add_argument(
        "--prefix",
        default="",
        help="Optional prefix to add to each filename.",
    )

    parser.add_argument(
        "--lowercase",
        action="store_true",
        help="Convert filenames and extensions to lowercase.",
    )

    parser.add_argument(
        "--keep-spaces",
        action="store_true",
        help="Keep spaces instead of replacing them with underscores.",
    )

    parser.add_argument(
        "--apply",
        action="store_true",
        help="Actually rename files. Without this flag, the tool runs in dry-run mode.",
    )

    return parser


def main() -> None:
    setup_logging()

    parser = build_parser()
    args = parser.parse_args()

    config = FileRenamerConfig(
        directory=Path(args.directory),
        prefix=args.prefix,
        lowercase=args.lowercase,
        replace_spaces=not args.keep_spaces,
        dry_run=not args.apply,
    )

    try:
        rename_files(config)

    except FileRenamerError as error:
        logging.error("%s", error)


if __name__ == "__main__":
    main()