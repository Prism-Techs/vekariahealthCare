import tkinter as tk
from tkinter import ttk
from tkinter import font as tkfont

class MacularDensitometer:
    def __init__(self, root):
        self.root = root
        self.root.title("Macular Densitometer")
        self.root.geometry("1024x604")
        self.root.configure(bg='black')
        
        # Create top frame
        self.top_frame = tk.Frame(root, bg='#1f2836', height=40)
        self.top_frame.pack(fill='x')
        
        # Company name and version
        self.company_label = tk.Label(self.top_frame, text="Vekaria Healthcare", 
                                    font=('Helvetica Neue', 16, 'bold'),
                                    bg='#1f2836', fg='white')
        self.company_label.place(x=60, y=0)
        
        self.version_label = tk.Label(self.top_frame, text="V1.0",
                                    font=('Helvetica Neue', 14),
                                    bg='#1f2836', fg='white')
        self.version_label.place(x=930, y=0)
        
        # Main title
        self.title_label = tk.Label(root, 
                                  text="Macular Densitometer                                                  BRK Fovea Test",
                                  font=('Helvetica Rounded', 18, 'bold'),
                                  bg='black', fg='white')
        self.title_label.place(x=0, y=40)
        
        # Left side buttons
        button_configs = [
            ("Flicker Demo", 150, 'white', 'black'),
            ("CFF Fovea", 210, 'black', 'white'),
            ("BRK Fovea", 270, 'black', 'white'),
            ("CFF Para-Fovea", 330, 'black', 'white'),
            ("BRK Para-Fovea", 390, 'black', 'white'),
            ("Test Result", 450, 'black', 'white')
        ]
        
        for text, y_pos, bg, fg in button_configs:
            btn = tk.Button(root, text=text,
                          font=('Helvetica Neue', 16),
                          width=20, height=1,
                          bg=bg, fg=fg,
                          relief='solid', borderwidth=2)
            btn.place(x=20, y=y_pos)
        
        # Center controls
        self.null_label = tk.Label(root, text="NULL",
                                 font=('Helvetica', 24, 'bold'),
                                 bg='black', fg='#1210FF')
        self.null_label.place(x=360, y=110)
        
        # Number controls
        self.up_button = tk.Button(root, text="+",
                                 font=('Helvetica', 30, 'bold'),
                                 width=2, height=1,
                                 bg='black', fg='white',
                                 relief='solid', borderwidth=1)
        self.up_button.place(x=380, y=160)
        
        self.number_label = tk.Label(root, text="15",
                                   font=('Helvetica Rounded', 28, 'bold'),
                                   width=3, height=1,
                                   bg='black', fg='white',
                                   relief='solid', borderwidth=2)
        self.number_label.place(x=370, y=246)
        
        self.down_button = tk.Button(root, text="-",
                                   font=('Helvetica', 30, 'bold'),
                                   width=2, height=1,
                                   bg='black', fg='white',
                                   relief='solid', borderwidth=1)
        self.down_button.place(x=380, y=330)
        
        # Bottom buttons
        self.resume_button = tk.Button(root, text="RESUME",
                                     font=('Helvetica', 16),
                                     width=15, height=2,
                                     bg='#B8C9D9')
        self.resume_button.place(x=330, y=450)
        
        self.restart_button = tk.Button(root, text="RESTART",
                                      font=('Helvetica', 16),
                                      width=15, height=2,
                                      bg='#B8C9D9')
        self.restart_button.place(x=740, y=450)
        
        # Right side display
        self.value_label = tk.Label(root, text="24.5",
                                  font=('Helvetica', 28),
                                  width=8, height=1,
                                  bg='black', fg='white',
                                  relief='solid', borderwidth=2)
        self.value_label.place(x=720, y=110)
        
        # Create three text boxes
        for i, x_pos in enumerate([720, 800, 880]):
            text = tk.Text(root, font=('Helvetica', 20),
                         width=4, height=6,
                         bg='black', fg='brown',
                         relief='solid', borderwidth=2)
            text.place(x=x_pos, y=190)
            text.insert('1.0', "132\n156\n135\n160")
            text.config(state='disabled')

def main():
    root = tk.Tk()
    app = MacularDensitometer(root)
    root.mainloop()

if __name__ == "__main__":
    main()