import tkinter as tk
from tkinter import messagebox
import random
import time
import winsound  # Pour les effets sonores (Windows uniquement)

# Liste de mots à deviner
WORDS = [
    "python", "hangman", "developer", "algorithm", "machine", "learning", "fantastic",
    "programming", "artificial", "intelligence", "database", "network", "security",
    "hardware", "software", "interface", "compiler", "debugging", "encryption",
    "framework", "iteration", "variable", "function", "recursive", "optimization",
    "authentication", "cryptography", "virtualization", "processor", "bandwidth",
    "firewall", "protocol", "repository", "encryption", "operating", "multithreading"
]
MAX_ATTEMPTS = 6  # Nombre d'erreurs max

class HangmanGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Jeu du Pendu Fantastique")
        self.root.geometry("600x700")
        self.root.configure(bg="#1e1e2f")  # Fond sombre

        self.word_to_guess = random.choice(WORDS)
        self.guessed_letters = set()
        self.attempts = 0
        self.score = 0  # Score du joueur

        # Canvas pour dessiner le pendu
        self.canvas = tk.Canvas(root, width=300, height=300, bg="#2e2e4f", highlightthickness=0)
        self.canvas.pack(pady=20)

        # Dessiner la structure du pendu (base, poteau, barre, corde)
        self.draw_structure()

        # Label pour afficher le mot caché
        self.word_label = tk.Label(root, text=self.get_display_word(), font=("Arial", 28), fg="#ffffff", bg="#1e1e2f")
        self.word_label.pack(pady=10)

        # Zone d'entrée pour entrer une lettre
        self.letter_entry = tk.Entry(root, font=("Arial", 20), width=5, bg="#3e3e5f", fg="#ffffff", borderwidth=2)
        self.letter_entry.pack(pady=10)

        # Bouton pour valider la lettre
        self.guess_button = tk.Button(root, text="Proposer", font=("Arial", 16), command=self.check_letter,
                                     bg="#4e4e7f", fg="#ffffff", activebackground="#6e6e9f", activeforeground="#ffffff")
        self.guess_button.pack(pady=10)

        # Label pour afficher les lettres essayées
        self.tried_label = tk.Label(root, text="Lettres essayées : ", font=("Arial", 14), fg="#ffffff", bg="#1e1e2f")
        self.tried_label.pack(pady=10)

        # Label pour afficher le score
        self.score_label = tk.Label(root, text=f"Score : {self.score}", font=("Arial", 14), fg="#ffffff", bg="#1e1e2f")
        self.score_label.pack(pady=10)

        # Liste des étapes du pendu (uniquement le personnage)
        self.hangman_parts = [
            lambda: self.draw_head(),  # Tête
            lambda: self.draw_body(),  # Corps
            lambda: self.draw_left_arm(),  # Bras gauche
            lambda: self.draw_right_arm(),  # Bras droit
            lambda: self.draw_left_leg(),  # Jambe gauche
            lambda: self.draw_right_leg(),  # Jambe droite
        ]

        # Sons (remplacer par des fichiers WAV si disponibles)
        self.correct_sound = lambda: winsound.Beep(1000, 200)  # Son pour une bonne lettre
        self.wrong_sound = lambda: winsound.Beep(500, 200)  # Son pour une mauvaise lettre
        self.win_sound = lambda: winsound.Beep(1500, 500)  # Son pour la victoire
        self.lose_sound = lambda: winsound.Beep(200, 1000)  # Son pour la défaite

    def draw_structure(self):
        """Dessine la structure fixe du pendu (poteau, barre, corde)."""
        self.canvas.create_line(50, 250, 250, 250, width=3, fill="#ffffff")  # Base
        self.canvas.create_line(150, 50, 150, 250, width=3, fill="#ffffff")  # Poteau
        self.canvas.create_line(150, 50, 220, 50, width=3, fill="#ffffff")  # Barre horizontale
        self.canvas.create_line(220, 50, 220, 80, width=3, fill="#ffffff")  # Corde

    def draw_head(self):
        """Dessine la tête avec une animation."""
        for i in range(10):
            self.canvas.create_oval(200, 80 + i, 240, 120 + i, width=3, outline="#ffcc00")
            self.root.update()
            time.sleep(0.05)
            if i < 9:
                self.canvas.create_oval(200, 80 + i, 240, 120 + i, width=3, outline="#2e2e4f")

    def draw_body(self):
        """Dessine le corps avec une animation."""
        for i in range(10):
            self.canvas.create_line(220, 120 + i, 220, 180 + i, width=3, fill="#ffcc00")
            self.root.update()
            time.sleep(0.05)
            if i < 9:
                self.canvas.create_line(220, 120 + i, 220, 180 + i, width=3, fill="#2e2e4f")

    def draw_left_arm(self):
        """Dessine le bras gauche avec une animation."""
        for i in range(10):
            self.canvas.create_line(220 - i, 140 + i, 200 - i, 170 + i, width=3, fill="#ffcc00")
            self.root.update()
            time.sleep(0.05)
            if i < 9:
                self.canvas.create_line(220 - i, 140 + i, 200 - i, 170 + i, width=3, fill="#2e2e4f")

    def draw_right_arm(self):
        """Dessine le bras droit avec une animation."""
        for i in range(10):
            self.canvas.create_line(220 + i, 140 + i, 240 + i, 170 + i, width=3, fill="#ffcc00")
            self.root.update()
            time.sleep(0.05)
            if i < 9:
                self.canvas.create_line(220 + i, 140 + i, 240 + i, 170 + i, width=3, fill="#2e2e4f")

    def draw_left_leg(self):
        """Dessine la jambe gauche avec une animation."""
        for i in range(10):
            self.canvas.create_line(220 - i, 180 + i, 200 - i, 230 + i, width=3, fill="#ffcc00")
            self.root.update()
            time.sleep(0.05)
            if i < 9:
                self.canvas.create_line(220 - i, 180 + i, 200 - i, 230 + i, width=3, fill="#2e2e4f")

    def draw_right_leg(self):
        """Dessine la jambe droite avec une animation."""
        for i in range(10):
            self.canvas.create_line(220 + i, 180 + i, 240 + i, 230 + i, width=3, fill="#ffcc00")
            self.root.update()
            time.sleep(0.05)
            if i < 9:
                self.canvas.create_line(220 + i, 180 + i, 240 + i, 230 + i, width=3, fill="#2e2e4f")

    def get_display_word(self):
        """Affiche le mot caché avec les lettres trouvées."""
        return " ".join(letter if letter in self.guessed_letters else "_" for letter in self.word_to_guess)

    def check_letter(self):
        """Vérifie si la lettre entrée est correcte."""
        letter = self.letter_entry.get().lower()
        self.letter_entry.delete(0, tk.END)

        if not letter.isalpha() or len(letter) != 1:
            messagebox.showwarning("Erreur", "Veuillez entrer une seule lettre.")
            return

        if letter in self.guessed_letters:
            messagebox.showinfo("Déjà essayé", "Vous avez déjà essayé cette lettre.")
            return

        self.guessed_letters.add(letter)

        if letter in self.word_to_guess:
            self.correct_sound()
            self.word_label.config(text=self.get_display_word())
            self.score += 10  # Augmenter le score
            self.score_label.config(text=f"Score : {self.score}")
            if "_" not in self.get_display_word():
                self.win_sound()
                messagebox.showinfo("Gagné !", f"Félicitations ! Vous avez trouvé le mot : {self.word_to_guess}")
                self.root.quit()
        else:
            self.wrong_sound()
            if self.attempts < len(self.hangman_parts):
                self.hangman_parts[self.attempts]()  # Dessine une partie du personnage
                self.attempts += 1

            if self.attempts == MAX_ATTEMPTS:
                self.lose_sound()
                messagebox.showerror("Perdu", f"Vous avez perdu ! Le mot était : {self.word_to_guess}")
                self.root.quit()

        self.tried_label.config(text=f"Lettres essayées : {', '.join(self.guessed_letters)}")

if __name__ == "__main__":
    root = tk.Tk()
    game = HangmanGame(root)
    root.mainloop()