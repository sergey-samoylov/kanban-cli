#!/usr/bin/env python3

import sys

try:
    import rich
except ImportError:
    print("❌ Rich is not installed.")
    print("Install with:")
    print("  pip install rich")
    print("Or if you're using system packages:")
    print("  sudo apt install python3-rich")
    sys.exit(1)

print("✅ Rich is installed.")

