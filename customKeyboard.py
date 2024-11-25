from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QPushButton, QGridLayout

class CustomLineEdit(QtWidgets.QLineEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.keyboard = None

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        # Show keyboard on mouse press
        self.show_keyboard()

    def show_keyboard(self):
        if self.keyboard is None or not self.keyboard.isVisible():
            keyboard_width = 800
            keyboard_height = 400
            
            # Get main window geometry
            main_window = self.window()
            window_rect = main_window.geometry()
            
            # Calculate keyboard position
            keyboard_x = window_rect.x() + (window_rect.width() - keyboard_width) // 2
            keyboard_y = window_rect.y() + window_rect.height() - keyboard_height - 50
            
            self.keyboard = VirtualKeyboard(self, main_window)
            self.keyboard.setFixedSize(keyboard_width, keyboard_height)
            self.keyboard.move(keyboard_x, keyboard_y)
            self.keyboard.show()

class VirtualKeyboard(QDialog):
    def __init__(self, target_widget, parent=None):
        super().__init__(parent)
        self.target_widget = target_widget
        self.uppercase = False
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setStyleSheet("background-color: #1e293b; color: white;")
        self.init_ui()

    def init_ui(self):
        layout = QGridLayout(self)
        layout.setSpacing(5)

        # Keyboard layout
        keys = [
            ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "Back"],
            ["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P", "@"],
            ["A", "S", "D", "F", "G", "H", "J", "K", "L", "Enter"],
            ["Shift", "Z", "X", "C", "V", "B", "N", "M", ",", ".", "?"],
            ["123", "Space", "-", "_", "/", "Cancel"]
        ]

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
        for i in reversed(range(layout.count())): 
            layout.itemAt(i).widget().setParent(None)

        for row_index, row in enumerate(self.current_keys):
            for col_index, key in enumerate(row):
                button = QPushButton(key)
                button.setFixedSize(60, 50)
                
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
        try:
            from globalvar import globaladc
            globaladc.buzzer_1()
        except Exception as e:
            print(f"Buzzer error: {e}")

        if key == "Back":
            self.target_widget.backspace()
        elif key == "Enter":
            self.close()
            self.target_widget.keyboard = None
        elif key == "Space":
            self.target_widget.insert(" ")
        elif key == "Shift":
            self.uppercase = not self.uppercase
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
            self.target_widget.keyboard = None
        else:
            self.target_widget.insert(key.upper() if self.uppercase else key.lower())

