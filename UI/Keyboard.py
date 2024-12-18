
import tkinter as tk
from globalvar import globaladc

class KeyBoard:
    def __init__(self):
        self.shift_active = False
        self._drag_data = {"x": 0, "y": 0, "item": None}

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

    def on_drag_start(self, event, window):
        """Begin drag of the window"""
        self._drag_data["x"] = event.x
        self._drag_data["y"] = event.y

    def on_drag_motion(self, event, window):
        """Handle dragging of the window"""
        delta_x = event.x - self._drag_data["x"]
        delta_y = event.y - self._drag_data["y"]
        x = window.winfo_x() + delta_x
        y = window.winfo_y() + delta_y
        window.geometry(f"+{x}+{y}")

    def createAlphaKey(self, root, entry, number=False):
        # Define layout with lowercase by default
        alphabets = [
            ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '@'],
            ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', '#'],
            ['a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', '/', '*'],
            ['Shift', 'z', 'x', 'c', 'v', 'b', 'n', 'm', '!', 'Back'],  # Fixed this row
            ['Space', 'Enter']  # Fixed this row
        ]
        
        window = tk.Toplevel(root)
        x = root.winfo_x()
        y = root.winfo_y()

        window.geometry(f"+{x+20}+{y+400}")
        window.overrideredirect(1)
        window.configure(background="black")
        window.wm_attributes("-alpha", 0.7)

        button_config = {
            'padx': 1,
            'pady': 1,
            'bd': 1,
            'bg': "black",
            'fg': "white",
            'font': ('Arial', 10)
        }

        for y, row in enumerate(alphabets):
            x = 0
            for text in row:
                if text == 'Shift':
                    width = 8  # Width for Shift
                    columnspan = 2
                    button = tk.Button(window, text=text, width=width,
                                    command=lambda value=text: self.select(entry, window, root, value),
                                    fg="#42A5F5",
                                    **button_config)
                elif text == 'Space':
                    width = 30  # Width for Space
                    columnspan = 6  # Adjusted columnspan
                    button = tk.Button(window, text=text, width=width,
                                    command=lambda value=text: self.select(entry, window, root, value),
                                    **button_config)
                elif text == 'Enter':
                    width = 12  # Width for Enter
                    columnspan = 3  # Adjusted columnspan
                    button = tk.Button(window, text=text, width=width,
                                    command=lambda value=text: self.select(entry, window, root, value),
                                    **button_config)
                elif text == 'Back':
                    width = 8  # Width for Back
                    columnspan = 2
                    button = tk.Button(window, text=text, width=width,
                                    command=lambda value=text: self.select(entry, window, root, value),
                                    **button_config)
                else:
                    width = 4  # Width for regular keys
                    columnspan = 1
                    button = tk.Button(window, text=text, width=width,
                                    command=lambda value=text: self.select(entry, window, root, value),
                                    **button_config)

                button.grid(row=y, column=x, columnspan=columnspan, padx=1, pady=1)
                x += columnspan
    def createNumaKey(self, root, entry, number=False):
        numbers = [
            ['1', '2', '3'],
            ['4', '5', '6'],
            ['7', '8', '9'],
            ['0', 'Enter', '<-']
        ]

        window = tk.Toplevel(root)
        x = root.winfo_x()
        y = root.winfo_y()

        window.geometry(f"+{x+40}+{y+300}")
        window.overrideredirect(1)
        window.configure(background="black")
        window.wm_attributes("-alpha", 0.7)

        # Add drag bindings to window
        window.bind("<Button-1>", lambda e: self.on_drag_start(e, window))
        window.bind("<B1-Motion>", lambda e: self.on_drag_motion(e, window))

        button_config = {
            'padx': 1,
            'pady': 1,
            'bd': 1,
            'width': 5,
            'bg': "black",
            'fg': "white",
            'font': ('Arial', 10)
        }

        # Create a frame for the buttons
        button_frame = tk.Frame(window, bg='black')
        button_frame.pack(padx=2, pady=2)

        for y, row in enumerate(numbers):
            for x, text in enumerate(row):
                button = tk.Button(button_frame, text=text,
                                 command=lambda value=text: self.select(entry, window, root, value),
                                 **button_config)
                button.grid(row=y, column=x, padx=1, pady=1)
                
                # Make each button draggable too
                button.bind("<Button-1>", lambda e, w=window: self.on_drag_start(e, w))
                button.bind("<B1-Motion>", lambda e, w=window: self.on_drag_motion(e, w))

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
