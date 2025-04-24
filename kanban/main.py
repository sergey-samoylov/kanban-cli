"""
main.py - Kanban Board CLI Interface

Handles user interaction and display management.
Refreshes board automatically after each operation.
"""

try:
    from rich.console import Console
    from rich.prompt import Prompt
except ImportError:
    print("Rich is not installed.")
    print("Install it with pip or your package manager.")
    exit(1)

from board import KanbanBoard, COLUMN_HEADERS
from storage import load_tasks, save_tasks
from task import Task
from task_operations import TaskOperator, TaskActionResult
from category_colors import COLORS, save_category_colors

console = Console()

def display_result(
    result: TaskActionResult,
    board: KanbanBoard,
    tasks: list[Task]) -> tuple[KanbanBoard, list[Task]]:
    """Handle operation results and refresh display"""
    if result["message"]:
        color = "green" if result["success"] else "red"
        console.print(f"[{color}]{result['message']}[/{color}]")

    if result["success"]:
        tasks = result["tasks"]
        board = KanbanBoard(tasks)
        board.render()
    return board, tasks

def main() -> None:
    """Main application loop with automatic refreshes"""
    tasks = load_tasks()
    operator = TaskOperator(tasks)
    board = KanbanBoard(tasks)
    board.render()

    while True:
        try:
            command = Prompt.ask(":").strip().lower()

            match command:
                # Help system
                case "h" | ":h" | "help" | ":help":
                    while True:
                        board.render_help()
                        cmd = Prompt.ask(":exit help>", default="q")
                        if cmd in ("q", ":q"):
                            break
                    board.render()

                # Exit commands
                case "q" | "quit" | ":q" | "й":
                    save_tasks(tasks)
                    console.print("[[green]Saved[/] & [blue]Quit[/]]")
                    break
                case "q!" | "quit!" | ":q!":
                    break

                # Save command
                case "w" | ":w" | "ц":
                    save_tasks(tasks)
                    console.print("[[green]Saved[/]]")

                # Task operations:
                case "a" | ":a" | "ф":  # Add
                    result = operator.handle_task("add")
                    board, tasks = display_result(result, board, tasks)

                case "e" | ":e":  # Edit
                    try:
                        task_id = int(Prompt.ask("Task ID to edit"))
                        result = operator.handle_task("edit", task_id)
                        board, tasks = display_result(result, board, tasks)
                    except ValueError:
                        console.print("[red]Invalid task ID[/red]")

                case "d" | ":d":  # Delete
                    try:
                        task_id = int(Prompt.ask("Task ID to delete"))
                        result = operator.delete_task(task_id)
                        board, tasks = display_result(result, board, tasks)
                    except ValueError:
                        console.print("[red]Invalid task ID[/red]")

                # Layout toggle
                case "l" | ":l":
                    board.toggle_layout()

                # Task movement
                case "m" | ":m":
                    try:
                        task_id = int(Prompt.ask("Task ID to move"))
                        status = Prompt.ask(
                            "New status (todo/now/done or t/n/d)",
                            default="now"
                        )
                        result = operator.move_task(task_id, status)
                        board, tasks = display_result(result, board, tasks)
                    except ValueError:
                        console.print("[red]Invalid input[/red]")

                # Color management
                case "c" | ":c":
                    if not operator._colors:
                        console.print("[yellow]No categories exist yet![/yellow]")
                        continue

                    category = Prompt.ask(
                        "Category to change",
                        choices=list(operator._colors.keys()),
                        show_choices=True
                    )
                    new_color = Prompt.ask(
                        f"New color for '{category}'",
                        choices=COLORS,
                        default=operator._colors[category],
                        show_choices=True
                    )
                    if new_color != operator._colors[category]:
                        operator._colors[category] = new_color
                        save_category_colors(operator._colors)
                        console.print(f"[green]Updated {category} color[/green]")
                        board = KanbanBoard(tasks)  # Refresh after color change
                        board.render()
                    else:
                        console.print("[yellow]Color unchanged[/yellow]")

                # Filtering by status or category
                case "f" | ":f":
                    filter_type = Prompt.ask(
                        "Filter by",
                        choices=["status", "category"],
                        default="status"
                    )
                    if filter_type == "status":
                        value = Prompt.ask(
                            "Status (todo/now/done or t/n/d)",
                            default="todo"
                        )
                        filtered = operator.filter_tasks("status", value)
                    else:
                        value = Prompt.ask("Category name")
                        filtered = operator.filter_tasks("category", value)

                    if not filtered:
                        console.print("[yellow]No matching tasks found[/yellow]")
                    board = KanbanBoard(filtered)
                    board.render()

                # Sorting
                case "s" | ":s":
                    sort_key = Prompt.ask(
                        "Sort by",
                        choices=["id", "title", "category"],
                        default="id"
                    )
                    operator.sort_tasks(sort_key)
                    board = KanbanBoard(tasks)
                    board.render()

                # Search
                case cmd if cmd.startswith('/') or cmd in ("search", ":search"):
                    query = cmd[1:] if cmd.startswith('/') else Prompt.ask("Search term")
                    if not query.strip():
                        console.print("[yellow]Please enter a search term[/yellow]")
                        continue

                    results = operator.search_tasks(query)
                    console.print(f"[blue]Found {results.match_count} matches[/blue]")
                    board = KanbanBoard(results.tasks)
                    board.render()

                # Reset view
                case "clear" | ":clear":
                    board = KanbanBoard(tasks)
                    board.render()

                # Unknown command
                case _:
                    console.print(
                        "[yellow]Unknown command - type 'help' for options[/]"
                    )

        except KeyboardInterrupt:
            console.print(
                "\n[yellow]Use 'q' to quit or 'clear' to refresh[/]"
            )
        except Exception as e:
            console.print(f"[red]Error: {str(e)}[/]")
            save_tasks(tasks)  # Emergency save

if __name__ == "__main__":
    main()
