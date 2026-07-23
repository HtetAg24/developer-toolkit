import argparse
import json
from pathlib import Path

def load_json(file_path: Path):
    """Load JSON data from a file."""
    with file_path.open("r", encoding="utf-8") as file:
        data = json.load(file)

    return data


def format_json(data, indent: int = 4, sort_keys: bool = False) -> str:
    """Convert Python data into formatted JSON text."""
    formatted_text = json.dumps(
        data,
        indent=indent,
        sort_keys=sort_keys,
        ensure_ascii=False,
    )

    return formatted_text


def save_text(text: str, output_path: Path) -> None:
    """Save text to a file."""
    with output_path.open("w", encoding="utf-8") as file:
        file.write(text)


def build_output_path(input_path: Path) -> Path:
    """Create a default output path based on the input file name."""
    return input_path.with_name(f"{input_path.stem}_formatted.json")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Format a JSON file and save a readable version."
    )

    parser.add_argument(
        "input_file",
        help="Path to the JSON file to format.",
    )

    parser.add_argument(
        "-o",
        "--output",
        help="Optional output file path.",
    )

    parser.add_argument(
        "--indent",
        type=int,
        default=4,
        help="Number of spaces to use for indentation. Default is 4.",
    )

    parser.add_argument(
        "--sort-keys",
        action="store_true",
        help="Sort JSON keys alphabetically.",
    )

    args = parser.parse_args()

    input_path = Path(args.input_file)

    if args.output:
        output_path = Path(args.output)
    else:
        output_path = build_output_path(input_path)

    try:
        data = load_json(input_path)
        formatted_text = format_json(
            data,
            indent=args.indent,
            sort_keys=args.sort_keys,
        )
        save_text(formatted_text, output_path)

        print("JSON formatted successfully.")
        print(f"Input file: {input_path}")
        print(f"Output file: {output_path}")

    except FileNotFoundError:
        print(f"Error: File not found: {input_path}")

    except json.JSONDecodeError as error:
        print("Error: Invalid JSON file.")
        print(f"Details: {error}")


if __name__ == "__main__":
    main()