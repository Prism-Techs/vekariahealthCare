from PyQt5 import QtCore, QtWidgets
from globalvar import globaladc

class CustomKeyboard(QtWidgets.QWidget):
    def __init__(self, parent, entry, mainwindow):
        super().__init__(parent)
        self.parent = parent
        self.entry = entry
        self.mainwindow = mainwindow
        self.uppercase = False
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.create_keyboard()

    def select(self, value):
        if value == "Space":
            value = ' '
        elif value == 'Enter':
            value = ''
            globaladc.get_print("enter pressed")
            self.mainwindow.setFocus()
            self.close()
        elif value == 'Tab':
            value = '\t'

        if value == "Back" or value == '<-':
            if isinstance(self.entry, QtWidgets.QLineEdit):
                self.entry.backspace()
            else: # QtWidgets.QTextEdit
                cursor = self.entry.textCursor()
                cursor.deletePreviousChar()
                self.entry.setTextCursor(cursor)
        elif value in ('Caps Lock', 'Shift'):
            self.uppercase = not self.uppercase
        else:
            if self.uppercase:
                value = value.upper()
            self.entry.insert(value)
        globaladc.buzzer_1()

    def create_keyboard(self):
        layout = QtWidgets.QGridLayout()
        self.setLayout(layout)

        alphabets = [
            ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P'],
            ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', 'Back'],
            ['Z', 'X', 'C', 'V', 'B', 'N', 'M', 'Enter'],
            ['Space']
        ]

        for y, row in enumerate(alphabets):
            for text in row:
                width = 8
                if text == 'Space':
                    width = 80
                    columnspan = 16
                else:
                    columnspan = 1
                button = QtWidgets.QPushButton(text)
                button.setFixedWidth(width * 10)
                button.clicked.connect(lambda checked, value=text: self.select(value))
                button.setStyleSheet("""
                    QPushButton {
                        background-color: black;
                        color: white;
                        border: none;
                        padding: 5px;
                        font-size: 24px;
                    }
                    QPushButton:hover {
                        background-color: #333;
                    }
                """)
                layout.addWidget(button, y, row.index(text), 1, columnspan)

        x = self.parent.x() + 20
        y = self.parent.y() + 400
        self.move(x, y)
        self.show()