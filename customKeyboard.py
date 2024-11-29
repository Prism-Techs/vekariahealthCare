from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtWidgets import QDialog, QPushButton, QGridLayout, QSizeGrip


class VirtualKeyboard(QDialog):
    def __init__(self, target_widget, parent=None):
        super().__init__(parent)
        self.target_widget = target_widget
        self.uppercase = False
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.dragging = False
        self.offset = QPoint()

        # Main layout setup
        self.setup_layouts()
        # Initialize the keyboard UI
        self.init_ui()
        # Apply styles
        self.apply_styles()

    def setup_layouts(self):
        # Main layout
        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.main_layout.setContentsMargins(10, 10, 10, 10)

        # Title bar
        self.title_bar = QtWidgets.QWidget()
        self.title_bar_layout = QtWidgets.QHBoxLayout(self.title_bar)
        self.title_bar_layout.setContentsMargins(5, 5, 5, 5)

        # Add drag handle icon
        self.drag_label = QtWidgets.QLabel("≡")
        self.drag_label.setStyleSheet("color: #94a3b8; font-size: 18px;")
        self.title_bar_layout.addWidget(self.drag_label)
        self.title_bar_layout.addStretch()

        # Close button
        self.close_btn = QPushButton("×")
        self.close_btn.setFixedSize(30, 30)
        self.close_btn.clicked.connect(self.close)
        self.title_bar_layout.addWidget(self.close_btn)

        # Container widget
        self.container = QtWidgets.QWidget()
        self.container.setObjectName("container")

        # Container layout
        self.container_layout = QtWidgets.QVBoxLayout(self.container)
        self.container_layout.setContentsMargins(8, 8, 8, 8)
        self.container_layout.addWidget(self.title_bar)

        # Keyboard widget
        self.keyboard_widget = QtWidgets.QWidget()
        self.keyboard_layout = QGridLayout(self.keyboard_widget)
        self.keyboard_layout.setSpacing(5)
        self.container_layout.addWidget(self.keyboard_widget)

        # Size grip
        size_grip_layout = QtWidgets.QHBoxLayout()
        self.size_grip = QSizeGrip(self)
        size_grip_layout.addStretch()
        size_grip_layout.addWidget(self.size_grip)
        self.container_layout.addLayout(size_grip_layout)

        self.main_layout.addWidget(self.container)

    def init_ui(self):
        self.setMinimumSize(600, 300)

        self.alpha_keys = [
            ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "Back"],
            ["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P", "@"],
            ["A", "S", "D", "F", "G", "H", "J", "K", "L", "Enter"],
            ["Shift", "Z", "X", "C", "V", "B", "N", "M", ",", ".", "?"],
            ["123", "Space", "-", "_", "/", "Done"],
        ]

        self.symbol_keys = [
            ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "Back"],
            ["!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "+"],
            ["=", "{", "}", "[", "]", ";", ":", "'", '"', "Enter"],
            ["~", "`", "\\", "|", "<", ">", "€", "£", "¥", "¢", "?"],
            ["ABC", "Space", "-", "_", "/", "Done"],
        ]

        self.current_keys = self.alpha_keys
        self.create_buttons(self.keyboard_layout)

    def apply_styles(self):
        self.setStyleSheet("""
            QDialog {
                background: transparent;
            }
            #container {
                background-color: #1e293b;
                border: 1px solid #475569;
                border-radius: 12px;
            }
            QPushButton {
                color: #f8fafc;
                border-radius: 6px;
                min-width: 45px;
                min-height: 45px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton#close_btn {
                background-color: transparent;
                color: #94a3b8;
                font-size: 20px;
                border-radius: 15px;
                min-width: 30px;
                min-height: 30px;
            }
            QPushButton#close_btn:hover {
                background-color: #dc2626;
                color: white;
            }
            QSizeGrip {
                width: 16px;
                height: 16px;
            }
        """)

    def create_buttons(self, layout):
        # Clear existing buttons
        for i in reversed(range(layout.count())):
            widget = layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)

        # Create new buttons
        for row_index, row in enumerate(self.current_keys):
            for col_index, key in enumerate(row):
                button = QPushButton(key)
                button.setFocusPolicy(Qt.NoFocus)  # Prevent focus border

                # Style based on key type
                if key in ["Back", "Enter", "Shift", "123", "ABC", "Done"]:
                    button.setStyleSheet("""
                        QPushButton {
                            background-color: #475569;
                            border-radius: 6px;
                        }
                        QPushButton:pressed {
                            background-color: #64748b;
                        }
                    """)
                elif key == "Space":
                    button.setMinimumWidth(200)
                else:
                    button.setStyleSheet("""
                        QPushButton {
                            background-color: #334155;
                            border-radius: 6px;
                        }
                        QPushButton:pressed {
                            background-color: #475569;
                        }
                    """)

                button.clicked.connect(lambda checked, k=key: self.key_pressed(k))
                layout.addWidget(button, row_index, col_index)

    def key_pressed(self, key):
        if key == "Back":
            self.target_widget.backspace()
        elif key in ["Enter", "Done"]:
            self.close()
        elif key == "Space":
            self.target_widget.insert(" ")
        elif key == "Shift":
            self.uppercase = not self.uppercase
            for i in range(self.keyboard_layout.count()):
                button = self.keyboard_layout.itemAt(i).widget()
                if isinstance(button, QPushButton) and len(button.text()) == 1:
                    button.setText(button.text().upper() if self.uppercase else button.text().lower())
        elif key == "123":
            self.current_keys = self.symbol_keys
            self.create_buttons(self.keyboard_layout)
        elif key == "ABC":
            self.current_keys = self.alpha_keys
            self.create_buttons(self.keyboard_layout)
        else:
            self.target_widget.insert(key.upper() if self.uppercase else key.lower())

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and self.title_bar.geometry().contains(event.pos()):
            self.dragging = True
            self.offset = event.globalPos() - self.pos()
        event.accept()

    def mouseMoveEvent(self, event):
        if self.dragging and event.buttons() & Qt.LeftButton:
            self.move(event.globalPos() - self.offset)
        event.accept()

    def mouseReleaseEvent(self, event):
        self.dragging = False
        event.accept()
