import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QPushButton, QComboBox, QLineEdit, QFrame)
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt, QSize

class WifiConfigUI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('WiFi Configuration')
        self.setStyleSheet("""
            QWidget {
                background-color: #1e2129;
                color: white;
                font-family: Arial;
            }
            QFrame {
                background-color: #2a2f3a;
                border-radius: 10px;
                padding: 20px;
            }
            QPushButton {
                background-color: #3a3f4a;
                border: none;
                padding: 10px;
                border-radius: 5px;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #4a4f5a;
            }
            QLineEdit, QComboBox {
                background-color: #3a3f4a;
                border: none;
                padding: 10px;
                border-radius: 5px;
                min-width: 200px;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox::down-arrow {
                image: url(down_arrow.png);
                width: 12px;
                height: 12px;
            }
            QComboBox QAbstractItemView {
                background-color: #3a3f4a;
                selection-background-color: #4a4f5a;
            }
        """)

        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        # Card frame
        card = QFrame()
        card_layout = QVBoxLayout(card)
        main_layout.addWidget(card, alignment=Qt.AlignCenter)

        # Title
        title = QLabel("WiFi Configuration")
        title.setFont(QFont("Arial", 18, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(title)

        # Network dropdown and rescan icon layout
        network_layout = QHBoxLayout()
        card_layout.addLayout(network_layout)

        # Network dropdown
        self.network_dropdown = QComboBox()
        self.network_dropdown.setPlaceholderText("Select a network")
        network_layout.addWidget(self.network_dropdown)

        # Rescan icon button
        rescan_btn = QPushButton()
        rescan_btn.setIcon(QIcon("refresh_icon.png"))  # Make sure to have this icon in your directory
        rescan_btn.setFixedSize(QSize(40, 40))
        rescan_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border-radius: 20px;
            }
            QPushButton:hover {
                background-color: #3a3f4a;
            }
        """)
        rescan_btn.clicked.connect(self.rescan_networks)
        network_layout.addWidget(rescan_btn)

        # Password input
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter password")
        self.password_input.setEchoMode(QLineEdit.Password)
        card_layout.addWidget(self.password_input)

        # Buttons layout
        buttons_layout = QHBoxLayout()
        card_layout.addLayout(buttons_layout)

        # Forget Network button
        forget_btn = QPushButton("Forget")
        forget_btn.clicked.connect(self.forget_network)
        buttons_layout.addWidget(forget_btn)

        # Connect button
        connect_btn = QPushButton("Connect")
        connect_btn.clicked.connect(self.connect_network)
        connect_btn.setStyleSheet("""
            background-color: #0066cc;
            color: white;
            font-weight: bold;
        """)
        buttons_layout.addWidget(connect_btn)

        self.setGeometry(300, 300, 300, 400)

    def rescan_networks(self):
        # Placeholder for rescan functionality
        self.network_dropdown.clear()
        networks = ["Network 1", "Network 2", "Network 3"]  # Replace with actual scan
        self.network_dropdown.addItems(networks)

    def forget_network(self):
        # Placeholder for forget network functionality
        current_network = self.network_dropdown.currentText()
        if current_network:
            index = self.network_dropdown.currentIndex()
            self.network_dropdown.removeItem(index)
            print(f"Forgot network: {current_network}")
            # Implement actual forget network logic here

    def connect_network(self):
        # Placeholder for connect functionality
        network = self.network_dropdown.currentText()
        password = self.password_input.text()
        if network:
            print(f"Connecting to {network} with password: {password}")
            # Implement actual connection logic here

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = WifiConfigUI()
    ex.show()
    sys.exit(app.exec_())