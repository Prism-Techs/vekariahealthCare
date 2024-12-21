import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import json
import os
from PIL import Image, ImageTk
from header import HeaderComponent
from Startupclass import StatrupClass
from loader import AnimatedWindow


class HomePage:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1024x600")
        self.root.resizable(False, False)
        self.root.configure(bg='black')
        
        # Remove window decorations
        self.root.overrideredirect(True)
        
        # Initialize variables
        self.wifi_window = None
        self.setup_ui()

    def setup_ui(self):
        # Add the header component
        self.header = HeaderComponent(self.root, "                                                    Home Page")
        self.header.set_wifi_callback(self.open_wifi_page)
        
        # Welcome Label (User Info)
        self.user_info_label = tk.Label(
            self.root,
            text="Welcome",
            font=('Helvetica Neue', 14, 'bold'),
            fg='white',
            bg='black',  # Same as root background
            anchor='w'
        )
        self.user_info_label.place(x=20, y=150, width=280, height=40)
        
        # Create main buttons with hover effect
        self.create_styled_button("Create User", 347, 150, self.create_user)
        self.create_styled_button("View Reports", 347, 280, self.view_reports)
        self.create_styled_button("Test Mode", 347, 410, self.test_mode)
        
        # Time and Date Labels
        self.time_label = tk.Label(
            self.root,
            font=('Helvetica Neue', 10),
            fg='white',
            bg='black',
        )
        self.time_label.place(x=960, y=550)
        
        self.date_label = tk.Label(
            self.root,
            font=('Helvetica Neue', 10),
            bg='black',

            fg='white'
        )
        self.date_label.place(x=934, y=570)
        
        # Start time updates
        self.update_datetime()
        
        # Check user role
        self.check_user_role()

    def create_styled_button(self, text, x, y, command):
        button = tk.Button(
            self.root,
            text=text,
            font=('Arial', 24, 'bold'),
            bg='#101826',
            fg='white',
            bd=1,
            relief='solid',
            width=15,
            height=1,
            command=command
        )
        button.place(x=x, y=y)
        
        # Bind hover events
        button.bind('<Enter>', lambda e, b=button: self.on_button_hover(b))
        button.bind('<Leave>', lambda e, b=button: self.on_button_leave(b))
        
        return button

    def on_button_hover(self, button):
        button.configure(
            bg='rgba(33, 150, 243, 0.1)',
            fg='#64B5F6',
            bd=2
        )

    def on_button_leave(self, button):
        button.configure(
            bg='#101826',
            fg='white',
            bd=1
        )

    def check_user_role(self):
        """Check user role from latest_user.json and show/hide buttons accordingly"""
        try:
            json_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 
                                   "user_data", "latest_user.json")
            
            if os.path.exists(json_path):
                with open(json_path, 'r') as file:
                    user_data = json.load(file)
                
                # Check if user is an operator
                is_operator = user_data.get('is_operator', 0) == 1
                
                # Set user info label
                title = user_data.get('title', '')
                first_name = user_data.get('first_name', '')
                last_name = user_data.get('last_name', '')
                
                # Format user info with title if available
                if title:
                    user_info = f"Welcome,\n{title} {first_name} {last_name}"
                else:      
                    user_info = f"Welcome,\n{first_name} {last_name}"
                
                self.user_info_label.config(text=user_info)
                
                # Adjust button visibility and positions based on role
                if is_operator:
                    for widget in self.root.winfo_children():
                        if isinstance(widget, tk.Button):
                            if widget['text'] == "Create User":
                                widget.place_forget()
                            elif widget['text'] == "View Reports":
                                widget.place(x=347, y=150)
                            elif widget['text'] == "Test Mode":
                                widget.place(x=347, y=280)
                else:
                    for widget in self.root.winfo_children():
                        if isinstance(widget, tk.Button):
                            if widget['text'] == "Create User":
                                widget.place(x=347, y=150)
                            elif widget['text'] == "View Reports":
                                widget.place(x=347, y=280)
                            elif widget['text'] == "Test Mode":
                                widget.place(x=347, y=410)
            else:
                messagebox.showwarning('Error', 'No user data found. Please log in again.')
                
        except Exception as e:
            messagebox.showerror('Error', f'Error loading user data: {str(e)}')

    def update_datetime(self):
        """Update time and date labels"""
        current_time = datetime.now().strftime('%H:%M')
        current_date = datetime.now().strftime('%d-%m-%Y')
        self.time_label.config(text=current_time)
        self.date_label.config(text=current_date)
        self.root.after(1000, self.update_datetime)

    def open_wifi_page(self):
        """Open WiFi settings window"""
        # Implement WiFi page
        print("Opening WiFi page")

    def create_user(self):
        """Handle create user button click"""
        # Implement create user functionality
        print("Create user clicked")

    def view_reports(self):
        """Handle view reports button click"""
        # Implement view reports functionality
        print("View reports clicked")

    def test_mode(self):
        """Handle test mode button click"""
        # Implement test mode functionality
        self.root.withdraw()  # Hide current window
        # Launch patient info page
        
        st = StatrupClass()
        st.main()
        print("Test mode clicked")

def main():
    root = tk.Tk()
    app = HomePage(root)
    root.mainloop()

if __name__ == "__main__":
    main()