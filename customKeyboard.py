import tkinter as tk
from globalvar import globaladc

class KeyBoard:
    def __init__(self, root, entry, mainwindow):
        self.root = root
        self.entry = entry
        self.mainwindow = mainwindow

    def select(self, value, uppercase=None):
        if value == "Space":
            value = ' '
        elif value == 'Enter':
            value = ''
            globaladc.get_print("enter pressed")
            self.mainwindow.focus_force()
            self.window.destroy()
        elif value == 'Tab':
            value = '\t'

        if value == "Back" or value == '<-':
            if isinstance(self.entry, tk.Entry):
                self.entry.delete(len(self.entry.get())-1, 'end')
            else: # tk.Text
                self.entry.delete('end - 2c', 'end')
        elif value in ('Caps Lock', 'Shift'):
            self.uppercase = not self.uppercase # change True to False, or False to True
        else:
            if self.uppercase:
                value = value.upper()
            self.entry.insert('end', value)
        globaladc.buzzer_1()

    def create_keyboard(self):
        self.uppercase = False
        self.window = tk.Toplevel(self.root)
        x = self.root.winfo_x()
        y = self.root.winfo_y()

        self.window.geometry("+%d+%d" %(x+20, y+400))
        self.window.overrideredirect(1)
        self.window.configure(background="black")
        self.window.wm_attributes("-alpha", 0.7)

        alphabets = [
            ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P'],
            ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', 'Back'],
            ['Z', 'X', 'C', 'V', 'B', 'N', 'M', 'Enter'],
            ['Space']
        ]

        for y, row in enumerate(alphabets):
            x = 0
            for text in row:
                width = 8
                columnspan = 1
                tk.Button(self.window, text=text, width=width,
                          command=lambda value=text: self.select(value),
                          padx=3, pady=3, bd=12, bg="black", fg="white"
                         ).grid(row=y, column=x, columnspan=columnspan)
                x += columnspan