import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QRadioButton, QPushButton, QMessageBox, QFrame
from PyQt5.QtGui import QFont, QPalette, QColor
from PyQt5.QtCore import Qt

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Instrumental Machine Login')
        self.setFixedSize(1024, 600)
        self.setStyleSheet("""
            QWidget {
                background-color: #0a192f;
                color: #ffffff;
                font-family: 'Poppins', sans-serif;
            }
            QLineEdit {
                padding: 10px;
                border: 1px solid #ffffff;
                border-radius: 5px;
                background-color: #1d3153;
                color: #ffffff;
                font-size: 16px;
            }
            QPushButton {
                padding: 10px;
                border: none;
                border-radius: 5px;
                background-color: #64ffda;
                color: #0a192f;
                font-weight: bold;
                font-size: 18px;
            }
            QPushButton:hover {
                background-color: #4cdbbd;
            }
            QRadioButton {
                spacing: 10px;
                font-size: 16px;
            }
            QRadioButton::indicator {
                width: 20px;
                height: 20px;
            }
            QRadioButton::indicator:checked {
                background-color: #64ffda;
                border: 2px solid white;
            }
        """)

        main_layout = QHBoxLayout()
        self.setLayout(main_layout)

        # Left spacer
        main_layout.addStretch(1)

        # Central widget
        central_widget = QFrame()
        central_widget.setFixedWidth(400)
        central_widget.setStyleSheet("""
            QFrame {
                background-color: #172a45;
                border-radius: 10px;
            }
        """)
        central_layout = QVBoxLayout(central_widget)
        main_layout.addWidget(central_widget)

        # Right spacer
        main_layout.addStretch(1)

        title = QLabel('Instrumental Machine')
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont('Poppins', 24, QFont.Bold))
        central_layout.addWidget(title)

        central_layout.addSpacing(20)

        self.username = QLineEdit()
        self.username.setPlaceholderText('Username')
        central_layout.addWidget(self.username)

        central_layout.addSpacing(10)

        self.password = QLineEdit()
        self.password.setPlaceholderText('Password')
        self.password.setEchoMode(QLineEdit.Password)
        central_layout.addWidget(self.password)

        central_layout.addSpacing(20)

        mode_label = QLabel('Operation Mode')
        mode_label.setAlignment(Qt.AlignCenter)
        mode_label.setFont(QFont('Poppins', 18))
        central_layout.addWidget(mode_label)

        central_layout.addSpacing(10)

        radio_layout = QHBoxLayout()
        self.radio_flicker = QRadioButton('Flicker')
        self.radio_clinic = QRadioButton('Clinic')
        self.radio_demo = QRadioButton('Demo')
        radio_layout.addWidget(self.radio_flicker)
        radio_layout.addWidget(self.radio_clinic)
        radio_layout.addWidget(self.radio_demo)
        central_layout.addLayout(radio_layout)

        central_layout.addSpacing(30)

        login_button = QPushButton('Login')
        login_button.clicked.connect(self.login)
        central_layout.addWidget(login_button)

        central_layout.addStretch(1)

    def login(self):
        username = self.username.text()
        password = self.password.text()
        
        if not username or not password:
            self.show_message('Error', 'Please enter both username and password.')
            return

        if not any([self.radio_flicker.isChecked(), self.radio_clinic.isChecked(), self.radio_demo.isChecked()]):
            self.show_message('Error', 'Please select an Operation Mode.')
            return

        if username == 'admin' and password == 'password':
            mode = 'Flicker' if self.radio_flicker.isChecked() else 'Clinic' if self.radio_clinic.isChecked() else 'Demo'
            self.show_message('Success', f'Login successful! Mode: {mode}')
        else:
            self.show_message('Error', 'Invalid username or password.')

    def show_message(self, title, message):
        msg_box = QMessageBox()
        msg_box.setStyleSheet("""
            QMessageBox {
                background-color: #172a45;
                color: #ffffff;
            }
            QMessageBox QPushButton {
                padding: 5px 10px;
                min-width: 60px;
            }
        """)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.exec_()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec_())