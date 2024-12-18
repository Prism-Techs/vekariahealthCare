import tkinter as tk
from globalvar import globaladc

class KeyBoard:

    def __init__(self):
        self.shift_active = False
        self._drag_data = {"x": 0, "y": 0}  # For dragging


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

    def select(self, entry, window, mainwindow, value, ucase=None):        
        uppercase =ucase
        if value == "Space":
            value = ' '
        elif value == 'Enter':
            value = ''
            globaladc.get_print("enter pressed")
            mainwindow.focus_force()
            window.destroy()
        elif value == 'Tab':
            value = '\t'

        if value == "Back" or value == '<-':
            if isinstance(entry, tk.Entry):
                entry.delete(len(entry.get())-1, 'end')
            #elif isinstance(entry, tk.Text):
            else: # tk.Text
                entry.delete('end - 2c', 'end')
        
        elif value == 'Shift':
            self.shift_active = not self.shift_active
            for widget in window.winfo_children():
                if isinstance(widget, tk.Frame):
                    for btn in widget.winfo_children():
                        if isinstance(btn, tk.Button) and btn['text'] not in ['Space', 'Enter', 'Back', 'Shift', '<-']:
                            btn['text'] = btn['text'].upper() if self.shift_active else btn['text'].lower()

        elif value in ('Caps Lock', 'Shift'):
            uppercase = not uppercase # change True to False, or False to True
        else:
            if uppercase:
                value = value.upper()
            entry.insert('end', value)
        globaladc.buzzer_1()



    def createAlphaKey(self, root, entry, number=False):
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

        # Add dragging to window
        window.bind("<Button-1>", lambda e: self.on_drag_start(e, window))
        window.bind("<B1-Motion>", lambda e: self.on_drag_motion(e, window))

        # Create main frame
        main_frame = tk.Frame(window, bg='black')
        main_frame.pack(padx=2, pady=2)  # Slightly more padding

        # Common button style
        button_style = {
            'bg': "black",
            'fg': "white",
            'padx': 2,  # Increased padding
            'pady': 2,
            'font': ('Arial', 12),  # Bigger font
            'bd': 1  # Border width
        }

        for y, row in enumerate(alphabets):
            x = 0
            for text in row:
                if text == 'Shift':
                    width = 8  # Bigger width
                    columnspan = 2
                elif text == 'Space':
                    width = 40  # Bigger space bar
                    columnspan = 8
                elif text == 'Enter':
                    width = 8  # Bigger width
                    columnspan = 2
                elif text == 'Back':
                    width = 8  # Bigger width
                    columnspan = 2
                else:
                    width = 5  # Bigger width for regular keys
                    columnspan = 1

                button = tk.Button(main_frame, 
                                text=text, 
                                width=width,
                                command=lambda value=text: self.select(entry, window, root, value),
                                **button_style)
                button.grid(row=y, column=x, columnspan=columnspan, padx=2, pady=2, sticky='nsew')

                # Make each button draggable
                button.bind("<Button-1>", lambda e, w=window: self.on_drag_start(e, w))
                button.bind("<B1-Motion>", lambda e, w=window: self.on_drag_motion(e, w))

                x += columnspan


   #create a Numeric Keypad
    def createNumaKey(self, root, entry, number=False):

            numbers = [
                ['1', '2', '3' ],
                ['4', '5', '6' ],
                ['7', '8', '9',],
                ['0', 'Enter','<-']
            ]


            window = tk.Toplevel(root)
            x = root.winfo_x()
            y = root.winfo_y()

            window.geometry("+%d+%d" % (x+40, y + 300))

            window.overrideredirect (1)  # Don't allow the widgets inside to determine the frame's width / height

            window.configure(background="cornflowerblue")
            window.wm_attributes("-alpha", 0.7)

            for y, row in enumerate(numbers):

                x = 0
                width = 10
                columnspan = 1
                #for x, text in enumerate(row):
                for text in row:
                    # if text in ('Enter', 'Shift'):
                        
                    #     columnspan = 1
                    # elif text == 'Space':
                    #     width = 8
                    #     columnspan = 1
                    # else:
                    #     width = 8
                    #     columnspan = 1

                    tk.Button(window, text=text, width=width,
                            command=lambda value=text: self.select(entry, window,root,value),
                            padx=3, pady=3, bd=12, bg="black", fg="white"
                            ).grid(row=y, column=x, columnspan=columnspan)

                    x += columnspan

# --- main ---

if __name__ == '__main__':
    root = tk.Tk()
    root.title('Test Keyboard')
    kb = KeyBoard()

    def callback(sv):
        lobaladc.get_print("call back")

    label = tk.Label(root, text='Test Keyboard')
    label.grid(row=0, column=0, columnspan=2)

    sv = tk.StringVar ()
    sv.trace ("w",
              lambda name, index, mode, sv=sv: callback (sv))

    entry1 = tk.Entry(root)
    entry1.bind ('<FocusIn>',
                   lambda event: kb.createAlphaKey(root, entry1))
    entry1.grid(row=1, column=0, sticky='news')

    button1 = tk.Button(root, text='Keyboard', command=lambda:kb.createNumaKey(root, entry1))
    button1.grid(row=1, column=1, sticky='news')

    entry2 = tk.Entry(root)
    entry2.grid(row=2, column=0, sticky='news')

    button2 = tk.Button(root, text='Keyboard', command=lambda:kb.createNumaKey(root, entry2))
    button2.grid(row=2, column=1, sticky='news')

    text1 = tk.Text(root)
    text1.grid(row=3, column=0, sticky='news')

    button3 = tk.Button(root, text='Keyboard', command=lambda:kb.createNumaKey(root, text1))
    button3.grid(row=3, column=1, sticky='news')

    root.mainloop()