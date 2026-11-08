"""Point d'entrée ARIA — console, GUI, debug.

L'import de tkinter est fait en *lazy* : sans tkinter installé, la
console fonctionne quand même (utile sur un serveur minimal).
"""
import sys
from config import set_debug, debug_print


def main():
    if "--debug" in sys.argv:
        set_debug(True)
        debug_print("Mode Debug activé : Informations détaillées affichées.")

    if "--gui" in sys.argv:
        try:
            import tkinter  # noqa: F401  (vérifie la présence de Tk)
        except ImportError:
            sys.stderr.write(
                "[GUI indisponible] tkinter n'est pas installé.\n"
                " Debian/Ubuntu :  sudo apt install python3-tk\n"
                " Fedora        :  sudo dnf install python3-tkinter\n")
            sys.exit(2)
        from interface.gui import start_gui
        start_gui()
    else:
        from interface.console import start_console
        start_console()


if __name__ == "__main__":
    main()
