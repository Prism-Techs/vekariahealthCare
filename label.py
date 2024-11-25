from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt
import sys

class StatusLabel(QLabel):
    def __init__(self, text, status):
        super().__init__(text)
        self.setAlignment(Qt.AlignCenter)
        self.setFixedSize(120, 40)
        
        # Base style for 3D effect with dark theme
        base_style = """
            QLabel {{
                color: {text_color};
                border: none;
                border-radius: 5px;
                font-weight: bold;
                font-size: 14px;
                padding: 5px;
                
                /* Dark theme base style */
                background-color: {bg_color};
                
                /* 3D effect borders */
                border-top: 2px solid {light};
                border-left: 2px solid {light};
                border-bottom: 2px solid {dark};
                border-right: 2px solid {dark};
                
                /* Deeper shadow for dark theme */
                box-shadow: 2px 2px 4px rgba(0, 0, 0, 0.4),
                           inset 1px 1px 2px rgba(255, 255, 255, 0.1);
            }}
            
            QLabel:hover {{
                background-color: {hover_color};
                border-top: 2px solid {dark};
                border-left: 2px solid {dark};
                border-bottom: 2px solid {light};
                border-right: 2px solid {light};
            }}
        """
        
        # Dark theme status-specific colors
        if status == "active":
            colors = {
                "bg_color": "#1a472a",      # Dark green
                "hover_color": "#2a5a3a",    # Slightly lighter green
                "light": "#2d8549",          # Highlight
                "dark": "#0d2415",           # Shadow
                "text_color": "#4CAF50"      # Bright green text
            }
        elif status == "warning":
            colors = {
                "bg_color": "#4d3319",       # Dark orange
                "hover_color": "#5d4329",    # Slightly lighter orange
                "light": "#b36b1b",          # Highlight
                "dark": "#2b1d0e",           # Shadow
                "text_color": "#FFA500"      # Bright orange text
            }
        else:  # error
            colors = {
                "bg_color": "#4d1f1f",       # Dark red
                "hover_color": "#5d2f2f",    # Slightly lighter red
                "light": "#a33636",          # Highlight
                "dark": "#2b1111",           # Shadow
                "text_color": "#ff4444"      # Bright red text
            }
            
        self.setStyleSheet(base_style.format(**colors))

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Dark Theme Status Labels")
        
        # Main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)
        
        # Set dark theme for main window
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1e1e1e;
            }
            QWidget {
                background-color: #1e1e1e;
            }
        """)
        
        # Create status labels
        active_label = StatusLabel("ACTIVE", "active")
        warning_label = StatusLabel("WARNING", "warning")
        error_label = StatusLabel("ERROR", "error")
        
        # Add labels to layout
        layout.addWidget(active_label, alignment=Qt.AlignCenter)
        layout.addWidget(warning_label, alignment=Qt.AlignCenter)
        layout.addWidget(error_label, alignment=Qt.AlignCenter)
        
        # Window setup
        self.setGeometry(100, 100, 300, 250)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())