import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont

class HealthcareApp:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1024x612")
        self.root.resizable(False, False)
        self.root.title("Vekaria Healthcare")
        self.root.configure(bg='black')
        
        # Configure styles
        self.style = ttk.Style()
        self.style.configure('Header.TFrame', background='#1f2836')
        self.style.configure('Content.TFrame', background='#1f2836')
        self.style.configure('Header.TLabel', 
                           background='#1f2836',
                           foreground='white',
                           font=('Helvetica Neue', 16, 'bold'))
        
        # Header Frame
        self.header_frame = ttk.Frame(root, style='Header.TFrame', height=41)
        self.header_frame.pack(fill='x')
        
        # Company Name
        self.company_label = ttk.Label(self.header_frame, 
                                     text="Vekaria Healthcare",
                                     style='Header.TLabel')
        self.company_label.place(x=60, y=0)
        
        # Version Label
        self.version_label = ttk.Label(self.header_frame,
                                     text="V1.0",
                                     style='Header.TLabel')
        self.version_label.place(x=930, y=0)
        
        # Main Title
        self.title_label = ttk.Label(root,
                                   text="Macular Densitometer                                                          CFF Fovea Test",
                                   font=('Helvetica Neue', 18),
                                   background='black',
                                   foreground='white')
        self.title_label.pack(pady=10)
        
        # Left Side Buttons
        button_styles = {
            'font': ('Helvetica Neue', 16),
            'bg': 'black',
            'fg': 'white',
            'width': 20,
            'height': 1,
            'relief': 'solid',
            'bd': 2
        }
        
        self.buttons_frame = tk.Frame(root, bg='black')
        self.buttons_frame.pack(side='left', padx=10)
        
        button_texts = [
            "Flicker Demo", "CFF Fovea", "BRK Fovea",
            "CFF Para-Fovea", "BRK Para-Fovea", "Test Result"
        ]
        
        self.buttons = []
        for text in button_texts:
            btn = tk.Button(self.buttons_frame, text=text, **button_styles)
            if text == "CFF Fovea":
                btn.configure(bg='white', fg='black')
            btn.pack(pady=5)
            self.buttons.append(btn)
        
        # Main Content Frame
        self.content_frame = ttk.Frame(root, style='Content.TFrame')
        self.content_frame.pack(expand=True, fill='both', padx=20)
        
        # CFF Fovea Display Frame
        self.cff_frame = tk.Frame(self.content_frame, bg='black', bd=3, relief='solid')
        self.cff_frame.place(relx=0.3, rely=0.1, width=291, height=126)
        
        self.cff_title = tk.Label(self.cff_frame, text="CFF Fovea",
                                font=('Helvetica Neue', 22),
                                bg='black', fg='white')
        self.cff_title.pack(pady=10)
        
        self.cff_value_frame = tk.Frame(self.cff_frame, bg='black')
        self.cff_value_frame.pack()
        
        self.cff_value1 = tk.Label(self.cff_value_frame, text="23.5",
                                 font=('Helvetica Neue', 28),
                                 bg='black', fg='white')
        self.cff_value1.pack(side='left', padx=10)
        
        self.cff_value2 = tk.Label(self.cff_value_frame, text="23.5",
                                 font=('Helvetica Neue', 28),
                                 bg='black', fg='white')
        self.cff_value2.pack(side='left', padx=10)
        
        # Status Buttons
        self.status_frame = tk.Frame(self.content_frame, bg='#1f2836')
        self.status_frame.place(relx=0.1, rely=0.5)
        
        self.status_label = tk.Label(self.status_frame, text="Test Status",
                                   font=('Helvetica Neue', 18),
                                   bg='#1f2836', fg='white')
        self.status_label.pack(pady=10)
        
        # Create status buttons with their specific styles
        status_buttons = [
            ("Machine Ready", "#1a472a", "#4CAF50"),
            ("Flicker Start", "#4d3319", "#FFA500"),
            ("Flicker Visible", "#4d1f1f", "#ff4444")
        ]
        
        for text, bg, fg in status_buttons:
            btn = tk.Button(self.status_frame, text=text,
                          font=('Arial', 14, 'bold'),
                          bg=bg, fg=fg,
                          width=15, height=1,
                          relief='raised')
            btn.pack(pady=5)
        
        # Navigation Buttons
        self.nav_frame = tk.Frame(self.content_frame, bg='#1f2836')
        self.nav_frame.place(relx=0.6, rely=0.8)
        
        nav_style = {
            'font': ('Arial', 24, 'bold'),
            'bg': '#1f2836',  # Changed from 'transparent' to actual color
            'fg': 'white',
            'width': 8,
            'height': 1,
            'relief': 'solid',
            'bd': 1
        }
        
        self.home_btn = tk.Button(self.nav_frame, text="Home", **nav_style)
        self.home_btn.pack(side='left', padx=10)
        
        self.next_btn = tk.Button(self.nav_frame, text="Next", **nav_style)
        self.next_btn.pack(side='left', padx=10)

def main():
    root = tk.Tk()
    app = HealthcareApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()