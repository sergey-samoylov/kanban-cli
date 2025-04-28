"""
main.py - Kanban Board CLI Interface

This module serves as the main entry point for the Kanban Board command-line
application.  It provides an interactive interface for managing tasks using a
Rich-powered terminal display.

The application features:
- Interactive task management (add, edit, delete, move tasks)
- Real-time board rendering with automatic refreshes
- Task filtering, sorting, and searching capabilities
- Category color customization
- Persistent storage of tasks and configurations
- Help system with command documentation

Key Components:
- KanbanBoard: Handles the visual representation of tasks
- TaskOperator: Manages task operations and business logic
- Task: Represents individual task items
- Storage functions: Handle data persistence

Usage:
    Run the module directly to start the interactive CLI interface.
    Commands are entered at the prompt (:) and include:
    - Task operations (a/e/d/m)
    - View controls (l/f/s/clear)
    - System commands (q/w/help)

The interface automatically saves changes on quit and provides
emergency saving in case of errors.

KeyboardInterrupt handling prevents accidental exits and
provides guidance on proper quit procedure.

Dependencies:
- rich: For terminal formatting and display
- Custom kanban modules for board logic and storage
"""

try:
    from rich.console import Console
    from rich.prompt import Prompt
except ImportError:
    print("Rich is not installed.")
    print("Install it with pip or your package manager.")
    exit(1)
try:
    from kanban.board import KanbanBoard, COLUMN_HEADERS
    from kanban.storage import load_tasks, save_tasks
    from kanban.task import Task
    from kanban.task_operations import TaskOperator, TaskActionResult
    from kanban.category_colors import COLORS, save_category_colors
except ImportError:
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
    """
    Main application loop for the Kanban Board CLI.

    This function:
    1. Initializes the application state (loads tasks and colors)
    2. Renders the initial Kanban board
    3. Enters an interactive command loop that:
       - Processes user commands for task management
       - Handles board operations (filtering, sorting, layout changes)
       - Manages system functions (saving, quitting, help)
    4. Provides automatic board refreshes after each operation
    5. Handles errors gracefully with emergency saving

    The command loop supports:
    - Task operations:
      - Add (a), Edit (e), Delete (d), Move (m)
    - View controls:
      - Toggle layout (l), Filter (f), Sort (s), Clear filters (clear)
    - System commands:
      - Save (w), Quit (q), Help (help)
    - Advanced features:
      - Category color management (c)
      - Task search (/ or search)

    KeyboardInterrupt (Ctrl+C) is caught to prevent accidental exits.

    Returns:
        None: Runs indefinitely until user quits
    """
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
