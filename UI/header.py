# header_component.py
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import font
from globalvar import globaladc

class HeaderComponent:
    def __init__(self, parent_frame, page_title=""):
        """
        Initialize header component
        parent_frame: The main frame where header will be placed
        page_title: The title of the current page/screen
        """
        # Create header frame
        self.header_frame = tk.Frame(parent_frame, bg='#1f2836', height=41)
        self.header_frame.pack(fill='x')
        
        # Keep reference of the image to prevent garbage collection
        self.images = {}
        
        # Setup company logo
        try:
            logo = Image.open("logo.png")
            logo = logo.resize((44, 23))
            self.images['logo'] = ImageTk.PhotoImage(logo)
            self.logo_label = tk.Label(
                self.header_frame, 
                image=self.images['logo'], 
                bg='#1f2836'
            )
            self.logo_label.place(x=0, y=10)
        except Exception as e:
            print(f"Logo image not found: {e}")
            
        # Setup WiFi icon
        try:
            wifi_image = Image.open("wifi_logo.png")
            wifi_image = wifi_image.resize((41, 31), Image.LANCZOS)
            self.images['wifi'] = ImageTk.PhotoImage(wifi_image)
            self.wifi_label = self.create_clickable_label(
                self.header_frame,
                image=self.images['wifi'],
                bg='#1f2836'
            )
            self.wifi_label.place(x=868, y=5)
        except Exception as e:
            print(f"WiFi logo not found: {e}")

        # Company name label
        tk.Label(
            self.header_frame, 
            text="Vekaria Healthcare",
            font=('Helvetica Neue', 16, 'bold'),
            bg='#1f2836',
            fg='white'
        ).place(x=60, y=10)

        # Version label
        tk.Label(
            self.header_frame,
            text="V1.0",
            font=('Helvetica Neue', 14, 'bold'),
            bg='#1f2836',
            fg='white'
        ).place(x=930, y=10)

        # Page title
        if page_title:
            tk.Label(
                parent_frame,
                text=page_title,
                font=("Arial", 20),
                bg='black',
                fg='white'
            ).place(x=0, y=40)

    def create_clickable_label(self, master, **kwargs):
        """Create a clickable label with callback functionality"""
        label = tk.Label(master, **kwargs)
        label.bind('<Button-1>', self._on_click)
        label.callback = None
        return label

    def _on_click(self, event):
        """Handle click events on labels"""
        if hasattr(event.widget, 'callback') and event.widget.callback:
            event.widget.callback()

    def set_wifi_callback(self, callback):
        """Set callback for wifi icon click"""
        self.wifi_label.callback = callback
        

    def update_page_title(self, new_title):
        """Update the page title"""
        if hasattr(self, 'title_label'):
            self.title_label.config(text=new_title)