# 🧮 Terminal Kanban Board

A visually appealing **terminal-based Kanban board**  
powered by the [Rich](https://github.com/Textualize/rich) library.  

Tasks are organized in three statuses:   
**TODO**, **NOW**, and **DONE**,  
displayed either **horizontally or vertically**.

Each task belongs to a **custom category**,  
and each category is assigned a **unique color** for visual grouping.

Data is stored in a simple **CSV file**,  
and all configuration is handled with a **Python dictionary file**.

---

## 🛠 Features

- 📦 Three colored status columns: `TODO`, `NOW`, `DONE`
- 🗂 Tasks have `id`, `title`, `description`, `category`, `status`
- 🎨 Custom categories with persistent color assignment
- ⌨️ Vim-inspired commands like `:a`, `:m`, `:w`, `:q`
- 🧠 Intelligent ID reuse
- 🔁 Layout switching: vertical (default) or horizontal
- 🔍 Filtering, sorting, and searching tasks
- 🧹 Clean visual interface with bordered Rich panels

---

<img src="img/poster.png" alt="kanban-cli poster" width="70%">

---

## 🚀 Quickstart

```bash
pip install kanban-cli
# or
uv pip install kanban-cli
# then run it:
kanban
```

### 📦 Requirements

- Python 3.10+
- `rich` library

Install dependencies:

```bash
sudo apt install python3-rich
```
or

```bash
pip install rich
```

### ▶️ Run the app

```bash
python main.py
```

---

## ⌨️ Commands

| Command     | Description                       |
|-------------|-----------------------------------|
| `:a`        | Add a new task                    |
| `:m`        | Move a task to another status     |
| `:d`        | Delete a task                     |
| `:e`        | Edit a task                       |
| `:f`        | Filter tasks by status/category   |
| `:s`        | Sort tasks by ID, title, category |
| `:search`   | Search for text in tasks          |
| `:c`        | Change a category’s color         |
| `:layout`   | Switch layout (columns/rows)      |
| `:w`        | Save all changes                  |
| `:q`        | Quit                              |
| `:clear`    | Re-render the full board          |

---

## 📂 Project Structure

```
kanban/
├── main.py            # Entry point
├── board.py           # Kanban board rendering
├── task.py            # Task dataclass & logic
├── storage.py         # CSV load/save helpers
├── config.py          # Persistent config dict
├── config_utils.py    # Config manipulation utils
├── /db/tasks.csv      # Task database
├── README.md          # This README.md file
├── README_RU.md       # README in Russian
├── StyleGuide.md      # Code style guide for the project
```

---

## 📁 Configuration

All configuration (category colors, layout) is stored in `config.py` as a dictionary:

```python
CONFIG = {
    "category_colors": {
        "code": "cyan",
        "shop": "green",
    },
    "layout": "columns"
}
```

Colors are randomly assigned to new categories (avoiding duplicates), but can
be changed by the user with `:c`.

---

## 🧱 Scalability

- Designed to be modular and extensible.
- Easy to switch to JSON or database backend in future.
- Ready for multi-file/project/task view if needed.

---

## ❤️ Made with Rich

This app relies on the fantastic [Rich](https://github.com/Textualize/rich)
library for all terminal rendering — thank you, 
[Will McGugan](https://github.com/willmcgugan)!

---

## 📃 License

GNU General Public License.

---

