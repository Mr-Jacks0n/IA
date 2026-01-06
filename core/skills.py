import datetime
import webbrowser

def execute_command(command):
    if command == "get_time":
        return datetime.datetime.now().strftime("%H:%M")
    elif command == "open_browser":
        webbrowser.open("https://google.com")
        return "J'ai ouvert Google pour toi."
    return "Commande inconnue."