import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QGridLayout, QWidget, QVBoxLayout, QLineEdit
)
from PyQt5.QtCore import Qt, QPoint


class VirtualKeyboard(QWidget):
    def __init__(self, input_field):
        super().__init__()
        self.input_field = input_field
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setStyleSheet("background-color: #cccccc; border: 1px solid #000000;")
        self.setFixedSize(600, 200)
        self.init_ui()
        self.drag_position = None

    def init_ui(self):
        layout = QGridLayout()
        buttons = [
            '1', '2', '3', '4', '5', '6', '7', '8', '9', '0',
            'Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P',
            'A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', 
            'Z', 'X', 'C', 'V', 'B', 'N', 'M', '<', ' ', '>'
        ]

        positions = [(i, j) for i in range(4) for j in range(10)]
        for position, button in zip(positions, buttons):
            if button == " ":
                btn = QPushButton("Space")
                btn.setFixedSize(200, 40)
                btn.clicked.connect(lambda _, b=button: self.insert_text(b))
                layout.addWidget(btn, *position, 1, 3)
            else:
                btn = QPushButton(button)
                btn.setFixedSize(40, 40)
                btn.clicked.connect(lambda _, b=button: self.insert_text(b))
                layout.addWidget(btn, *position)

        self.setLayout(layout)

    def insert_text(self, char):
        if char == "<":
            self.input_field.backspace()
        elif char == ">":
            self.input_field.setText(self.input_field.text() + " ")
        else:
            self.input_field.setText(self.input_field.text() + char)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_position = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton and self.drag_position:
            self.move(event.globalPos() - self.drag_position)
            event.accept()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Virtual Keyboard Example")
        self.setGeometry(100, 100, 1024, 600)
        self.init_ui()

    def init_ui(self):
        self.input_field = QLineEdit(self)
        self.input_field.setPlaceholderText("Click the keyboard button to open the virtual keyboard")
        self.input_field.setFixedHeight(40)

        self.keyboard_button = QPushButton("Open Keyboard", self)
        self.keyboard_button.clicked.connect(self.show_keyboard)

        layout = QVBoxLayout()
        layout.addWidget(self.input_field)
        layout.addWidget(self.keyboard_button)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def show_keyboard(self):
        self.keyboard = VirtualKeyboard(self.input_field)
        self.keyboard.move(200, 400)
        self.keyboard.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
