#   ___                      _                                             
#  |   \    ___    _ __     (_)    _ _      ___    _  _      _ _     o O O 
#  | |) |  / -_)  | '  \    | |   | ' \    / -_)  | +| |    | '_|   o      
#  |___/   \___|  |_|_|_|  _|_|_  |_||_|   \___|   \_,_|   _|_|_   TS__[O] 
#_|"""""|_|"""""|_|"""""|_|"""""|_|"""""|_|"""""|_|"""""|_|"""""| {======| 
#"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'./o--000' 


import tkinter as tk
import tkinter.messagebox
import random

class Demineur(tk.Tk):
    def __init__(self, size=10, num_mines=10):
        super().__init__()

        self.size = size
        self.num_mines = num_mines
        self.title("Démineur")
        self.configure(bg="#2E2E2E")  # Couleur de fond sombre
        self.is_fullscreen = False  # Variable pour suivre l'état du plein écran
        self.cheat_mode = False  # État du mode triche

        # Initialisation des variables
        self.create_variables()
        self.create_widgets()
        self.place_mines()
        self.calculate_mine_counts()

    def create_variables(self):
        self.buttons = [[None for _ in range(self.size)] for _ in range(self.size)]
        self.board = [[0 for _ in range(self.size)] for _ in range(self.size)]
        self.mines = set()
        self.revealed = [[False for _ in range(self.size)] for _ in range(self.size)]
        self.flags = [[False for _ in range(self.size)] for _ in range(self.size)]
        self.game_over = False
        self.remaining_mines = self.num_mines
        self.time_elapsed = 0  # Chronomètre
        self.timer_running = False  # État du chronomètre

        # Lier la touche F11 pour activer/désactiver le mode plein écran
        self.bind("<F11>", self.toggle_fullscreen)

    def create_widgets(self):
        # Titre cliquable pour activer/désactiver le mode triche
        self.title_label = tk.Label(self, text="Démineur", font=("Helvetica", 24), bg="#2E2E2E", fg="white")
        self.title_label.grid(row=0, columnspan=self.size)
        self.title_label.bind("<Button-1>", self.toggle_cheat_mode)  # Clic gauche pour activer la triche

        # Frame pour contenir le chronomètre et le compteur de bombes
        self.info_frame = tk.Frame(self, bg="#2E2E2E")
        self.info_frame.grid(row=self.size + 1, columnspan=self.size, pady=10)

        # Chronomètre
        self.timer_label = tk.Label(self.info_frame, text='⏱️ 0', font=("Helvetica", 16), bg="#2E2E2E", fg="#FFFFFF")
        self.timer_label.pack(side=tk.LEFT, padx=20)

        # Compteur de bombes moderne
        self.bomb_counter = tk.Label(self.info_frame, text=f'💣 {self.remaining_mines}', font=("Helvetica", 16), bg="#2E2E2E", fg="#FF4136")
        self.bomb_counter.pack(side=tk.RIGHT, padx=20)

        # Boutons supplémentaires
        self.restart_button = tk.Button(self, text="Rejouer", command=self.reset_game, font=("Helvetica", 12), bg="#4CAF50", fg="white", borderwidth=0)
        self.restart_button.grid(row=self.size + 2, column=0, columnspan=self.size//2, sticky="ew", padx=5, pady=5)

        self.difficulty_button = tk.Button(self, text="Changer la difficulté", command=self.back_to_difficulty_selection, font=("Helvetica", 12), bg="#f44336", fg="white", borderwidth=0)
        self.difficulty_button.grid(row=self.size + 2, column=self.size//2, columnspan=self.size//2, sticky="ew", padx=5, pady=5)

        for i in range(self.size):
            for j in range(self.size):
                button = tk.Button(self, text='', width=3, height=1, font=("Helvetica", 12), bg="#DDDDDD", command=lambda x=i, y=j: self.reveal_square(x, y), borderwidth=1, relief="raised")
                button.bind("<Button-3>", lambda event, x=i, y=j: self.toggle_flag(x, y))  # Clic droit pour le drapeau
                button.grid(row=i + 1, column=j, sticky="nsew")
                self.buttons[i][j] = button

        # Rendre les lignes et colonnes réactives
        for i in range(self.size):
            self.grid_rowconfigure(i + 1, weight=1)
            self.grid_columnconfigure(i, weight=1)

    def place_mines(self):
        while len(self.mines) < self.num_mines:
            x = random.randint(0, self.size - 1)
            y = random.randint(0, self.size - 1)
            if (x, y) not in self.mines:
                self.mines.add((x, y))
                self.board[x][y] = -1  # -1 représente une mine

    def calculate_mine_counts(self):
        for x in range(self.size):
            for y in range(self.size):
                if self.board[x][y] == -1:
                    continue
                count = 0
                for i in range(max(0, x - 1), min(self.size, x + 2)):
                    for j in range(max(0, y - 1), min(self.size, y + 2)):
                        if (i, j) in self.mines:
                            count += 1
                self.board[x][y] = count

    def reveal_square(self, x, y):
        if self.game_over or self.revealed[x][y] or self.flags[x][y]:
            return

        self.revealed[x][y] = True
        
        if not self.timer_running:  # Démarrer le chronomètre au premier clic
            self.start_timer()

        if (x, y) in self.mines:
            self.buttons[x][y].config(text='💥', bg='red', fg='white')
            self.game_over = True
            self.end_game("Vous avez perdu !")
            return
        
        # Ajuste la couleur du texte selon la valeur de la case
        if self.board[x][y] == 0:
            self.buttons[x][y].config(text='', bg='lightgreen')  # Couleur pour les cases découvertes sans mines
        else:
            self.buttons[x][y].config(text=str(self.board[x][y]), bg='lightgreen', fg='black')  # Couleur pour les cases découvertes avec mines

        if self.board[x][y] == 0:
            self.reveal_surrounding_squares(x, y)

        # Vérifie si le joueur a gagné
        if self.check_win_condition():
            self.end_game("Vous avez gagné !")

        # Afficher toutes les mines si le mode triche est activé
        if self.cheat_mode:
            self.show_all_mines()

    def reveal_surrounding_squares(self, x, y):
        for i in range(max(0, x - 1), min(self.size, x + 2)):
            for j in range(max(0, y - 1), min(self.size, y + 2)):
                self.reveal_square(i, j)

    def toggle_flag(self, x, y):
        if self.game_over or self.revealed[x][y]:
            return
        
        if self.flags[x][y]:
            self.flags[x][y] = False
            self.buttons[x][y].config(text='', bg="#DDDDDD")  # Réinitialise la couleur de fond
            self.remaining_mines += 1
        else:
            if self.remaining_mines > 0:
                self.flags[x][y] = True
                self.buttons[x][y].config(text='🚩', bg='#FFC107', fg='black', font=("Helvetica", 12))  # Changement de couleur et de style du drapeau
                self.remaining_mines -= 1
        
        self.update_bomb_counter()

        # Vérifie si le joueur a gagné
        if self.check_win_condition():
            self.end_game("Vous avez gagné !")

    def update_bomb_counter(self):
        self.bomb_counter.config(text=f'💣 {self.remaining_mines}')

    def start_timer(self):
        self.timer_running = True
        self.update_timer()

    def update_timer(self):
        if self.game_over:
            return
        self.time_elapsed += 1
        self.timer_label.config(text=f'⏱️ {self.time_elapsed}')
        self.after(1000, self.update_timer)  # Appelle cette méthode toutes les secondes

    def end_game(self, message):
        self.timer_running = False  # Arrêter le chronomètre
        for x, y in self.mines:
            if not self.revealed[x][y]:
                self.buttons[x][y].config(text='💣', bg='red', fg='white')
        for row in self.buttons:
            for button in row:
                button.config(state='disabled')

        # Créer une nouvelle fenêtre pour le message de fin de jeu
        end_game_window = tk.Toplevel(self)  # Utiliser Toplevel pour créer une nouvelle fenêtre
        end_game_window.title("Fin de la partie")
        end_game_window.configure(bg="#282c34")  # Fond sombre
        end_game_window.geometry("300x200")  # Taille de la fenêtre

        # Message de fin de jeu
        message_label = tk.Label(end_game_window, text=message, font=("Helvetica", 16, "bold"), bg="#282c34", fg="#ffffff")
        message_label.pack(pady=20)

        # Bouton de redémarrage
        restart_button = tk.Button(end_game_window, text="Rejouer", command=self.reset_game, bg="#4CAF50", fg="white", font=("Helvetica", 12), borderwidth=0, relief="flat", padx=10, pady=5)
        restart_button.pack(pady=5)

        # Bouton de changement de difficulté
        difficulty_button = tk.Button(end_game_window, text="Changer la difficulté", command=self.back_to_difficulty_selection, bg="#FFC107", fg="black", font=("Helvetica", 12), borderwidth=0, relief="flat", padx=10, pady=5)
        difficulty_button.pack(pady=5)

        # Bouton de fermeture
        close_button = tk.Button(end_game_window, text="Quitter", command=self.destroy, bg="#F44336", fg="white", font=("Helvetica", 12), borderwidth=0, relief="flat", padx=10, pady=5)
        close_button.pack(pady=10)

        end_game_window.mainloop()



    def toggle_cheat_mode(self, event=None):
        self.cheat_mode = not self.cheat_mode
        if self.cheat_mode:
            self.title_label.config(text="Démineur (Triche activée)", fg="yellow")
            self.show_all_mines()  # Afficher toutes les mines lorsque le mode triche est activé
        else:
            self.title_label.config(text="Démineur", fg="white")
            self.hide_mines()  # Masquer les mines lorsque le mode triche est désactivé

    def show_all_mines(self):
        for x, y in self.mines:
            if not self.revealed[x][y]:
                self.buttons[x][y].config(text='💣', bg='red', fg='white')

    def hide_mines(self):
        for x, y in self.mines:
            if not self.revealed[x][y]:
                self.buttons[x][y].config(text='', bg="#DDDDDD")

    def reset_game(self):
        # Rejouer avec les mêmes paramètres
        self.destroy()
        new_game = Demineur(size=self.size, num_mines=self.num_mines)
        new_game.is_fullscreen = self.is_fullscreen  # Réappliquer l'état plein écran
        new_game.mainloop()

    def toggle_fullscreen(self, event=None):
        self.is_fullscreen = not self.is_fullscreen
        self.attributes("-fullscreen", self.is_fullscreen)

    def back_to_difficulty_selection(self):
        # Retourner à l'écran de sélection de la difficulté
        self.destroy()
        show_difficulty_selection()

    def check_win_condition(self):
        # Vérifie si toutes les cases non-minées sont révélées ou si toutes les mines sont correctement marquées
        non_mined_revealed = sum(1 for x in range(self.size) for y in range(self.size) if self.revealed[x][y] and (x, y) not in self.mines)
        all_mines_flagged = all(self.flags[x][y] for x, y in self.mines)
        
        # Vérification des conditions de victoire
        return non_mined_revealed == (self.size * self.size - self.num_mines) or all_mines_flagged

def show_difficulty_selection():
    # Fenêtre de sélection du niveau de difficulté
    def start_game(difficulty):
        size, num_mines = difficulty
        difficulty_window.destroy()  # Ferme la fenêtre de sélection
        new_game = Demineur(size=size, num_mines=num_mines)  # Lance le nouveau jeu avec les paramètres
        new_game.mainloop()

    difficulty_window = tk.Tk()
    difficulty_window.title("Choisissez un niveau")
    difficulty_window.configure(bg="#2E2E2E")

    tk.Label(difficulty_window, text="Choisissez un niveau de difficulté", font=("Helvetica", 14), bg="#2E2E2E", fg="#FFFFFF").pack(pady=10)

    # Boutons pour choisir la difficulté
    tk.Button(difficulty_window, text="Facile (8x8, 10 mines)", command=lambda: start_game((8, 10)), bg="#4CAF50", fg="white", font=("Helvetica", 12)).pack(pady=5)
    tk.Button(difficulty_window, text="Moyen (12x12, 20 mines)", command=lambda: start_game((12, 20)), bg="#FFC107", fg="black", font=("Helvetica", 12)).pack(pady=5)
    tk.Button(difficulty_window, text="Difficile (16x16, 40 mines)", command=lambda: start_game((16, 40)), bg="#F44336", fg="white", font=("Helvetica", 12)).pack(pady=5)

    difficulty_window.mainloop()

if __name__ == "__main__":
    show_difficulty_selection()
