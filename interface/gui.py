import tkinter as tk
from tkinter import scrolledtext, font as tkfont

from config import VERSION
from core.decision_engine import DecisionEngine
from core.memory import Memory, MemoryRefused
from learning.feedback import learn

# Charte : or de marque + fonds sombres, lisibilité d'abord.
_BRAND = "#bc9c22"
_BG = "#14171c"
_PANEL = "#1d2129"
_TEXT = "#e8e6df"


class GUIApp:
    def __init__(self, root):
        self.root = root
        self._face = tkfont.Font(family="DejaVu Sans", size=11)
        self._face_bold = tkfont.Font(family="DejaVu Sans", size=11,
                                      weight="bold")
        self._face_brand = tkfont.Font(family="DejaVu Sans", size=13,
                                       weight="bold")
        self._face_small = tkfont.Font(size=9)
        self._face_button = tkfont.Font(size=10)
        self.root = root
        self.root.title(f"ARIA v{VERSION} · Intelligence apprenante locale")
        self.root.geometry("640x480")
        self.root.minsize(520, 400)
        self.root.configure(bg=_BG)

        self.memory = Memory()
        self.engine = DecisionEngine(self.memory)

        # Barre de marque : or, nom + dispositif
        header = tk.Frame(root, bg=_BRAND)
        header.pack(fill=tk.X)
        tk.Label(header, text=f" ARIA v{VERSION}",
                 bg=_BRAND, fg="#1a1a1a", font=self._face_brand).pack(
            side=tk.LEFT, padx=(10, 6), pady=6)
        tk.Label(header, text="IA symbolique · mémoire locale · "
                              "aucun cloud",
                 bg=_BRAND, fg="#3a3000",
                 font=self._face_button).pack(side=tk.LEFT, pady=6)

        # Zone de chat : sombre, messages dosés par émetteur
        self.chat_area = scrolledtext.ScrolledText(
            root, wrap=tk.WORD, state='disabled', bg=_PANEL, fg=_TEXT,
            font=self._face, relief=tk.FLAT)
        self.chat_area.pack(padx=8, pady=(8, 4), fill=tk.BOTH, expand=True)
        self.chat_area.tag_config("aria_label", foreground=_BRAND,
                                  font=self._face_bold)
        self.chat_area.tag_config("user_label", foreground="#7fb4ff",
                                  font=self._face_bold)
        self.chat_area.tag_config("dim", foreground="#8a8f98")

        # Barre d'état : route gagnante du dernier tour
        self.status = tk.Label(root, text="prête", bg=_BG, fg="#8a8f98",
                               anchor='w', font=self._face_small)
        self.status.pack(fill=tk.X, padx=10)

        # Zone de saisie + boutons : alignement propre sur la ligne
        bottom = tk.Frame(root, bg=_BG)
        bottom.pack(fill=tk.X, padx=8, pady=(4, 8))
        self.entry = tk.Entry(bottom, font=self._face, bg=_PANEL, fg=_TEXT,
                              relief=tk.FLAT)
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=True,
                        ipady=6, padx=(0, 6))
        self.entry.bind("<Return>", self.send_message)
        self.entry.focus_set()

        tk.Button(bottom, text="Effacer", command=self.clear_chat,
                  bg=_PANEL, fg=_TEXT, relief=tk.FLAT,
                  font=self._face_button).pack(side=tk.LEFT, padx=4)
        tk.Button(bottom, text="Envoyer", command=self.send_message,
                  bg=_BRAND, fg="#1a1a1a", relief=tk.FLAT,
                  font=self._face_bold).pack(side=tk.LEFT)

        # Message d'accueil
        self.display_message(
            "ARIA",
            "Bonjour ! Je suis ARIA, une intelligence apprenante.\n"
            "Demandez : heure, calendrier, conversions, tâches, tirages, "
            "recherche web · ou apprenez-moi en corrigeant.")

    # ── tour de dialogue ─────────────────────────────────────────
    def send_message(self, event=None):
        user_input = self.entry.get().strip()
        if not user_input:
            return
        self.entry.delete(0, tk.END)
        self.display_message("Toi", user_input)

        if user_input.lower() == "exit":
            self.display_message("ARIA", "Au revoir ! Contexte sauvegardé.")
            self.memory.save_context()
            self.root.quit()
            return

        response, route = self.engine.find_best_match(user_input)
        self.status.configure(text=self.engine.last_trace[0]
                              if self.engine.last_trace else "prête")

        if response:
            self.display_message("ARIA", response)
            # Feedback seulement pour les règles apprises / inconnues
            if route in ("rules.fuzzy", None):
                self.ask_feedback(user_input)
        else:
            self.display_message(
                "ARIA", "Je ne sais pas encore répondre à cela. "
                        "Apprends-moi.")
            self.ask_feedback(user_input)

    def clear_chat(self):
        self.chat_area.config(state='normal')
        self.chat_area.delete("1.0", tk.END)
        self.chat_area.config(state='disabled')

    # ── feedback (règles apprises seulement) ─────────────────────
    def ask_feedback(self, user_input):
        feedback_window = tk.Toplevel(self.root)
        feedback_window.title("Feedback")
        feedback_window.geometry("320x150")
        feedback_window.configure(bg=_BG)
        feedback_window.transient(self.root)

        tk.Label(feedback_window, text="Réponse correcte ?", bg=_BG,
                 fg=_TEXT).pack(pady=12)

        def yes():
            feedback_window.destroy()

        def no():
            feedback_window.destroy()
            correction_window = tk.Toplevel(self.root)
            correction_window.title("Correction")
            correction_window.geometry("320x110")
            correction_window.configure(bg=_BG)
            correction_window.transient(self.root)

            tk.Label(correction_window, text="Quelle serait la bonne "
                                            "réponse ?", bg=_BG,
                     fg=_TEXT).pack(pady=8)
            correction_entry = tk.Entry(correction_window, bg=_PANEL,
                                        fg=_TEXT, relief=tk.FLAT)
            correction_entry.pack(pady=6, padx=12, fill=tk.X, ipady=4)
            correction_entry.focus_set()

            def submit():
                correction = correction_entry.get().strip()
                if correction:
                    try:
                        learn(self.memory, user_input.lower(), correction)
                        self.display_message(
                            "ARIA", f"Merci ! J'ai appris : "
                                    f"'{user_input}' -> '{correction}'")
                    except MemoryRefused as exc:
                        self.display_message("ARIA", f"⛔ Refusé : {exc}")
                correction_window.destroy()

            tk.Button(correction_window, text="Apprendre",
                      bg=_BRAND, fg="#1a1a1a", relief=tk.FLAT,
                      command=submit).pack(pady=8)

        tk.Button(feedback_window, text="Oui", bg=_PANEL, fg=_TEXT,
                  relief=tk.FLAT, command=yes
                  ).pack(side=tk.LEFT, padx=24, pady=6)
        tk.Button(feedback_window, text="Non", bg=_PANEL, fg=_TEXT,
                  relief=tk.FLAT, command=no
                  ).pack(side=tk.RIGHT, padx=24, pady=6)

    # ── affichage ────────────────────────────────────────────────
    def display_message(self, sender, message):
        label = "user_label" if sender == "Toi" else "aria_label"
        self.chat_area.config(state='normal')
        self.chat_area.insert(tk.END, f"{sender}: ", label)
        self.chat_area.insert(tk.END, f"{message}\n")
        if "\n" in str(message):
            self.chat_area.insert(tk.END, "\n")
        self.chat_area.config(state='disabled')
        self.chat_area.see(tk.END)


def start_gui():
    root = tk.Tk()
    GUIApp(root)
    root.mainloop()
