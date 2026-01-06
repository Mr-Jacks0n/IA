import tkinter as tk
from tkinter import scrolledtext
from core.decision_engine import DecisionEngine
from core.memory import Memory
from learning.feedback import learn

class GUIApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ARIA - Intelligence Apprenante")
        self.root.geometry("600x400")
        
        self.memory = Memory()
        self.engine = DecisionEngine(self.memory)
        
        # Zone de chat
        self.chat_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, state='disabled')
        self.chat_area.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
        
        # Zone d'entrée
        self.entry = tk.Entry(root, font=("Arial", 12))
        self.entry.pack(pady=5, padx=10, fill=tk.X)
        self.entry.bind("<Return>", self.send_message)
        
        # Bouton envoyer
        self.send_button = tk.Button(root, text="Envoyer", command=self.send_message)
        self.send_button.pack(pady=5)
        
        # Message d'accueil
        self.display_message("ARIA", "Bonjour ! Je suis ARIA, une intelligence apprenante. Comment puis-je t'aider ?")
    
    def send_message(self, event=None):
        user_input = self.entry.get().strip()
        if not user_input:
            return
        self.entry.delete(0, tk.END)
        
        self.display_message("Toi", user_input)
        
        if user_input.lower() == "exit":
            self.display_message("ARIA", "Au revoir !")
            self.root.quit()
            return
        
        response, key = self.engine.find_best_match(user_input)
        
        if response:
            self.display_message("ARIA", response)
            # Feedback seulement pour les réponses apprises
            if key not in ["logic_event", "advanced_reasoning"] and not response.startswith("Le résultat est"):
                self.ask_feedback(user_input)
        else:
            self.display_message("ARIA", "Je ne sais pas encore répondre à cela. Apprends-moi.")
            self.ask_feedback(user_input)
    
    def ask_feedback(self, user_input):
        feedback_window = tk.Toplevel(self.root)
        feedback_window.title("Feedback")
        feedback_window.geometry("300x150")
        
        tk.Label(feedback_window, text="Réponse correcte ?").pack(pady=10)
        
        def yes():
            feedback_window.destroy()
        
        def no():
            feedback_window.destroy()
            correction_window = tk.Toplevel(self.root)
            correction_window.title("Correction")
            correction_window.geometry("300x100")
            
            tk.Label(correction_window, text="Quelle serait la bonne réponse ?").pack(pady=5)
            correction_entry = tk.Entry(correction_window)
            correction_entry.pack(pady=5)
            
            def submit():
                correction = correction_entry.get().strip()
                if correction:
                    learn(self.memory, user_input.lower(), correction)
                    self.display_message("ARIA", f"Merci ! J'ai appris : '{user_input}' -> '{correction}'")
                correction_window.destroy()
            
            tk.Button(correction_window, text="Apprendre", command=submit).pack(pady=5)
        
        tk.Button(feedback_window, text="Oui", command=yes).pack(side=tk.LEFT, padx=20)
        tk.Button(feedback_window, text="Non", command=no).pack(side=tk.RIGHT, padx=20)
    
    def display_message(self, sender, message):
        self.chat_area.config(state='normal')
        self.chat_area.insert(tk.END, f"{sender}: {message}\n")
        self.chat_area.config(state='disabled')
        self.chat_area.see(tk.END)

def start_gui():
    root = tk.Tk()
    app = GUIApp(root)
    root.mainloop()