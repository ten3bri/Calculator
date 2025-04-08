from math import *
import tkinter as tk
#from tkinter import colorchooser

class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculator")

        # wybór koloru tła okna przez użytkownika
        #chosen_color = colorchooser.askcolor(title="Wybierz kolor tła")
        #if chosen_color[1]:
        #    self.root.configure(bg=chosen_color[1])

        self.digit_color = "#f0f0f0"
        self.operator_color = "#cce6ff"
        self.equal_color = "#66b3ff"

        # słownik
        self.hover_colors = {
            self.digit_color: "#e0e0e0",
            self.operator_color: "#b3daff",
            self.equal_color: "#4da6ff"
        }

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
        for i in range(6):
            self.root.grid_rowconfigure(i, weight=1)
        for j in range(5):  # Cztery kolumny (przyciski)
            self.root.grid_columnconfigure(j, weight=1)

        # Etykieta do wyświetlania wyniku z automatycznym aktualizowaniem
        result_label = tk.Label(self.root, textvariable=self.result_var, height=1, anchor='e', font=("Arial", 15), borderwidth=3, relief='ridge')
        result_label.grid(row=0, column=0, columnspan=5, sticky='nsew', padx=5, pady=3)

        buttons = [
            ('7', 2, 1), ('8', 2, 2), ('9', 2, 3), ('/', 2, 4),
            ('4', 3, 1), ('5', 3, 2), ('6', 3, 3), ('*', 3, 4),
            ('1', 4, 1), ('2', 4, 2), ('3', 4, 3), ('-', 4, 4),
            ('0', 5, 1), ('.', 5, 2), ('=', 5, 3), ('+', 5, 4),
        ]

        for (text, row, col) in buttons:
            if text in '0123456789.':
                bg_color = self.digit_color
            elif text == '=':
                bg_color = self.equal_color
            else:
                bg_color = self.operator_color

            button = tk.Button(self.root, text=text, width=4, height=2, bg=bg_color, command= lambda t = text: self.on_button_click(t))
            button.grid(row=row, column=col, sticky='nsew')

            # zapamiętujemy oryginalny kolor przycisku
            button.original_bg = bg_color

            # dodajemy efekty hovera
            button.bind('<Enter>', self.on_enter)
            button.bind('<Leave>', self.on_leave)

        clear_all_button = tk.Button(self.root, text='AC', width=4, height=2, bg=self.operator_color, command = self.clear)
        clear_all_button.grid(row=1, column=4, sticky='nsew')
        clear_all_button.original_bg = self.operator_color
        self.add_hover_effect(clear_all_button)

        clear_last_button = tk.Button(self.root, text='CE', width=4, height=2, bg=self.operator_color, command = self.clear_last)
        clear_last_button.grid(row=1, column=3, sticky='nsew')
        clear_last_button.original_bg = self.operator_color
        self.add_hover_effect(clear_last_button)

        l_bracket_button = tk.Button(self.root, text='(', width=4, height=2, bg=self.operator_color, command = lambda: self.on_button_click('('))
        l_bracket_button.grid(row=1, column=1, sticky='nsew')
        l_bracket_button.original_bg = self.operator_color
        self.add_hover_effect(l_bracket_button)

        r_bracket_button = tk.Button(self.root, text=')', width=4, height=2, bg=self.operator_color, command=lambda: self.on_button_click(')'))
        r_bracket_button.grid(row=1, column=2, sticky='nsew')
        r_bracket_button.original_bg = self.operator_color
        self.add_hover_effect(r_bracket_button)

        percent_button = tk.Button(self.root, text='%', width=4, height=2, bg=self.operator_color, command=lambda: self.on_button_click('%'))
        percent_button.grid(row=1, column=0, sticky='nsew')
        percent_button.original_bg = self.operator_color
        self.add_hover_effect(percent_button)

        ln_button = tk.Button(self.root, text='ln', width=4, height=2, bg=self.operator_color, command=self.calculate_ln)
        ln_button.grid(row=2, column=0, sticky='nsew')
        ln_button.original_bg = self.operator_color
        self.add_hover_effect(ln_button)

        log_button = tk.Button(self.root, text='log', width=4, height=2, bg=self.operator_color, command=self.calculate_log)
        log_button.grid(row=3, column=0, sticky='nsew')
        log_button.original_bg = self.operator_color
        self.add_hover_effect(log_button)

        sqrt_button = tk.Button(self.root, text='√', width=4, height=2, bg=self.operator_color, command=self.calculate_sqrt)
        sqrt_button.grid(row=4, column=0, sticky='nsew')
        sqrt_button.original_bg = self.operator_color
        self.add_hover_effect(sqrt_button)

        power_button = tk.Button(self.root, text='xʸ', width=4, height=2, bg=self.operator_color, command=lambda: self.on_button_click('^'))
        power_button.grid(row=5, column=0, sticky='nsew')
        power_button.original_bg = self.operator_color
        self.add_hover_effect(power_button)

    def on_button_click(self, char):
        current = self.result_var.get()
        if char == '=':
            try:
                # Zamień % na *0.01*, np. 50%10 -> 50*0.01*10 -> 5.0
                expression = current.replace('%', '*0.01*').replace('^', '**')
                # wykonanie wyrażenia
                result = eval(expression)

                # jeśli rezultat jest liczbą całkowitą to tak go wyświetlaj (bez części dziesiętnej)
                if isinstance(result, float) and result.is_integer():
                    result = int(result)

                self.result_var.set(str(result))
            except:
                self.result_var.set("Error")
        else:
            self.result_var.set(current + char)

    def clear(self):
        # Czyszczenie ekranu
        self.result_var.set("")

    def clear_last(self):
        # Czyszczenie ostatniego znaku
        current = self.result_var.get()
        if current:
            self.result_var.set(current[:-1])

    def calculate_ln(self):
        try:
            value = float(self.result_var.get())
            result = log(value)

            # jeśli wynik np. 2.0, wyświetlaj 2
            if result.is_integer():
                result = int(result)

            self.result_var.set(str(result))
        except:
            self.result_var.set("Error")

    def calculate_log(self):
        try:
            value = float(self.result_var.get())
            result = log10(value)

            # jeśli wynik np. 2.0, wyświetlaj 2
            if result.is_integer():
                result = int(result)

            self.result_var.set(str(result))
        except:
            self.result_var.set("Error")

    def calculate_sqrt(self):
        try:
            value = float(self.result_var.get())
            if value < 0:
                self.result_var.set("Error")
                return # ← tu przerywa działanie funkcji

            result = sqrt(value)
            self.result_var.set(str(result))

            # jeśli wynik np. 2.0, wyświetlaj 2
            if result.is_integer():
                result = int(result)

            self.result_var.set(str(result))
        except:
            self.result_var.set("Error")

    # przy najechaniu myszką zmiana koloru przycisku
    def on_enter(self, event):
        original_color = event.widget.cget("bg")
        hover_color = self.hover_colors.get(original_color, original_color)
        event.widget['background'] = hover_color

    # z powrotem na domyślny kolor
    def on_leave(self, event):
        event.widget['background'] = event.widget.original_bg

    def add_hover_effect(self, button):
        button.bind("<Enter>", self.on_enter)
        button.bind("<Leave>", self.on_leave)

if __name__ == '__main__':
    root = tk.Tk()
    app = Calculator(root)
    root.mainloop()