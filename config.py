# Configuration globale
DEBUG_MODE = False
VERSION = '1.3.1'

def set_debug(mode):
    global DEBUG_MODE
    DEBUG_MODE = mode

def debug_print(message):
    if DEBUG_MODE:
        print(f"[DEBUG] {message}")