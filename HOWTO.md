Let's run it 

- without pipx,
- without cluttering your system Python, 
- and with a smooth CLI experience.

---

## ✅ Plan: Create a *dedicated venv* + install with `uv` + shell wrapper

> ✔️ Create a venv in a fixed folder  
> ✔️ `uv pip install kanban-cli` there  
> ✔️ Use a wrapper script to auto-activate and run  
> ✔️ Forget it's a venv — it "just works"  

---

## 🧰 Step-by-step setup

### 1. Create a dedicated virtual environment

You can pick a permanent location, e.g. `~/.venvs/kanban`:

```bash
uv venv ~/.venvs/kanban
```

That’s your isolated Python env just for `kanban`.  
Install other Python apps in dedicated folders the same way.

---

### 2. Install kanban-cli app inside that venv

```bash
uv pip install --python ~/.venvs/kanban/bin/python kanban-cli
```

After that, you’ll find the actual binary here:

```bash
~/.venvs/kanban/bin/kanban
```

---

### 3. Create a wrapper script to run it globally

Create a new script in `~/.local/bin/kanban` (or any dir in your `$PATH`):

```bash
mkdir -p ~/.local/bin
nano ~/.local/bin/kanban
```

Paste this in:

```bash
#!/bin/bash
source ~/.venvs/kanban/bin/activate
exec kanban "$@"
```

Then make it executable:

```bash
chmod +x ~/.local/bin/kanban
```

✅ Now you can just run:
```bash
kanban
```

from **anywhere**, and it will:
- Activate the venv silently
- Run `kanban`
- Deactivate automatically when done (see below)

---

## 🔄 What about **deactivation**?

Good news: the virtual environment **doesn’t stay active**.

- You're using a script that activates, runs one command, and exits.
- Once `kanban` finishes, the shell wrapper exits — venv is implicitly "deactivated."
- Your terminal session remains untouched.

So there’s no need for `deactivate` — this is safe and self-contained.

---

## ✅ Summary

| Step                     | Command                                                |
|--------------------------|--------------------------------------------------------|
| Create venv              | `uv venv ~/.venvs/kanban`                             |
| Install in venv          | `~/.venvs/kanban/bin/uv pip install kanban-cli`       |
| Create shell wrapper     | `~/.local/bin/kanban` with auto-activate code         |
| Make executable          | `chmod +x ~/.local/bin/kanban`                        |
| Run from anywhere        | `kanban` ✅                                            |

---

## 🐍 And one more little thing...

You can run it from Python REPL.  
Here's a recipe:

- clone kanban-cli to a directory (Example: ~/Dev)
- create, if you don't have it already, .pythonstartup file at /home/your_user/
- add these lines to your .pythonstartup file:

```python
#!/usr/bin/env python3                                                                       
import sys 

from pathlib import Path

# Add your project directory to sys.path
sys.path.append(str(Path.home() / "Dev" / "kanban-cli"))

# Import the CLI main function
try:
    from kanban import main
    kanban = main.main
except Exception as e:
    print(f"⚠ Could not load kanban CLI: {e}")
```

- start Python REPL and enjoy

```
>>> kanban()
```

💡 Note:  

All your tasks are kept in your ~/.local/share/kanban-cli/db directory.

So, you can access it now any way you like: from bash or from python
