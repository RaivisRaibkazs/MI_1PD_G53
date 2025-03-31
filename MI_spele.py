import random
import tkinter as tk
from tkinter import messagebox, simpledialog

class NumberGame:
    def __init__(self, master):
        self.master = master
        master.title("Skaitļu secības spēle")
        master.geometry("600x500")
        master.configure(bg='#D6F5BB')

        # Spēles starta parametri (uzdevumā rakstīts, ka banka sākas ar 1)
        self.sequence = []
        self.points = 0
        self.bank = 1
        self.first_player = 1
        self.player_turn = 1

        # Šeit tiek veidots UI
        self.create_widgets()

    def create_widgets(self):
        # Spēles nosaukums un fonts
        self.title_label = tk.Label(
            self.master, 
            text="Skaitļu secības spēle", 
            font=('Arial', 16, 'bold'), 
            bg='#D6F5BB'
        )
        # Mūsu grupa (izveidotāji)
        self.title_label.pack(pady=1)
        self.title_label = tk.Label(
            self.master, 
            text="Šo spēli izstrādāja 53. grupas 2. kursa studenti no RTU IT fakultātes.", 
            font=('Arial', 10, 'bold'), 
            bg='#D6F5BB'
        )
        self.title_label.pack(pady=5)

        # Virknes izveides logs, izveide
        self.sequence_frame = tk.Frame(self.master, bg='#D6F5BB')
        # Tiks aizpildīts vēlāk

        self.sequence_label = tk.Label(
            self.sequence_frame, 
            text="Secība: ", 
            font=('Arial', 12), 
            bg='#D6F5BB'
        )
        self.sequence_label.pack(side=tk.LEFT)

        self.sequence_display = tk.Label(
            self.sequence_frame, 
            text="", 
            font=('Arial', 12, 'bold'), 
            relief=tk.SUNKEN, 
            padx=10, 
            pady=5
        )
        self.sequence_display.pack(side=tk.LEFT)

        # Punkti un banka
        self.score_frame = tk.Frame(self.master, bg='#D6F5BB')
        self.score_frame.pack(pady=10)

        self.points_label = tk.Label(
            self.score_frame, 
            text="Punkti: 0", 
            font=('Arial', 12), 
            bg='#D6F5BB'
        )
        self.points_label.pack(side=tk.LEFT, padx=10)

        self.bank_label = tk.Label(
            self.score_frame, 
            text="Banka: 1", 
            font=('Arial', 12), 
            bg='#D6F5BB'
        )
        self.bank_label.pack(side=tk.LEFT, padx=10)

        # Pogas
        self.buttons_frame = tk.Frame(self.master, bg='#D6F5BB')
        self.buttons_frame.pack(pady=10)

        # Spēles starta poga
        self.start_button = tk.Button(
            self.buttons_frame, 
            text="Sākt jaunu spēli", 
            command=self.start_game, 
            font=('Arial', 12),
            bg='#86942A'
        )
        self.start_button.pack(side=tk.LEFT, padx=10)

        # Darbības
        self.log_frame = tk.Frame(self.master, bg='#D6F5BB')
        self.log_frame.pack(pady=10)

        self.log_label = tk.Label(
            self.log_frame, 
            text="Noklikšķiniet uz 'Sākt jaunu spēli', lai sāktu spēli.", 
            font=('Arial', 10), 
            bg='#D6F5BB', 
            wraplength=500
        )
        self.log_label.pack()

        # Datora gājiena attēlošana
        self.ai_move_label = tk.Label(
            self.log_frame,
            text="",
            font=('Arial', 12, 'bold'),
            fg='#9C0000',  # Sarkana krāsa lai vieglāk pamanīt
            bg='#D6F5BB',
            wraplength=500
        )
        self.ai_move_label.pack(pady=5)

    def start_game(self):
        # Vaicājums lai iegūtu spēles sākuma skaitļus
        length = simpledialog.askinteger(
            "Spēles izveide", 
            "Ievadiet virknes garumu (15-20):", 
            minvalue=15, 
            maxvalue=20
        )
        if length is None:
            return

        first_player = simpledialog.askinteger(
            "Spēles izveide", 
            "Kas sāk? (1 = Spēlētājs, 2 = Dators):", 
            minvalue=1, 
            maxvalue=2
        )
        if first_player is None:
            return

        # Sākam spēli
        self.sequence = self.generate_sequence(length)
        self.points = 0
        self.bank = 1
        self.first_player = first_player
        self.player_turn = first_player

        # Attēlojam skaitļu virkni pēc spēlētāja gājiena
        self.sequence_frame.pack(pady=10)
        
        # Notīram datora gājiena rezultāta paziņojumu (to kas sarkans)
        self.ai_move_label.config(text="")
        
        # atjaunojam UI logu
        self.update_ui()
        
        # Ja spēli sāk spēlētājs, izveidojam ciparu pogas
        if self.player_turn == 1:
            self.create_number_buttons()
        # Ja spēli sāk dators, piešķiram tam gājienu
        else:
            self.ai_turn()

    def generate_sequence(self, length):
        return [random.choice([1, 2, 3, 4]) for _ in range(length)]

    def update_ui(self):
        # Atjaunojam ciparu virkni
        self.sequence_display.config(text=' '.join(map(str, self.sequence)))
        
        # Atjaunojam punktu un bankas rezultātus
        self.points_label.config(text=f"Punkti: {self.points}")
        self.bank_label.config(text=f"Banka: {self.bank}")
        
        # Parādam kuram spēlētājam ir gājiens
        self.log_label.config(text=f"{'Spēlētāja' if self.player_turn == 1 else 'Datora'} gājiens")

    def player_move(self, number):
        if number not in self.sequence:
            messagebox.showerror("Nepareizs gājiens", "Izvēlaties ciparu kas ir virknē.")
            return

        # Izņemam ciparu no virknes
        self.sequence.remove(number)

        # Apstrādājam ciparus kurus var sadalīt
        if number == 2:
            response = messagebox.askyesno("Darbības izvēle", "Vai vēlaties sadalīt '2' uz '1' un '1'?")
            if response:
                self.bank += 1
                self.sequence += [1, 1]
            else:
                self.points += 2
        elif number == 4:
            response = messagebox.askyesno("Darbības izvēle", "Vai vēlaties sadalīt '4' uz '2' un '2'?")
            if response:
                self.points += 2
                self.sequence += [2, 2]
            else:
                self.points += 4
        else:
            self.points += number

        # Notīram datora paziņojumu kad pienāk spēlētāja gājiens
        self.ai_move_label.config(text="")

        # Pārbaudam vai spēle ir beigusies
        if not self.sequence:
            self.end_game()
            return

        # Pārejam uz datora gājienu
        self.player_turn = 2
        self.update_ui()
        self.master.after(1000, self.ai_turn)

    def ai_turn(self):
        if not self.sequence:
            self.end_game()
            return

        move = self.ai_move(self.sequence.copy(), self.points, self.bank, self.first_player)
        self.sequence.remove(move[0])

        # Izveidojam paziņojumu par datora gājienu
        if move[1]:  # Ja dators sadalīja skaitli
            if move[0] == 2:
                self.bank += 1
                ai_message = f"Dators izvēlējās skaitli {move[0]} un sadalīja to, lai pievienotu 1 bankai"
            elif move[0] == 4:
                self.points += 2
                ai_message = f"Dators izvēlējās skaitli {move[0]} un sadalīja to, lai pievienotu 2 punktus"
        else:  # dators nesadalīja skaitli
            self.points += move[0]
            ai_message = f"Dators izvēlējās skaitli {move[0]} (bez sadalīšanas)"

        # Izvadam datora gājienu kā paziņojumu
        self.ai_move_label.config(text=ai_message)

        # Atjaunojam UI
        self.update_ui()

        # Pārbaudam vai spēle beidzās
        if not self.sequence:
            self.end_game()
            return

        # Pārejam atpakaļ uz spēlētāja gājienu
        self.player_turn = 1
        self.update_ui()

        # Izveidojam ciparu izvēles pogas
        self.create_number_buttons()

    def create_number_buttons(self):
        # Dzēšam pogas kuras vairs nevajag
        for widget in self.buttons_frame.winfo_children():
            if widget != self.start_button:
                widget.destroy()

        # Izveidojam pogas cipariem kas ir virknē
        for num in set(self.sequence):
            btn = tk.Button(
                self.buttons_frame, 
                text=str(num), 
                command=lambda x=num: self.player_move(x), 
                font=('Arial', 12)
            )
            btn.pack(side=tk.LEFT, padx=5)

    def end_game(self):
        # Pārbaudam kas uzvarēja
        winner = self.check_winner(self.points, self.bank, self.first_player)
        
        if winner == "Neizšķirts":
            message = "Neizšķirts!"
        elif winner == 1:
            message = "Spēlētājs uzvar!"
        else:
            message = "Dators uzvar!"

        # Spēles rezultāts
        messagebox.showinfo("Spēle beigusies", message)
        
        # Notīram liekās pogas
        for widget in self.buttons_frame.winfo_children():
            if widget != self.start_button:
                widget.destroy()

    def check_winner(self, points, bank, first_player):
        if points % 2 == 0 and bank % 2 == 0:
            return first_player
        elif points % 2 == 1 and bank % 2 == 1:
            return 2 if first_player == 1 else 1
        return "Neizšķirts"

    def minimax(self, sequence, points, bank, is_ai_turn, first_player, depth):
        if not sequence or depth == 0:
            return self.evaluate_game(points, bank, first_player)
        
        if is_ai_turn:
            best_score = float('-inf')
            for i in range(len(sequence)):
                new_sequence = sequence[:i] + sequence[i+1:]
                num = sequence[i]
                
                score = self.minimax(new_sequence, points + num, bank, not is_ai_turn, first_player, depth - 1)
                best_score = max(best_score, score)
                
                if num == 2:
                    score = self.minimax(new_sequence, points, bank + 1, not is_ai_turn, first_player, depth - 1)
                    best_score = max(best_score, score)
                elif num == 4:
                    score = self.minimax(new_sequence, points + 2, bank, not is_ai_turn, first_player, depth - 1)
                    best_score = max(best_score, score)
            return best_score
        else:
            best_score = float('inf')
            for i in range(len(sequence)):
                new_sequence = sequence[:i] + sequence[i+1:]
                num = sequence[i]
                
                score = self.minimax(new_sequence, points + num, bank, not is_ai_turn, first_player, depth - 1)
                best_score = min(best_score, score)
                
                if num == 2:
                    score = self.minimax(new_sequence, points, bank + 1, not is_ai_turn, first_player, depth - 1)
                    best_score = min(best_score, score)
                elif num == 4:
                    score = self.minimax(new_sequence, points + 2, bank, not is_ai_turn, first_player, depth - 1)
                    best_score = min(best_score, score)
            return best_score

    def evaluate_game(self, points, bank, first_player):
        ai_player = 2 if first_player == 1 else 1
        player_wins = points % 2 == 0 and bank % 2 == 0
        ai_wins = points % 2 == 1 and bank % 2 == 1
        
        if (first_player == 2 and player_wins) or (first_player == 1 and ai_wins):
            return 1  # Dators uzvar
        elif (first_player == 1 and player_wins) or (first_player == 2 and ai_wins):
            return -1  # Spēlētājs uzvar
        return 0  # Neizšķirts

    def ai_move(self, sequence, points, bank, first_player):
        best_score = float('-inf')
        best_move = None
        depth = 4  # minimax algoritma dziļums kuru pārmeklē dators (tas skatās 4 gājienus uz priekšu. uzliekot ciparu lielāku, dators pārāk ilgi domā, piemēram, dziļums 7 pilnībā uzkarina spēli)
        
        for i in range(len(sequence)):
            new_sequence = sequence[:i] + sequence[i+1:]
            num = sequence[i]
            
            score = self.minimax(new_sequence, points + num, bank, False, first_player, depth)
            if score > best_score:
                best_score = score
                best_move = (num, False)
            
            if num == 2:
                score = self.minimax(new_sequence, points, bank + 1, False, first_player, depth)
                if score > best_score:
                    best_score = score
                    best_move = (num, True)
            elif num == 4:
                score = self.minimax(new_sequence, points + 2, bank, False, first_player, depth)
                if score > best_score:
                    best_score = score
                    best_move = (num, True)
        
        return best_move

def main():
    root = tk.Tk()
    game = NumberGame(root)
    root.mainloop()

if __name__ == "__main__":
    main()