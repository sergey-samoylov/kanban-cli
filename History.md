# 🛠 The Story Behind the Terminal Kanban

## 💡 From Idea...

It all started with a simple but intriguing thought:  
**"What if I could build a Kanban board in the terminal?"**

No browsers, no graphical frameworks —  
**just pure Python, minimalism, and the beauty of the console**.

The goal was to build a tool that:
- starts instantly,
- is simple yet elegant,
- looks great in the terminal,
- is easy to expand and understand.

## 🧱 First Sketches

The foundation:
- Language: **Python 3.10+** (for `match case` and modern syntax),
- Visualization: **[Rich](https://github.com/Textualize/rich)**,
- Task storage: **CSV** — lightweight, readable, portable,
- Categories: assigned **unique colors**, dynamically.

The idea was simple... but as always, the devil was in the details.

## ⚙️ Architecture

From the beginning, the project was designed modularly:

- `task.py` — the `Task` class for representing and storing task data.
- `storage.py` — loading and saving tasks from/to CSV.
- `board.py` — the visual Kanban board built with Rich.
- `main.py` — the interactive CLI with Vim-inspired commands.
- `config.py` + `config_utils.py` — for storing user preferences like layout and category colors.

I planed to make each function clean, self-contained, and reusable.  
Every detail had a purpose.

## 🪄 Evolution and Improvements

Gradually, the project grew:

- 🎨 Color-coded categories with dynamic assignment and manual override.
- 🔄 Persistent user configuration across sessions.
- ↕ Switchable horizontal and vertical layouts.
- 🔍 Task filtering, searching, and sorting.
- ♻️  Smart ID management with gap-free ID reuse.
- 📦 A zipped project structure for easy sharing and launch.

The tool became something **enjoyable to use daily**.

## 🧭 Guiding Principles

The design was driven by values:

- **Readability** — code that reads like a story.
- **Modularity** — testable, extensible, clean.
- **Modern Python** — no legacy syntax.
- **Simplicity** — no bloat.
- **Flexibility** — ready for database backends or UI extensions.

## 📈 What’s Next?

This is just the beginning.  

Planned features include:
- Multi-project support.
- Importing tasks from GitHub or Trello.
- Rich TUI interface with Textual.
- Task import/export.
- Tags, priorities, deadlines.

---

**From idea to real working tool.**  
That’s how terminal Kanban in Python was born.

Author: Sergey Samoylov

