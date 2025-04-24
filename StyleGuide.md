# 🧑‍🎨 Code Style Guide – Terminal Kanban Board (Rich + CSV)

*A solid __Code Style Guide__ ensures the project stays  
readable, maintainable, and scalable.*

## 🔤 General Conventions

- **Language**: Pure Python 3.10+
- **Formatting**: Follow **PEP8** strictly
- **Max line length**: 79 characters (PEP8)
- **Encoding**: UTF-8
- **File extensions**: Always `.py`

---

## 🧱 File & Folder Structure

- Use **snake_case** for filenames and module names
- Store persistent data in a `db/` folder
- One responsibility per file (`task.py` = task logic, etc.)
- Group code into logical modules: `task`, `storage`, `commands`, `board`, `colors`

---

## 🧑‍💻 Naming Conventions

- **Variables**: `snake_case`
- **Functions**: `snake_case`
- **Classes**: `PascalCase`
- **Constants**: `ALL_CAPS`
- **Private members**: Prefix with `_` (e.g. `_parse_description`)

---

## ✨ Docstrings & Comments

- Use **English** for all code, comments, and docstrings
- Every function and class must include a **docstring**
- Use triple-double quotes (`"""`) for all docstrings
- Short inline comments should use `#`, start with a space

### Function Docstring Template:

```python
def move_task(task_id: int, column: str) -> None:
    """
    Move a task to the specified column.

    Args:
        task_id (int): ID of the task to move.
        column (str): Target column (TODO, NOW, DONE).

    Returns:
        None
    """
```

---

## ⌨️ Input & Command Syntax

- Commands are colon-prefixed (e.g., `:a`, `:w`)
- Task creation input uses brackets for description:
  - `"My task title [optional description]"`

---

## 🧪 Type Hints & Typing

- **Always use type hints** (functions, methods, parameters, return types)
- Use `Optional`, `List`, `Dict`, etc. from `typing` where needed
- Prefer clarity over compactness

---

## 📦 Imports

- Standard library → third-party libs → local modules
- Sorted alphabetically within each group
- Avoid wildcard imports (`from x import *`)

Example:
```python
import csv
import os
from typing import List

from rich.panel import Panel

from .task import Task
```

---

## 🎨 Rich-Specific Styling

- Use `rich.panel.Panel` for all visible UI blocks
- Use `rich.columns.Columns` for the main board layout
- Categories control the **border color** of each task
- Overall board should be wrapped in a `Panel` with title aligned to the right

---

## 🔁 ID Management

- IDs are reused and small (e.g. 1, 2, 3...)
- After deletion, lowest unused ID should be recycled
- Used only for command-based manipulations

---

## 🖍 Color & Category Rules

- New category → assigned random unused color
- User can reassign color using command (e.g., `:color work red`)
- Color config should be persistable (JSON or similar, optional at first)

---

## 🛑 Error Handling

- Show **friendly error messages** using Rich
- Never crash on bad input — always validate

---

## 🚀 Dev Philosophy

- Code must be **modular** and **easy to extend**
- Prefer **explicit logic** over clever tricks
- Favor **readability** over brevity
- Everything should feel like it belongs in the terminal

