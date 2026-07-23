import json
from pathlib import Path

from developer_toolkit.json_formatter import (
    build_output_path,
    format_json,
    load_json,
    save_text,
)


def test_format_json_adds_indentation() -> None:
    data = {"name": "Htet", "skills": ["Python", "Git"]}

    result = format_json(data, indent=2)

    assert '"name": "Htet"' in result
    assert "\n" in result
    assert '  "name"' in result


def test_format_json_can_sort_keys() -> None:
    data = {"b": 2, "a": 1}

    result = format_json(data, indent=2, sort_keys=True)

    assert result.index('"a"') < result.index('"b"')


def test_build_output_path() -> None:
    input_path = Path("examples/json/messy.json")

    output_path = build_output_path(input_path)

    assert output_path == Path("examples/json/messy_formatted.json")


def test_load_json_and_save_text(tmp_path: Path) -> None:
    input_path = tmp_path / "input.json"
    output_path = tmp_path / "output.json"

    input_path.write_text('{"name":"Htet","week":1}', encoding="utf-8")

    data = load_json(input_path)
    formatted_text = format_json(data)
    save_text(formatted_text, output_path)

    loaded_output = json.loads(output_path.read_text(encoding="utf-8"))

    assert data == {"name": "Htet", "week": 1}
    assert output_path.exists()
    assert loaded_output == data