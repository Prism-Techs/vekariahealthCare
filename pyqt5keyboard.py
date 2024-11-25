import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget, QLineEdit, QPushButton, QGridLayout, QDialog
)
from PyQt5.QtCore import Qt, pyqtSignal
# from PyQt5.QtMultimedia import QSound  # For playing the buzzer sound

# --- Global function to play a buzzer ---
def buzzer_1():
    from globalvar import globaladc
    globaladc.buzzer_1()  # Assuming this function is defined elsewhere  # Path to your buzzer sound file


# --- Custom QLineEdit to trigger the keyboard ---
class CustomLineEdit(QLineEdit):
    focusIn = pyqtSignal()  # Custom signal for focus

    def focusInEvent(self, event):
        super().focusInEvent(event)
        self.focusIn.emit()  # Emit custom signal on focus


# --- Virtual Keyboard Dialog ---
class VirtualKeyboard(QDialog):
    def __init__(self, target_widget, parent=None):
        super().__init__(parent)
        self.target_widget = target_widget
        self.uppercase = False  # To handle uppercase letters
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setStyleSheet("background-color: #1e293b; color: white;")
        self.init_ui()

    def init_ui(self):
        layout = QGridLayout(self)
        layout.setSpacing(5)

        # Define the keyboard layout
        keys = [
            ["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P", "Back"],
            ["A", "S", "D", "F", "G", "H", "J", "K", "L", "Enter"],
            ["Z", "X", "C", "V", "B", "N", "M", "Space"],
        ]

        for row_index, row in enumerate(keys):
            for col_index, key in enumerate(row):
                button = QPushButton(key)
                button.setFixedSize(60, 50)
                button.setStyleSheet(
                    "QPushButton {background-color: #334155; border-radius: 5px;}"
                    "QPushButton:pressed {background-color: #475569;}"
                )
                button.clicked.connect(lambda _, k=key: self.key_pressed(k))
                layout.addWidget(button, row_index, col_index)

    def key_pressed(self, key):
        buzzer_1()  # Trigger the buzzer sound
        if key == "Back":
            self.target_widget.backspace()
        elif key == "Enter":
            self.target_widget.returnPressed.emit()
            self.close()  # Close the keyboard
        elif key == "Space":
            self.target_widget.insert(" ")
        else:
            self.target_widget.insert(key.upper() if self.uppercase else key.lower())


# --- Main Window ---
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Virtual Keyboard with Buzzer")
        self.setGeometry(100, 100, 800, 400)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)

        # Add a few QLineEdit fields
        self.fields = []
        for i in range(3):
            field = CustomLineEdit(self)
            font = field.font()  # Retrieve the current font
            font.setPointSize(18)  # Modify the font size
            field.setFont(font)  # Apply the modified font back to the field
            field.setStyleSheet(
                "QLineEdit {background-color: #334155; color: white; border: 1px solid white; padding: 5px;}"
            )
            field.focusIn.connect(lambda f=field: self.open_keyboard(f))
            layout.addWidget(field)
            self.fields.append(field)


    def open_keyboard(self, target_widget):
        self.keyboard = VirtualKeyboard(target_widget, self)
        self.keyboard.setGeometry(100, 300, 600, 250)
        self.keyboard.show()


# --- Main Entry Point ---
if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Create main window
    window = MainWindow()
    window.show()

    sys.exit(app.exec_())
