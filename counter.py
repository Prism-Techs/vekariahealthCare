from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import Qt

class CounterWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.value = 0
        self.setup_ui()
        
    def setup_ui(self):
        # Create horizontal layout
        layout = QtWidgets.QHBoxLayout(self)
        layout.setSpacing(0)  # Remove spacing between widgets
        
        # Decrement button
        self.dec_button = QtWidgets.QPushButton("-")
        self.dec_button.setFixedSize(40, 40)
        self.dec_button.clicked.connect(self.decrement)
        
        # Value label
        self.value_label = QtWidgets.QLabel("0")
        self.value_label.setFixedSize(60, 40)
        
        # Increment button
        self.inc_button = QtWidgets.QPushButton("+")
        self.inc_button.setFixedSize(40, 40)
        self.inc_button.clicked.connect(self.increment)
        
        # Add widgets to layout
        layout.addWidget(self.dec_button)
        layout.addWidget(self.value_label)
        layout.addWidget(self.inc_button)
        
        # Style the widgets
        self.style_widgets()
        
    def style_widgets(self):
        # Common button style
        button_style = """
            QPushButton {
                background-color: #000000;
                color: #ffffff;
                border: 2px solid #333333;
                font-size: 20px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1a1a1a;
                border-color: #444444;
            }
            QPushButton:pressed {
                background-color: #2d2d2d;
                border-color: #555555;
            }
        """
        
        # Style decrement button (left side rounded)
        self.dec_button.setStyleSheet(button_style + """
            QPushButton {
                border-top-left-radius: 20px;
                border-bottom-left-radius: 20px;
                border-right: none;
            }
        """)
        
        # Style increment button (right side rounded)
        self.inc_button.setStyleSheet(button_style + """
            QPushButton {
                border-top-right-radius: 20px;
                border-bottom-right-radius: 20px;
                border-left: none;
            }
        """)
        
        # Style value label
        self.value_label.setStyleSheet("""
            QLabel {
                background-color: #000000;
                color: #00ff00;
                border-top: 2px solid #333333;
                border-bottom: 2px solid #333333;
                font-size: 18px;
                font-weight: bold;
                qproperty-alignment: AlignCenter;
            }
        """)
        
        # Set font
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        self.value_label.setFont(font)
        
        # Set cursor
        self.dec_button.setCursor(Qt.PointingHandCursor)
        self.inc_button.setCursor(Qt.PointingHandCursor)
        
    def increment(self):
        self.value += 1
        self.update_display()
        self.animate_button(self.inc_button)
        
    def decrement(self):
        self.value -= 1
        self.update_display()
        self.animate_button(self.dec_button)
        
    def update_display(self):
        self.value_label.setText(str(self.value))
        
    def animate_button(self, button):
        # Create animation for button press effect
        anim = QtCore.QPropertyAnimation(button, b"geometry")
        anim.setDuration(100)
        
        # Get current geometry
        geo = button.geometry()
        
        # Press down
        anim.setStartValue(geo)
        pressed_geo = geo.adjusted(0, 2, 0, 2)
        anim.setEndValue(pressed_geo)
        anim.start()
        
        # Pop back up after 100ms
        QtCore.QTimer.singleShot(100, lambda: self.animate_release(button))
        
    def animate_release(self, button):
        anim = QtCore.QPropertyAnimation(button, b"geometry")
        anim.setDuration(100)
        
        # Get current geometry
        geo = button.geometry()
        
        # Move back up
        anim.setStartValue(geo)
        release_geo = geo.adjusted(0, -2, 0, -2)
        anim.setEndValue(release_geo)
        anim.start()

# Example usage
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Counter Widget Demo")
        self.setStyleSheet("background-color: #121212;")
        
        # Create central widget
        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)
        
        # Create layout
        layout = QtWidgets.QVBoxLayout(central_widget)
        layout.setAlignment(Qt.AlignCenter)
        
        # Create counter widget
        self.counter = CounterWidget()
        layout.addWidget(self.counter)
        
        # Set window size
        self.setMinimumSize(300, 200)

# Run the application
if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())