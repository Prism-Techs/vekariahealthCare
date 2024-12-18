import tkinter as tk
from PIL import Image, ImageTk
from header import HeaderComponent
import os
from login import LoginApp  # Import the LoginApp class

class MacularInfoPage:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1024x600")
        self.root.resizable(False, False)
        self.root.configure(bg='black')
        self.root.overrideredirect(True)
        
        # Get the current directory
        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        
        self.setup_ui()
        
    def setup_ui(self):
        # Add header component
        self.header = HeaderComponent(self.root, "")
        self.header.set_wifi_callback(self.open_wifi_page)
        
        # Main content frame
        self.content_frame = tk.Frame(
            self.root,
            bg='black',
            height=551
        )
        self.content_frame.pack(fill='x', pady=(40, 0))
        
        # Load and display macular densitometer image
        try:
            # Construct path to image in UI directory
            image_path = os.path.join(self.current_dir,  "macular_densitometer_logo.png")
            img = Image.open(image_path)
            img = img.resize((391, 331))
            self.macular_photo = ImageTk.PhotoImage(img)
            
            self.image_label = tk.Label(
                self.content_frame,
                image=self.macular_photo,
                bg='black',
                cursor="hand2"  # Change cursor to hand when hovering
            )
            self.image_label.place(x=50, y=110)
            self.image_label.bind('<Button-1>', self.show_login)  # Bind click event
        except Exception as e:
            print(f"Error loading image: {e}")
            print(f"Attempted path: {image_path}")
            
        # Title Label
        self.title_label = tk.Label(
            self.content_frame,
            text="Macular Densitometer",
            font=('Helvetica Neue', 16, 'bold'),
            bg='black',
            fg='white',
            cursor="hand2"
        )
        self.title_label.place(x=530, y=100)
        self.title_label.bind('<Button-1>', self.show_login)  # Bind click event
        
        # Description Text
        description_text = """Macular Densitometer is the only gold standard pre-clinical & clinical stage psycho-physical subjective (test) screening device - globally, for measuring Macular Pigment Optical Density (MPOD), using HFP (Heterochromatic Flicker Photometry Technology); and preventing irreversibly, reversibly blinding diseases at pre-clinical stages and the socio-economic burden arising from the diseases on to the society."""
        
        self.description_label = tk.Label(
            self.content_frame,
            text=description_text,
            font=('Arial', 12),
            bg='black',
            fg='white',
            wraplength=481,
            justify='left',
            cursor="hand2"
        )
        self.description_label.place(x=440, y=130)
        self.description_label.bind('<Button-1>', self.show_login)  # Bind click event
        
        # Bind click event to the entire window
        self.root.bind('<Button-1>', self.show_login)
        
    def show_login(self, event=None):
        """Hide current window and show login page"""
        self.root.withdraw()  # Hide current window
        
        # Create new window for login
        login_window = tk.Toplevel()
        login_app = LoginApp(login_window)
        
        # If login window is closed, close the entire application
        login_window.protocol("WM_DELETE_WINDOW", lambda: self.root.destroy())
        
    def open_wifi_page(self):
        """Implement WiFi page opening functionality"""
        print("Opening WiFi page")

def main():
    root = tk.Tk()
    app = MacularInfoPage(root)
    root.mainloop()

if __name__ == "__main__":
    main()