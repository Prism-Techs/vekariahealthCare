import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget, QLineEdit, 
    QPushButton, QGridLayout, QDialog
)
from PyQt5.QtCore import Qt, pyqtSignal

# --- Global function to play a buzzer ---
def buzzer_1():
    from globalvar import globaladc
    globaladc.buzzer_1()

# --- Custom QLineEdit to trigger the keyboard ---
class CustomLineEdit(QLineEdit):
    focusIn = pyqtSignal()

    def focusInEvent(self, event):
        super().focusInEvent(event)
        self.focusIn.emit()

# --- Virtual Keyboard Dialog ---
class VirtualKeyboard(QDialog):
    def __init__(self, target_widget, parent=None):
        super().__init__(parent)
        self.target_widget = target_widget
        self.uppercase = False
        self.symbols_mode = False
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setStyleSheet("background-color: #1e293b; color: white;")
        self.init_ui()

    def init_ui(self):
        layout = QGridLayout(self)
        layout.setSpacing(5)

        # Define the keyboard layout with numbers and special characters
        keys = [
            ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "Back"],
            ["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P", "@"],
            ["A", "S", "D", "F", "G", "H", "J", "K", "L", "Enter"],
            ["Shift", "Z", "X", "C", "V", "B", "N", "M", ",", ".", "?"],
            ["123", "Space", "-", "_", "/", "Cancel"]
        ]

        # Additional symbols and numbers that appear when '123' is pressed
        self.symbol_keys = [
            ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "Back"],
            ["!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "+"],
            ["=", "{", "}", "[", "]", ";", ":", "'", '"', "Enter"],
            ["~", "`", "\\", "|", "<", ">", "€", "£", "¥", "¢", "?"],
            ["ABC", "Space", "-", "_", "/", "Cancel"]
        ]

        self.current_keys = keys
        self.create_buttons(layout)

    def create_buttons(self, layout):
        # Clear existing buttons
        for i in reversed(range(layout.count())): 
            layout.itemAt(i).widget().setParent(None)

        # Create new buttons
        for row_index, row in enumerate(self.current_keys):
            for col_index, key in enumerate(row):
                button = QPushButton(key)
                button.setFixedSize(60, 50)
                
                # Special styling for function keys
                if key in ["Back", "Enter", "Shift", "123", "ABC", "Cancel", "Space"]:
                    button.setStyleSheet(
                        "QPushButton {background-color: #475569; border-radius: 5px;}"
                        "QPushButton:pressed {background-color: #64748b;}"
                    )
                else:
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
            self.close()
        elif key == "Space":
            self.target_widget.insert(" ")
        elif key == "Shift":
            self.uppercase = not self.uppercase
            # Update button text case
            for i in range(self.layout().count()):
                button = self.layout().itemAt(i).widget()
                if isinstance(button, QPushButton) and len(button.text()) == 1:
                    button.setText(button.text().upper() if self.uppercase else button.text().lower())
        elif key == "123":
            self.current_keys = self.symbol_keys
            self.create_buttons(self.layout())
        elif key == "ABC":
            self.current_keys = [
                ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "Back"],
                ["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P", "@"],
                ["A", "S", "D", "F", "G", "H", "J", "K", "L", "Enter"],
                ["Shift", "Z", "X", "C", "V", "B", "N", "M", ",", ".", "?"],
                ["123", "Space", "-", "_", "/", "Cancel"]
            ]
            self.create_buttons(self.layout())
        elif key == "Cancel":
            self.close()
        else:
            self.target_widget.insert(key.upper() if self.uppercase else key.lower())

# --- Main Window ---
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Enhanced Virtual Keyboard with Buzzer")
        self.setGeometry(100, 100, 800, 600)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)

        # Add QLineEdit fields
        self.fields = []
        for i in range(3):
            field = CustomLineEdit(self)
            font = field.font()
            font.setPointSize(18)
            field.setFont(font)
            field.setStyleSheet(
                "QLineEdit {background-color: #334155; color: white; border: 1px solid white; padding: 5px;}"
            )
            field.focusIn.connect(lambda f=field: self.open_keyboard(f))
            layout.addWidget(field)
            self.fields.append(field)

    def open_keyboard(self, target_widget):
        self.keyboard = VirtualKeyboard(target_widget, self)
        self.keyboard.setGeometry(100, 300, 800, 400)  # Made wider to accommodate all keys
        self.keyboard.show()

# --- Main Entry Point ---
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())