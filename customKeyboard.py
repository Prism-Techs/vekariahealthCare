from PyQt5 import QtWidgets, QtCore, QtGui
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
        self.main_layout.setContentsMargins(5, 5, 5, 5)  # Soft margins

        # Title bar
        self.title_bar = QtWidgets.QWidget()
        self.title_bar.setObjectName("title_bar")
        self.title_bar.setFixedHeight(25)  # Slightly taller title bar
        self.title_bar_layout = QtWidgets.QHBoxLayout(self.title_bar)
        self.title_bar_layout.setContentsMargins(8, 0, 8, 0)

        # Drag handle icon
        self.drag_label = QtWidgets.QLabel("⣿")  # More modern drag indicator
        self.drag_label.setStyleSheet("""
            color: #6b7280; 
            font-size: 10px; 
            padding: 2px;
        """)
        self.drag_label.setFixedSize(20, 20)
        self.title_bar_layout.addWidget(self.drag_label)

        self.title_bar_layout.addStretch()

        # Close button
        self.close_btn = QPushButton("✕")
        self.close_btn.setFixedSize(25, 25)
        self.close_btn.setObjectName("close_btn")
        self.close_btn.clicked.connect(self.close)
        self.title_bar_layout.addWidget(self.close_btn)

        # Container widget
        self.container = QtWidgets.QWidget()
        self.container.setObjectName("container")

        # Container layout
        self.container_layout = QtWidgets.QVBoxLayout(self.container)
        self.container_layout.setContentsMargins(5, 5, 5, 5)
        self.container_layout.addWidget(self.title_bar)

        # Keyboard widget
        self.keyboard_widget = QtWidgets.QWidget()
        self.keyboard_layout = QGridLayout(self.keyboard_widget)
        self.keyboard_layout.setSpacing(5)  # Slightly more spacing
        self.container_layout.addWidget(self.keyboard_widget)

        # Size grip for resizing
        size_grip_layout = QtWidgets.QHBoxLayout()
        self.size_grip = QSizeGrip(self)
        size_grip_layout.addStretch()
        size_grip_layout.addWidget(self.size_grip)
        self.container_layout.addLayout(size_grip_layout)

        self.main_layout.addWidget(self.container)

    def init_ui(self):
        self.setMinimumSize(350, 180)  # Slightly larger minimum size

        self.alpha_keys = [
            ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "Back"],
            ["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
            ["A", "S", "D", "F", "G", "H", "J", "K", "L", "Enter"],
            ["Shift", "Z", "X", "C", "V", "B", "N", "M", ",", ".", "?"],
            ["123", "Space", "Done"],
        ]

        self.symbol_keys = [
            ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "Back"],
            ["!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "+"],
            ["=", "{", "}", "[", "]", ";", ":", "'", '"', "Enter"],
            ["~", "`", "\\", "|", "<", ">", "€", "£", "¥", "¢", "?"],
            ["ABC", "Space", "Done"],
        ]

        self.current_keys = self.alpha_keys
        self.create_buttons(self.keyboard_layout)

    def apply_styles(self):
        self.setStyleSheet("""
            QDialog {
                background: transparent;
            }
            #container {
                background-color: #1f2937;  /* Deeper dark gray */
                border: 2px solid #374151;
                border-radius: 8px;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            }
            #title_bar {
                background-color: #111827;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
            }
            QPushButton {
                color: #f9fafb;
                border-radius: 4px;
                min-width: 30px;
                min-height: 30px;
                font-size: 10px;
                font-weight: 600;
                transition: all 0.2s;
            }
            QPushButton#close_btn {
                background-color: transparent;
                color: #9ca3af;
                font-size: 12px;
                border: none;
            }
            QPushButton#close_btn:hover {
                background-color: #ef4444;
                color: white;
            }
            QSizeGrip {
                width: 12px;
                height: 12px;
                background-color: #4b5563;
                border-radius: 4px;
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
                button.setFocusPolicy(Qt.NoFocus)

                # Style based on key type
                if key in ["Back", "Enter", "Shift", "123", "ABC", "Done"]:
                    button.setStyleSheet("""
                        QPushButton {
                            background-color: #374151;
                            color: #e5e7eb;
                            border-radius: 4px;
                        }
                        QPushButton:pressed {
                            background-color: #4b5563;
                        }
                    """)
                elif key == "Space":
                    button.setMinimumWidth(100)  # Wider space bar
                    button.setStyleSheet("""
                        QPushButton {
                            background-color: #374151;
                            color: #e5e7eb;
                            border-radius: 4px;
                        }
                        QPushButton:pressed {
                            background-color: #4b5563;
                        }
                    """)
                else:
                    button.setStyleSheet("""
                        QPushButton {
                            background-color: #1f2937;
                            color: #f9fafb;
                            border: 1px solid #374151;
                            border-radius: 4px;
                        }
                        QPushButton:pressed {
                            background-color: #374151;
                        }
                    """)

                button.clicked.connect(lambda checked, k=key: self.key_pressed(k))
                layout.addWidget(button, row_index, col_index)

    def key_pressed(self, key):
        try:
            from globalvar import globaladc
            globaladc.buzzer_1()  # Trigger the buzzer
        except Exception as e:
            print(f"Buzzer error: {e}")

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