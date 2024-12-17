# custom_widgets.py
import tkinter as tk
from tkinter import font

class CustomEntry(tk.Entry):
    def __init__(self, parent, **kwargs):
        font_style = ('Helvetica Neue', 14, 'bold')
        default_style = {
            'font': font_style,
            'bg': '#334155',
            'fg': '#94a3b8',
            'relief': 'solid',
            'bd': 1,
            'highlightthickness': 0,
            'insertbackground': 'white'
        }
        default_style.update(kwargs)
        super().__init__(parent, **default_style)

        # Round corners using custom border
        self.configure(highlightbackground='white', 
                      highlightcolor='white')

class RadioButtonGroup:
    def __init__(self, parent, options, x, y, spacing=120):
        self.buttons = []
        self.var = tk.StringVar()
        
        for i, (text, value) in enumerate(options):
            btn = tk.Radiobutton(
                parent,
                text=text,
                value=value,
                variable=self.var,
                font=('Helvetica Neue', 16),
                bg='black',
                fg='white',
                selectcolor='black',
                activebackground='black',
                activeforeground='white'
            )
            btn.place(x=x + (i * spacing), y=y)
            self.buttons.append(btn)

    def get_value(self):
        return self.var.get()

    def set_value(self, value):
        self.var.set(value)