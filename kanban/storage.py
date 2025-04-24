#!/usr/bin/env python3
"""Loads and saves Task objects to/from a CSV file."""

import csv
from pathlib import Path
from platformdirs import user_data_dir

try:
    from kanban.task import Task
except ImportError:
    from task import Task

APP_NAME = "kanban-cli"
APP_AUTHOR = "your-name"  # optional, change or omit

# Construct a cross-platform safe data directory path
DATA_DIR = Path(user_data_dir(APP_NAME, APP_AUTHOR))
DB_DIR = DATA_DIR / "db"
TASKS_FILE = DB_DIR / "tasks.csv"

# Ensure the db directory exists
DB_DIR.mkdir(parents=True, exist_ok=True)

def load_tasks() -> list[Task]:
    """Load tasks from the CSV file and return them as Task objects.

    Returns:
        list[Task]: A list of Task objects loaded from the file.
        Returns empty list if file doesn't exist or is empty.
    """
    try:
        with open(TASKS_FILE, newline="") as f:
            reader = csv.DictReader(f)
            return [Task(
                id=int(row["id"]),
                title=row["title"],
                description=row["description"],
                category=row["category"],
                status=row["status"]
            ) for row in reader]
    except FileNotFoundError:
        return []

def save_tasks(tasks: list[Task]) -> None:
    """Save a list of Task objects to the CSV file.

    Overwrites the existing file with the provided tasks data.
    The CSV file == a header row followed by one row per task.

    Args:
        tasks (list[Task]): List of Task objects to be saved.
    """
    with open(TASKS_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["id", "title", "description", "category", "status"])
        for task in tasks:
            writer.writerow([
                task.id,
                task.title,
                task.description,
                task.category,
                task.status
            ])

