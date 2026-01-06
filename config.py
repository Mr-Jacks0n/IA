# Configuration globale
DEBUG_MODE = False

def set_debug(mode):
    global DEBUG_MODE
    DEBUG_MODE = mode

def debug_print(message):
    if DEBUG_MODE:
        print(f"[DEBUG] {message}")