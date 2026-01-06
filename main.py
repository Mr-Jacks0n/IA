import sys
from interface.console import start_console
from interface.gui import start_gui

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--gui":
        start_gui()
    else:
        start_console()