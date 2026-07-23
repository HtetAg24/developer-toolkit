import argparse
import secrets
import string


def build_character_sets(
    use_lowercase: bool = True,
    use_uppercase: bool = True,
    use_digits: bool = True,
    use_symbols: bool = True,
    
) -> list[str]:
    """Build the selected character sets for password generation."""
    character_sets = []

    if use_lowercase:
        character_sets.append(string.ascii_lowercase)

    if use_uppercase:
        character_sets.append(string.ascii_uppercase)

    if use_digits:
        character_sets.append(string.digits)

    if use_symbols:
        character_sets.append(string.punctuation)

    return character_sets


def validate_options(length: int, character_sets: list[str]) -> None:
    """Validate password generation options."""
    if length <= 0:
        raise ValueError("Password length must be greater than 0.")

    if not character_sets:
        raise ValueError("At least one character type must be selected.")

    if length < len(character_sets):
        raise ValueError(
            "Password length is too short for the selected character types."
        )


def generate_password(length: int, character_sets: list[str]) -> str:
    """Generate a secure random password."""
    all_characters = "".join(character_sets)

    password_characters = []

    for character_set in character_sets:
        password_characters.append(secrets.choice(character_set))

    remaining_length = length - len(password_characters)

    for _ in range(remaining_length):
        password_characters.append(secrets.choice(all_characters))

    secrets.SystemRandom().shuffle(password_characters)

    return "".join(password_characters)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate secure random passwords."
    )

    parser.add_argument(
        "--length",
        type=int,
        default=16,
        help="Length of the password. Default is 16.",
    )

    parser.add_argument(
        "--count",
        type=int,
        default=1,
        help="Number of passwords to generate. Default is 1.",
    )

    parser.add_argument(
        "--no-lowercase",
        action="store_true",
        help="Exclude lowercase letters.",
    )

    parser.add_argument(
        "--no-uppercase",
        action="store_true",
        help="Exclude uppercase letters.",
    )

    parser.add_argument(
        "--no-digits",
        action="store_true",
        help="Exclude digits.",
    )

    parser.add_argument(
        "--no-symbols",
        action="store_true",
        help="Exclude symbols.",
    )

    args = parser.parse_args()

    try:
        character_sets = build_character_sets(
            use_lowercase=not args.no_lowercase,
            use_uppercase=not args.no_uppercase,
            use_digits=not args.no_digits,
            use_symbols=not args.no_symbols,
        )

        validate_options(args.length, character_sets)

        if args.count <= 0:
            raise ValueError("Password count must be greater than 0.")

        for _ in range(args.count):
            password = generate_password(args.length, character_sets)
            print(password)

    except ValueError as error:
        print(f"Error: {error}")


if __name__ == "__main__":
    main()