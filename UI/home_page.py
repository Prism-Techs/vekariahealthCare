import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import json
import os
from PIL import Image, ImageTk
from header import HeaderComponent
from Startupclass import StatrupClass
from functools import lru_cache
import weakref

class HomePage:
    def __init__(self, root):
        self.root = root
        # Use hardware acceleration if available
        try:
            self.root.attributes('-accelerated', True)
        except:
            pass
            
        self.root.geometry("1024x600")
        self.root.resizable(False, False)
        self.root.configure(bg='black')
        
        # Remove window decorations
        self.root.overrideredirect(True)
        
        # Initialize variables
        self.wifi_window = None
        self._setup_resources()
        self.setup_ui()
        
        # Cache for frequently accessed data
        self._user_data_cache = None
        self._last_cache_update = 0
        
        # Optimize update intervals
        self._time_update_interval = 1000  # 1 second
        self._cache_lifetime = 60000  # 1 minute

    def _setup_resources(self):
        """Pre-initialize resources and styles"""
        self.button_style = {
            'font': ('Arial', 24, 'bold'),
            'bg': '#101826',
            'fg': 'white',
            'bd': 1,
            'relief': 'solid',
            'width': 15,
            'height': 1
        }
        
        self.label_style = {
            'font': ('Helvetica Neue', 10),
            'fg': 'white',
            'bg': 'black'
        }

    @lru_cache(maxsize=32)
    def _create_font(self, family, size, weight):
        """Cache frequently used fonts"""
        return (family, size, weight)

    def setup_ui(self):
        # Add the header component with cached fonts
        self.header = HeaderComponent(self.root, "                                                    Home Page")
        self.header.set_wifi_callback(self.open_wifi_page)
        
        # Welcome Label (User Info) with cached font
        self.user_info_label = tk.Label(
            self.root,
            text="Welcome",
            font=self._create_font('Helvetica Neue', 14, 'bold'),
            fg='white',
            bg='black',
            anchor='w'
        )
        self.user_info_label.place(x=20, y=150, width=280, height=40)
        
        # Create main buttons with optimized event handling
        self._create_optimized_buttons()
        
        # Time and Date Labels with shared styles
        self.time_label = tk.Label(self.root, **self.label_style)
        self.time_label.place(x=960, y=550)
        
        self.date_label = tk.Label(self.root, **self.label_style)
        self.date_label.place(x=934, y=570)
        
        # Initialize time display
        self._update_datetime()
        
        # Load user role with caching
        self._check_user_role()

    def _create_optimized_buttons(self):
        """Create buttons with shared styles and optimized event handling"""
        buttons_config = [
            ("Create User", 347, 150, self.create_user),
            ("View Reports", 347, 280, self.view_reports),
            ("Test Mode", 347, 410, self.test_mode)
        ]
        
        self.buttons = []
        for text, x, y, command in buttons_config:
            button = tk.Button(self.root, text=text, command=command, **self.button_style)
            button.place(x=x, y=y)
            
            # Use weak references for event binding to prevent memory leaks
            button_ref = weakref.ref(button)
            button.bind('<Enter>', lambda e, b=button_ref: self._on_button_hover(b()))
            button.bind('<Leave>', lambda e, b=button_ref: self._on_button_leave(b()))
            
            self.buttons.append(button)

    def _on_button_hover(self, button):
        """Optimized hover effect"""
        if button:
            button.configure(bg='rgba(33, 150, 243, 0.1)', fg='#64B5F6', bd=2)

    def _on_button_leave(self, button):
        """Optimized leave effect"""
        if button:
            button.configure(**self.button_style)

    @lru_cache(maxsize=1)
    def _get_user_data_path(self):
        """Cache the user data file path"""
        return os.path.join(os.path.dirname(os.path.abspath(__file__)), 
                           "user_data", "latest_user.json")

    def _check_user_role(self):
        """Check user role with caching"""
        current_time = datetime.now().timestamp()
        
        # Use cached data if available and not expired
        if (self._user_data_cache and 
            current_time - self._last_cache_update < self._cache_lifetime):
            self._update_ui_for_role(self._user_data_cache)
            return
            
        try:
            json_path = self._get_user_data_path()
            
            if os.path.exists(json_path):
                with open(json_path, 'r') as file:
                    self._user_data_cache = json.load(file)
                    self._last_cache_update = current_time
                    self._update_ui_for_role(self._user_data_cache)
            else:
                messagebox.showwarning('Error', 'No user data found. Please log in again.')
                
        except Exception as e:
            messagebox.showerror('Error', f'Error loading user data: {str(e)}')

    def _update_ui_for_role(self, user_data):
        """Update UI based on user role"""
        is_operator = user_data.get('is_operator', 0) == 1
        
        # Update user info label
        user_info = self._format_user_info(user_data)
        self.user_info_label.config(text=user_info)
        
        # Update button positions
        self._update_button_positions(is_operator)

    def _format_user_info(self, user_data):
        """Format user info string"""
        title = user_data.get('title', '')
        first_name = user_data.get('first_name', '')
        last_name = user_data.get('last_name', '')
        
        return f"Welcome,\n{title} {first_name} {last_name}" if title else f"Welcome,\n{first_name} {last_name}"

    def _update_button_positions(self, is_operator):
        """Update button positions based on role"""
        positions = {
            True: {  # Operator
                "View Reports": (347, 150),
                "Test Mode": (347, 280)
            },
            False: {  # Non-operator
                "Create User": (347, 150),
                "View Reports": (347, 280),
                "Test Mode": (347, 410)
            }
        }
        
        for button in self.buttons:
            if button['text'] in positions[is_operator]:
                x, y = positions[is_operator][button['text']]
                button.place(x=x, y=y)
            else:
                button.place_forget()

    def _update_datetime(self):
        """Update time and date with optimized interval"""
        current = datetime.now()
        self.time_label.config(text=current.strftime('%H:%M'))
        self.date_label.config(text=current.strftime('%d-%m-%Y'))
        self.root.after(self._time_update_interval, self._update_datetime)

    def open_wifi_page(self):
        """Open WiFi settings window"""
        if not self.wifi_window:
            print("Opening WiFi page")

    def create_user(self):
        print("Create user clicked")

    def view_reports(self):
        print("View reports clicked")

    def test_mode(self):
        self.root.withdraw()
        st = StatrupClass()
        st.main()

def main():
    # Enable garbage collection optimization
    import gc
    gc.enable()
    
    root = tk.Tk()
    
    # Set process priority (Linux/Raspberry Pi specific)
    try:
        import os
        os.nice(10)  # Lower priority to prevent GUI from hogging CPU
    except:
        pass
    
    app = HomePage(root)
    root.mainloop()

if __name__ == "__main__":
    main()