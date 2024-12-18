import tkinter as tk
from globalvar import globaladc

class KeyBoard:
    def __init__(self):
        self.shift_active = False  # Track shift state

    def select(self, entry, window, mainwindow, value, ucase=None):        
        if value == "Space":
            value = ' '
        elif value == 'Enter':
            value = ''
            globaladc.get_print("enter pressed")
            mainwindow.focus_force()
            window.destroy()
        elif value == 'Tab':
            value = '\t'
        elif value == 'Shift':
            self.shift_active = not self.shift_active  # Toggle shift state
            # Update button labels based on shift state
            for widget in window.winfo_children():
                if isinstance(widget, tk.Button) and widget['text'] not in ['Space', 'Enter', 'Back', 'Shift', '<-']:
                    widget['text'] = widget['text'].upper() if self.shift_active else widget['text'].lower()
            return  # Don't insert anything for Shift key

        if value == "Back" or value == '<-':
            if isinstance(entry, tk.Entry):
                entry.delete(len(entry.get())-1, 'end')
            else: # tk.Text
                entry.delete('end - 2c', 'end')
        else:
            if self.shift_active:
                value = value.upper()
            entry.insert('end', value)
        globaladc.buzzer_1()

    def createAlphaKey(self, root, entry, number=False):
        # Define layout with lowercase by default
        alphabets = [
        ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '@'],
        ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', '#'],
        ['a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', '/', '*'],
        ['Shift', 'z', 'x', 'c', 'v', 'b', 'n', 'm', '!', 'Back'],
        ['Space', 'Enter']
        ]
        
        window = tk.Toplevel(root)
        x = root.winfo_x()
        y = root.winfo_y()

        window.geometry("+%d+%d" %(x+20, y+400))
        window.overrideredirect(1)
        window.configure(background="black")
        window.wm_attributes("-alpha", 0.7)

        for y, row in enumerate(alphabets):
            x = 0
            for text in row:
                if text == 'Shift':
                    width = 12
                    columnspan = 2
                    button = tk.Button(window, text=text, width=width,
                                     command=lambda value=text: self.select(entry, window, root, value),
                                     padx=3, pady=3, bd=12, bg="black", fg="#42A5F5")  # Different color for Shift
                elif text == 'Space':
                    width = 80
                    columnspan = 16
                    button = tk.Button(window, text=text, width=width,
                                     command=lambda value=text: self.select(entry, window, root, value),
                                     padx=3, pady=3, bd=12, bg="black", fg="white")
                elif text == 'Enter':
                    width = 10
                    columnspan = 1
                    button = tk.Button(window, text=text, width=width,
                                     command=lambda value=text: self.select(entry, window, root, value),
                                     padx=3, pady=3, bd=12, bg="black", fg="white")
                else:
                    width = 8
                    columnspan = 1
                    button = tk.Button(window, text=text, width=width,
                                     command=lambda value=text: self.select(entry, window, root, value),
                                     padx=3, pady=3, bd=12, bg="black", fg="white")

                button.grid(row=y, column=x, columnspan=columnspan)
                x += columnspan

    def createNumaKey(self, root, entry, number=False):
        # Numeric keyboard remains unchanged
        numbers = [
            ['1', '2', '3'],
            ['4', '5', '6'],
            ['7', '8', '9'],
            ['0', 'Enter', '<-']
        ]

        window = tk.Toplevel(root)
        x = root.winfo_x()
        y = root.winfo_y()

        window.geometry("+%d+%d" % (x+40, y + 300))
        window.overrideredirect(1)
        window.configure(background="cornflowerblue")
        window.wm_attributes("-alpha", 0.7)

        for y, row in enumerate(numbers):
            x = 0
            width = 10
            columnspan = 1
            for text in row:
                tk.Button(window, text=text, width=width,
                         command=lambda value=text: self.select(entry, window, root, value),
                         padx=3, pady=3, bd=12, bg="black", fg="white"
                         ).grid(row=y, column=x, columnspan=columnspan)
                x += columnspan

if __name__ == '__main__':
    root = tk.Tk()
    root.title('Test Keyboard')
    kb = KeyBoard()

    def callback(sv):
        globaladc.get_print("call back")

    label = tk.Label(root, text='Test Keyboard')
    label.grid(row=0, column=0, columnspan=2)

    sv = tk.StringVar()
    sv.trace("w", lambda name, index, mode, sv=sv: callback(sv))

    entry1 = tk.Entry(root)
    entry1.bind('<FocusIn>', lambda event: kb.createAlphaKey(root, entry1))
    entry1.grid(row=1, column=0, sticky='news')

    button1 = tk.Button(root, text='Keyboard', command=lambda: kb.createNumaKey(root, entry1))
    button1.grid(row=1, column=1, sticky='news')

    entry2 = tk.Entry(root)
    entry2.grid(row=2, column=0, sticky='news')

    button2 = tk.Button(root, text='Keyboard', command=lambda: kb.createNumaKey(root, entry2))
    button2.grid(row=2, column=1, sticky='news')

    text1 = tk.Text(root)
    text1.grid(row=3, column=0, sticky='news')

    button3 = tk.Button(root, text='Keyboard', command=lambda: kb.createNumaKey(root, text1))
    button3.grid(row=3, column=1, sticky='news')

    root.mainloop()