"""
task_operations.py - Centralized task business logic

Handles all task-related operations including:
- CRUD operations
- Search/filter/sort
- Category/color management
- Validation
"""

from dataclasses import dataclass
from rich.prompt import Prompt
from rich.console import Console
from typing import TypedDict

from task import Task
from board import COLUMN_HEADERS
from category_colors import load_category_colors, ensure_category_colors, COLORS

console = Console()

# Type definitions - using modern Python syntax
TaskMode = str  # "add" | "edit"
FilterType = str  # "status" | "category"
SortKey = str  # "id" | "title" | "category"

class TaskActionResult(TypedDict):
    tasks: list[Task]
    success: bool
    message: str

@dataclass
class TaskSearchResult:
    tasks: list[Task]
    match_count: int
    query: str

class TaskOperator:
    def __init__(self, tasks: list[Task]):
        self.tasks = tasks
        self._colors = load_category_colors()
    
    def handle_task(
        self,
        mode: TaskMode = "add",
        task_id: int | None = None) -> TaskActionResult:
        """Unified handler for task add/edit operations"""
        # Validation
        if mode == "edit" and task_id is None:
            return self._result("Task ID required for edit mode", False)
        
        existing_task = self._get_task(task_id) if mode == "edit" else None
        
        # Get user input
        title, description = self._get_task_text(existing_task)
        if not title:
            return self._result("Task title cannot be empty", False)
        
        category = self._get_category(existing_task.category if existing_task else None)
        status = self._get_status(existing_task.status if existing_task else None)
        
        # Apply changes
        if mode == "add":
            new_task = Task(
                id=self._get_next_id(),
                title=title,
                description=description,
                category=category,
                status=status
            )
            self.tasks.append(new_task)
        else:
            existing_task.title = title
            existing_task.description = description
            existing_task.category = category
            existing_task.status = status
        
        self._ensure_category_color(category)
        return self._result("Task saved successfully", True)

    def delete_task(self, task_id: int) -> TaskActionResult:
        """Remove task by ID"""
        before_count = len(self.tasks)
        self.tasks = [t for t in self.tasks if t.id != task_id]
        success = len(self.tasks) != before_count
        msg = "Task deleted" if success else "Task not found"
        return self._result(msg, success)

    def move_task(self, task_id: int, status_input: str) -> TaskActionResult:
        """Change task status with validation"""
        try:
            status = self._validate_status(status_input)
        except ValueError as e:
            return self._result(str(e), False)
        
        for task in self.tasks:
            if task.id == task_id:
                if task.status != status:
                    task.status = status
                    return self._result(f"Moved to {status}", True)
                return self._result("Status unchanged", False)
        return self._result("Task not found", False)

    def search_tasks(self, query: str) -> TaskSearchResult:
        """Case-insensitive search across task fields"""
        query = query.lower()
        results = [
            task for task in self.tasks
            if query in task.title.lower() or 
            query in task.description.lower()
        ]
        return TaskSearchResult(results, len(results), query)

    def filter_tasks(self, filter_type: FilterType, value: str) -> list[Task]:
        """Filter by status or category"""
        if filter_type == "status":
            try:
                status = self._validate_status(value)
                return [task for task in self.tasks if task.status == status]
            except ValueError:
                return []
        return [t for t in self.tasks if value.lower() in t.category.lower()]

    def sort_tasks(self, key: SortKey) -> list[Task]:
        """In-place sort by specified key"""
        reverse = key == "id"  # Descending for IDs
        self.tasks.sort(
            key=lambda t: getattr(t, key).lower() if key != "id" else t.id,
            reverse=reverse
        )
        return self.tasks

    # Helper methods
    def _get_task(self, task_id: int) -> Task:
        return next((t for t in self.tasks if t.id == task_id), None)

    def _get_task_text(self, existing_task: Task) -> tuple[str, str]:
        """Extract title and description from user input"""
        default = existing_task.title if existing_task else ""
        raw = Prompt.ask("Enter task", default=default)
        
        if "[" in raw and "]" in raw:
            title, description = raw.split("[", 1)
            return title.strip(), description.rstrip("]").strip()
        return raw.strip(), existing_task.description if existing_task else ""

    def _get_category(self, default: str | None = None) -> str:
        """Get valid category with suggestions"""
        default = default or next(iter(self._colors), "general")
        
        while True:
            category = Prompt.ask(
                f"Category (existing: {', '.join(self._colors.keys())})",
                default=default
            ).strip()
            
            if not category:
                continue
                
            if category not in self._colors:
                confirm = Prompt.ask(
                    f"Create new category '{category}'?",
                    choices=["y", "n"],
                    default="y"
                )
                if confirm == "y":
                    break
                continue
            break
        return category

    def _get_status(self, default: str | None = None) -> str:
        """Get validated status"""
        default = default or COLUMN_HEADERS[0]
        while True:
            status = Prompt.ask(
                "Status",
                choices=COLUMN_HEADERS,
                default=default
            )
            try:
                return self._validate_status(status)
            except ValueError as e:
                console.print(f"[red]{e}[/red]")

    def _validate_status(self, status: str) -> str:
        """Convert and validate status input"""
        status_map = {
            "todo": COLUMN_HEADERS[0],
            "now": COLUMN_HEADERS[1],
            "done": COLUMN_HEADERS[2],
            "t": COLUMN_HEADERS[0],
            "n": COLUMN_HEADERS[1],
            "d": COLUMN_HEADERS[2]
        }
        
        normalized = status_map.get(status.lower(), status)
        if normalized not in COLUMN_HEADERS:
            raise ValueError(f"Invalid status. Must be one of: {COLUMN_HEADERS}")
        return normalized

    def _get_next_id(self) -> int:
        return max((t.id for t in self.tasks), default=0) + 1

    def _ensure_category_color(self, category: str) -> None:
        if category not in self._colors:
            self._colors = load_category_colors()  # Refresh
            if category not in self._colors:
                ensure_category_colors([Task(0, "", "", category, "")])
                self._colors = load_category_colors()

    def _result(self, message: str, success: bool) -> TaskActionResult:
        return {"tasks": self.tasks, "success": success, "message": message}
