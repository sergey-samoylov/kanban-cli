"""Category color management module for Kanban board application.

Handles storage and retrieval of category-color associations,
providing consistent color assignment and management.
"""

import json
from random import choice

# Predefined color palette
COLORS = [
    "black",
    "blue",
    "cyan",
    "green",
    "magenta",
    "red",
    "white",
    "yellow",
]

class ColorStorage:
    """Abstract storage layer for category-color associations.

    Provides a unified interface for loading and saving color mappings.
    Currently uses JSON storage but designed for easy transition to SQLite.
    """

    @staticmethod
    def load() -> dict[str, str]:
        """Load color mappings from storage.

        Returns:
            dict: Category to color mappings. Returns empty dict if no storage exists.
        """
        try:
            with open('db/category_colors.json') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    @staticmethod
    def save(colors: dict[str, str]) -> None:
        """Save color mappings to storage.

        Args:
            colors (dict): Category to color mappings to be saved.
        """
        with open('db/category_colors.json', 'w') as f:
            json.dump(colors, f, indent=4)

def load_category_colors() -> dict[str, str]:
    """Load current category-color associations.

    Returns:
        dict: Copy of current category-color mappings.
    """
    return ColorStorage.load()

def save_category_colors(colors: dict[str, str]) -> None:
    """Persist category-color associations to storage.

    Args:
        colors (dict): Category to color mappings to save.
    """
    ColorStorage.save(colors)

def assign_random_color(used: set[str]) -> str:
    """Assign a random color not in the used set.

    Args:
        used (set): Colors that are already assigned.

    Returns:
        str: Available color from COLORS palette.
    """
    available = [c for c in COLORS if c not in used]
    return choice(available) if available else choice(COLORS)

def change_category_color(category: str, new_color: str) -> None:
    """Change color for an existing category.

    Args:
        category (str): Category to modify.
        new_color (str): New color to assign.

    Raises:
        ValueError: If color is not in predefined COLORS.
        KeyError: If category doesn't exist.
    """
    if new_color not in COLORS:
        raise ValueError(f"Color must be one of: {COLORS}")

    colors = load_category_colors()
    if category not in colors:
        raise KeyError(f"Category '{category}' doesn't exist")

    colors[category] = new_color
    save_category_colors(colors)

# The quotes around 'Task' are important - this is called a "forward reference"
# and is used when the Task class hasn't been defined yet when this type hint
# is written

def ensure_category_colors(tasks: list['Task']) -> None:
    """
    Ensure all task categories have assigned colors.
    Creates new color assignments for any missing categories.

    Args:
        tasks: List of Task objects to check for categories
    """
    colors = load_category_colors()
    used_colors = set(colors.values())

    for task in tasks:
        if task.category and task.category not in colors:
            colors[task.category] = assign_random_color(used_colors)
            used_colors.add(colors[task.category])

    save_category_colors(colors)
