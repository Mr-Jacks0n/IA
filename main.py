import sys
from config import set_debug, debug_print
from interface.console import start_console
from interface.gui import start_gui

if __name__ == "__main__":
    if "--debug" in sys.argv:
        set_debug(True)
        debug_print("Mode Debug activé : Informations détaillées affichées.")
    
    if "--gui" in sys.argv:
        start_gui()
    else:
        start_console()