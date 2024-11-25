from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtWidgets import QDialog, QPushButton, QGridLayout, QSizeGrip

class VirtualKeyboard(QDialog):
    def __init__(self, target_widget, parent=None):
        super().__init__(parent)
        self.target_widget = target_widget
        self.uppercase = False
        # Remove WindowStaysOnTopHint to allow proper dragging
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.dragging = False
        self.offset = QPoint()
        self.resize_margin = 10  # Resize border width
        
        # Main layout
        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.main_layout.setContentsMargins(self.resize_margin, self.resize_margin, 
                                          self.resize_margin, self.resize_margin)
        
        # Create a container widget with border styling
        self.container = QtWidgets.QWidget()
        self.container.setObjectName("container")
        self.main_layout.addWidget(self.container)
        
        # Title bar
        self.title_bar = QtWidgets.QWidget()
        self.title_bar_layout = QtWidgets.QHBoxLayout(self.title_bar)
        self.title_bar.setCursor(Qt.OpenHandCursor)
        self.title_bar.setFixedHeight(20)
        self.title_bar_layout.setContentsMargins(5, 0, 5, 0)
        self.title_label = QtWidgets.QLabel("Virtual Keyboard")
        self.title_label.setStyleSheet("color: white; font-weight: bold;")
        self.title_bar_layout.addWidget(self.title_label)
        
        # Container layout
        self.container_layout = QtWidgets.QVBoxLayout(self.container)
        self.container_layout.setContentsMargins(0, 0, 0, 0)
        self.container_layout.addWidget(self.title_bar)
        
        # Add keyboard grid
        self.keyboard_widget = QtWidgets.QWidget()
        self.keyboard_layout = QGridLayout(self.keyboard_widget)
        self.keyboard_layout.setSpacing(5)
        self.container_layout.addWidget(self.keyboard_widget)
        
        # Add size grip
        self.size_grip = QSizeGrip(self)
        self.size_grip.setStyleSheet("background: transparent;")

        # Use a layout that doesn’t add extra spacing
        size_grip_layout = QtWidgets.QHBoxLayout()
        size_grip_layout.setContentsMargins(0, 0, 0, 0)  # Make sure no margins are added
        size_grip_layout.setSpacing(0)  # Ensure no spacing is added

        # Optionally remove the stretch if it's causing unwanted vertical space
        # size_grip_layout.addStretch()

        # Add the size grip widget to the layout
        size_grip_layout.addWidget(self.size_grip)
        self.container_layout.addLayout(size_grip_layout)
        
        # Set styles
        self.setStyleSheet("""
            QDialog {
                background: transparent;
            }
            #container {
                background-color: #1e293b;
                border: 1px solid #475569;
                border-radius: 10px;
            }
            QPushButton {
                color: white;
                border-radius: 5px;
                min-width: 40px;
                min-height: 40px;
            }
        """)
        
        self.init_ui()

    def init_ui(self):
        self.setMinimumSize(600, 100)  # Set minimum size
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
        self.create_buttons(self.keyboard_layout)

    def create_buttons(self, layout):
        for i in reversed(range(layout.count())): 
            layout.itemAt(i).widget().setParent(None)

        self.keyboard_layout.setVerticalSpacing(0)  # Removes vertical spacing
        self.keyboard_layout.setHorizontalSpacing(5)  # Optionally, adjust horizontal spacing

        for row_index, row in enumerate(self.current_keys):
            for col_index, key in enumerate(row):
                button = QPushButton(key)
                
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

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = True
            self.offset = event.globalPos() - self.pos()
            event.accept()

    def mouseMoveEvent(self, event):
        if self.dragging and event.buttons() & Qt.LeftButton:
            self.move(event.globalPos() - self.offset)
            event.accept()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = False
            event.accept()

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
            for i in range(self.keyboard_layout.count()):
                button = self.keyboard_layout.itemAt(i).widget()
                if isinstance(button, QPushButton) and len(button.text()) == 1:
                    button.setText(button.text().upper() if self.uppercase else button.text().lower())
        elif key == "123":
            self.current_keys = self.symbol_keys
            self.create_buttons(self.keyboard_layout)
        elif key == "ABC":
            self.current_keys = [
                ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "Back"],
                ["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P", "@"],
                ["A", "S", "D", "F", "G", "H", "J", "K", "L", "Enter"],
                ["Shift", "Z", "X", "C", "V", "B", "N", "M", ",", ".", "?"],
                ["123", "Space", "-", "_", "/", "Cancel"]
            ]
            self.create_buttons(self.keyboard_layout)
        elif key == "Cancel":
            self.close()
            self.target_widget.keyboard = None
        else:
            self.target_widget.insert(key.upper() if self.uppercase else key.lower())