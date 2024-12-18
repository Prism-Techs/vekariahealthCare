import tkinter as tk
from PIL import Image, ImageTk
from header import HeaderComponent
import os

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
            image_path = os.path.join(self.current_dir, "macular_densitometer_logo.png")
            img = Image.open(image_path)
            img = img.resize((391, 331))
            self.macular_photo = ImageTk.PhotoImage(img)
            
            self.image_label = tk.Label(
                self.content_frame,
                image=self.macular_photo,
                bg='black'
            )
            self.image_label.place(x=50, y=20)
        except Exception as e:
            print(f"Error loading image: {e}")
            print(f"Attempted path: {image_path}")
            
        # Title Label
        self.title_label = tk.Label(
            self.content_frame,
            text="Macular Densitometer\n",
            font=('Helvetica Neue', 18, 'bold'),
            bg='black',
            fg='white'
        )
        self.title_label.place(x=530, y=100)
        
        # Description Text
        description_text = """\nMacular Densitometer is the only gold standard pre-clinical & clinical stage psycho-physical subjective (test) screening device - globally, for measuring Macular Pigment Optical Density (MPOD), using HFP (Heterochromatic Flicker Photometry Technology); and preventing irreversibly, reversibly blinding diseases at pre-clinical stages and the socio-economic burden arising from the diseases on to the society."""
        
        self.description_label = tk.Label(
            self.content_frame,
            text=description_text,
            font=('Arial',17 ),
            bg='black',
            fg='white',
            wraplength=481,
            justify='left'
        )
        self.description_label.place(x=440, y=130)
        
    def open_wifi_page(self):
        """Implement WiFi page opening functionality"""
        print("Opening WiFi page")

def main():
    root = tk.Tk()
    app = MacularInfoPage(root)
    root.mainloop()

if __name__ == "__main__":
    main()