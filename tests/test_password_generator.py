import pytest

from developer_toolkit.password_generator import (
    build_character_sets,
    generate_password,
    validate_options,
)


def test_build_character_sets_default_includes_four_sets() -> None:
    character_sets = build_character_sets()

    assert len(character_sets) == 4


def test_build_character_sets_can_exclude_symbols() -> None:
    character_sets = build_character_sets(use_symbols=False)
    combined_characters = "".join(character_sets)

    assert "a" in combined_characters
    assert "A" in combined_characters
    assert "0" in combined_characters
    assert "!" not in combined_characters


def test_validate_options_rejects_zero_length() -> None:
    character_sets = build_character_sets()

    with pytest.raises(ValueError, match="greater than 0"):
        validate_options(0, character_sets)


def test_validate_options_rejects_no_character_sets() -> None:
    with pytest.raises(ValueError, match="At least one character type"):
        validate_options(16, [])


def test_generate_password_has_requested_length() -> None:
    character_sets = build_character_sets()

    password = generate_password(24, character_sets)

    assert len(password) == 24


def test_generate_digits_only_password() -> None:
    character_sets = build_character_sets(
        use_lowercase=False,
        use_uppercase=False,
        use_digits=True,
        use_symbols=False,
    )

    password = generate_password(12, character_sets)

    assert len(password) == 12
    assert password.isdigit()