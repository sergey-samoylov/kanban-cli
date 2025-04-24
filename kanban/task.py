#!/usr/bin/env python3
"""The Task data structure using Python's dataclasses."""

from dataclasses import dataclass

@dataclass
class Task:
    """A task item representing a unit of work to be tracked.

    Example:
        >>> task = Task(
        ...     id=1,
        ...     title="Complete project documentation",
        ...     description="Write API documentation for all endpoints",
        ...     category="🖥️ Work",
        ...     status="🔥NOW",
        ... )
        >>> task.title
        'Complete project documentation'
    """
    id: int
    title: str
    description: str
    category: str
    status: str
