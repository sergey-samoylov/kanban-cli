#!/usr/bin/env python3
"""
Kanban Board Visualization Module

Provides the KanbanBoard class for displaying tasks in a vertical or horizontal layout.
Handles task rendering, layout toggling, and help system display using Rich library.
"""

from rich.columns import Columns
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

from task import Task
from category_colors import load_category_colors


COLUMN_HEADERS = ["⏳TODO", "🔥NOW", "✨DONE"]

# In case you prefer main operators prompts at the bottom:
# OPERATORS = [
#     "a - add", "e - edit", "d - del", "m - move",
#     "s - sort", "w - save", "q - quit", "/ - find",
#     "l - layout"
# ]

# SHORTCUTS = ", ".join(OPERATORS)
# === minimal prompt needed: ===
SHORTCUTS = "h - help"


class KanbanBoard:
    """Main Kanban board visualization class.

    Handles task display in either vertical or horizontal layout,
    with support for toggling between views and displaying help information.
    """

    def __init__(self, tasks: list[Task], layout: str = "vertical") -> None:
        """Initialize the Kanban board with tasks and layout preference.

        Args:
            tasks: List of Task objects to display
            layout: Initial layout ("vertical" or "horizontal")
        """
        self.tasks = tasks
        self.console = Console()
        self.colors = load_category_colors()
        self.layout = layout  # Tracks current layout mode

    def toggle_layout(self):
        """Toggle between vertical and horizontal layout modes.
        
        Switches the layout and triggers an immediate re-render.
        """
        self.layout = "horizontal" if self.layout == "vertical" else "vertical"
        self.render()

    def render_help(self) -> None:
        """Render the interactive help screen with three panels.
        
        Displays:
        - Key commands (🔑 KEYS)
        - Available colors (🎨 COLORS)
        - Category information (🗂️ CAT)
        """
        help_data = {
            "🔑 KEYS": [
                "[cyan]a[/] - Add new task",
                "[cyan]c[/] - Change category color",
                "[cyan]d[/] - Delete task",
                "[cyan]e[/] - Edit task",
                "[cyan]m[/] - Move task between columns",
                "[cyan]s[/] - Sort tasks",
                "[cyan]w[/] - Save changes",
                "[cyan]q[/] - Quit/Back",
                "[cyan]/[/] - Search tasks",
                "[cyan]l[/] - Toggle layout"
            ],
            "🎨 COLORS": [
                "🔴red", 
                "🟢green", 
                "🟡yellow",
                "🔵blue", 
                "⚪white",
                "🟣magenta",
                "🥏cyan",
            ],
            "🗂️  CAT": [
                "Categories auto-created",
                "with task creation",
                "Colors assigned randomly",
                "but can be changed",
                "using 'c' command"
            ],
            "💡 LIFEHACKS": [
                "[cyan]clear[/] - restores kanban after filters",
                "[cyan]/word[/] - finds and displays tasks with the word",
                "Если забыл переключить раскладку:",
                "[cyan]ф[/] - works as 'add new task'",
                "[cyan]й[/] - works as 'quit'",
                "[cyan]ц[/] - works as 'write'",
            ],
        }

        panels = []

        for title, content in help_data.items():
            panel = Panel(
                "\n".join(content),
                title=title,
                title_align="left",
                border_style="bold blue",
                padding=(0, 1)
            )
            panels.append(panel)

        help_screen = Panel(
            Columns(panels, equal=True, expand=True),
            title="[bold cyan]🪢KANBAN",
            title_align="right",
            subtitle="created by [i]Sergey Samoylov[/i]",
            subtitle_align="left",
            border_style="bold blue"
        )
        
        self.console.clear()
        self.console.print(help_screen)


    def _create_column_panels(self):
        """Create Rich panels for each Kanban column (TODO/NOW/DONE).
        
        Returns:
            List of Rich Panel objects ready for layout rendering
        """
        columns = ["⏳TODO", "🔥NOW", "✨DONE"]
        panels = []

        for col in columns:
            match col:
                case "⏳TODO": border_style = "bold yellow"
                case "🔥NOW": border_style = "bold red"
                case "✨DONE": border_style = "bold green"

            items = [self.render_task(t) for t in self.tasks if t.status == col]
            content = Columns(items, expand=True) if items else "[dim]No tasks"

            panel = Panel(
                content,
                title=col,
                title_align="left",
                border_style=border_style,
                padding=(0, 1),
            )
            panels.append(panel)

        return panels

    def _calculate_vertical_widths(self):
        """Calculate optimal column widths for vertical layout.
        
        Returns:
            int: Calculated width for vertical columns
        """
        terminal_width = self.console.width
        min_col_width = 25
        max_col_width = max(35, terminal_width // 3)
        target_col_width = max(min_col_width, terminal_width // 3 - 3)
        return min(max_col_width, max(min_col_width, target_col_width))

    def render(self) -> None:
        """Main rendering method for the Kanban board.
        
        Handles both vertical and horizontal layouts by:
        1. Creating column panels
        2. Applying layout-specific formatting
        3. Displaying the final board
        """
        panels = self._create_column_panels()

        if self.layout == "vertical":
            # Apply vertical-specific width calculations
            width = self._calculate_vertical_widths()
            for panel in panels:
                panel.width = width

            board_content = Columns(
                panels,
                equal=False,
                expand=True,
                padding=0,
                column_first=True,
            )
        else:
            # horizontal layout uses full width
            for panel in panels:
                panel.width = self.console.width - 4

            board_content = Columns(panels, expand=True)

        board = Panel(
            board_content,
            title="[bold cyan]📌KANBAN",
            title_align="right",
            subtitle=f"[cyan]{SHORTCUTS} [yellow]({self.layout})[/yellow][/cyan]",
            subtitle_align="left",
            padding=(0, 1),
        )

        self.console.clear()
        self.console.print(board)

    def render_task(self, task: Task) -> Panel:
        """Render an individual task as a Rich Panel.
        
        Args:
            task: Task object to render
            
        Returns:
            Rich Panel containing the task's information
        """
        color = self.colors.get(task.category, "white")
        content = f"[b][black]{task.id}[/black][/b] {task.title} [i][blue]{task.description}[/blue][/i]"
        return Panel(
            content,
            title=task.category,
            border_style=color,
            padding=(0, 1),
        )
