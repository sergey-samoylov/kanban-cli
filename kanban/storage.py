#!/usr/bin/env python3
"""Loads and saves Task objects to/from a CSV file."""

import csv
from task import Task

FILE_PATH = "db/tasks.csv"

def load_tasks() -> list[Task]:
    """Load tasks from the CSV file and return them as Task objects.

    Returns:
        list[Task]: A list of Task objects loaded from the file.
        Returns empty list if file doesn't exist or is empty.
    """
    try:
        with open(FILE_PATH, newline="") as f:
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

    Raises:
        PermissionError:
            If the program doesn't have write permissions for the file.
        FileNotFoundError:
            If the directory doesn't exist (only if 'db/' doesn't exist).
    """
    with open(FILE_PATH, "w", newline="") as f:
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
