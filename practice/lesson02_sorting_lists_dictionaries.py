ffxtoons = [
    {"name": "Tidus", "weapon": "Caladbolg", "HP": 99999, "MP": 999, "Luck": 120},
    {"name": "Yuna", "weapon": "Nivarna", "HP": 38908, "MP": 999, "Luck": 135},
    {"name": "Auron", "weapon": "Masamune", "HP": 90000, "MP": 300, "Luck": 90},
    {"name": "Wakka", "weapon": "World_Champion", "HP": 99900, "MP": 333, "Luck": 110},
    {"name": "Kimahri", "weapon": "Spirit_Lance", "HP": 50000, "MP": 888, "Luck": 100},
    {"name": "Lulu", "weapon": "Onion_Knight", "HP": 40000, "MP": 990, "Luck": 125},
    {"name": "Rikku", "weapon": "Godhand", "HP": 70098, "MP": 770, "Luck": 140},
]

sorted_by_hp = sorted(
    ffxtoons,
    key=lambda character: character["HP"],
    reverse=True
)

for character in sorted_by_hp:
    print(
        character["name"],
        "-",
        character["weapon"],
        "- HP:",
        character["HP"],
        "- MP:",
        character["MP"],
        "- Luck:",
        character["Luck"]
    )