from math import *
import tkinter as tk

class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculator")

        window_width = 300
        window_height = 400

        # Pobieranie rozmiarów ekranu
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Obliczanie współrzednych, aby okno było na środku ekranu
        x_pos = (screen_width - window_width) // 2
        y_pos = (screen_height - window_height) // 2

        # Ustawienie okna na środku ekranu
        self.root.geometry(f'{window_width}x{window_height}+{x_pos}+{y_pos}')

        self.result_var = tk.StringVar()
        self.create_widgets()
        #self.root.mainloop()

    def create_widgets(self):
        # Konfiguracja wierszy i kolumn w siatce
        #self.root.grid_rowconfigure(0, weight=1)  # Pierwszy wiersz (etykieta) rozciąga się
        #self.root.grid_rowconfigure(1, weight=4)  # Wiersz przycisków (większa waga)
        for i in range(5):
            self.root.grid_rowconfigure(i, weight=1)
        for j in range(4):  # Cztery kolumny (przyciski)
            self.root.grid_columnconfigure(j, weight=1)
        # Etykieta do wyświetlania wyniku z automatycznym aktualizowaniem
        result_label = tk.Label(self.root, textvariable=self.result_var, height=1, anchor='e')
        result_label.grid(row=0, column=0, columnspan=4, sticky='nsew')

        buttons = [
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('/', 1, 3),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('*', 2, 3),
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('-', 3, 3),
            ('0', 4, 0), ('.', 4, 1), ('=', 4, 2), ('+', 4, 3),
        ]

        for (text, row, col) in buttons:
            button = tk.Button(self.root, text=text, width=4, height=2, command = lambda t = text: self.on_button_click(t))
            button.grid(row=row, column=col, sticky='nsew')

    def on_button_click(self, char):
        current = self.result_var.get()
        if char == '=':
            try:
                # wykonanie wyrażenia
                result = str(eval(current))
                self.result_var.set(result)
            except:
                self.result_var.set("Error")
        else:
            self.result_var.set(current + char)

    def clear(self):
        # Czyszczenie ekranu
        self.result_var.set("")

if __name__ == '__main__':
    root = tk.Tk()
    app = Calculator(root)
    root.mainloop()