"""Point d'entrée ARIA · console, GUI, debug, audit, stats.

L'import de tkinter est fait en *lazy* : sans tkinter installé, la
console fonctionne quand même (utile sur un serveur minimal).
"""
import sys

from config import set_debug, debug_print


def run_audit():
    from core.selfaudit import run_audit
    run_audit(verbose='--verbose' in sys.argv)


def run_stats():
    from core.memory import Memory
    from core.catalog import SkillCatalog
    m = Memory()
    c = SkillCatalog()
    print("ARIA · état")
    print(f"  mémoire   : {len(m.rules)} règles · {len(m.facts)} faits · "
          f"{len(m.context.get('recent', []))} échanges récents")
    print(f"  catalogue : {c.summary()}")


def main():
    if "--debug" in sys.argv:
        set_debug(True)
        debug_print("Mode Debug activé : Informations détaillées affichées.")
        debug_print("la trace de routage s'affiche avec --debug aussi")

    if "--audit" in sys.argv:
        run_audit()
        return

    if "--stats" in sys.argv:
        run_stats()
        return

    if "--gui" in sys.argv:
        try:
            import tkinter  # noqa: F401 (vérifie la présence de Tk)
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
