import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QTimer, Qt, QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import QPixmap
# from login import Ui_Form
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtCore import QTimer, Qt, QPropertyAnimation, QEasingCurve, QEvent
from PyQt5.QtGui import QPixmap
from imagewrite import Ui_Form as WriteUPImageForm
from globalvar import globaladc
from wifi_checker import main as wifi_checker_main
from Patient_checker import run_in_thread
# from . import login_page
from PyQt5.QtWidgets import QMessageBox
from customKeyboard import RPiKeyboard
from database  import DatabaseConnection
import os
import subprocess
from datetime import datetime
import json
from wifi_update import WifiStatusLabel
from wifi_final import WifiPage
from PyQt5.QtCore import Qt, QRect, QTimer, QDateTime
# from . import home_page
# from . import patient_page 
from flicker_controller import FlickerController

class LoadingScreen(QWidget):
    def __init__(self):
        super().__init__()
        # Set size for 7-inch display (assuming 1024x600 resolution)
        self.setFixedSize(1024, 600)
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.CustomizeWindowHint | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        globaladc.buzzer_3()
        globaladc.fan_on()
        self.label = QLabel(self)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setGeometry(0, 0, 1024, 600)
        run_in_thread("patient_data","http://localhost:5600/patient/sync/",'wifi_status.py')

        # Replace 'path/to/your/logo.png' with the actual path to your logo
        self.pixmap = QPixmap('logo.png')
        self.label.setPixmap(self.pixmap.scaled(1, 1, Qt.KeepAspectRatio, Qt.SmoothTransformation))

        self.timer = QTimer()
        self.timer.timeout.connect(self.animate_logo)
        self.timer.start(50)  # Adjust for faster/slower animation
        wifi_checker_main()
        self.counter = 0

    def animate_logo(self):
        self.counter += 1
        if self.counter <= 40:
            # Zoom in
            size = min(self.counter * 25, 600)  # Max size is screen width
            self.label.setPixmap(self.pixmap.scaled(size, size, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        elif self.counter <= 50:
            # Hold at full size
            pass
        elif self.counter <= 60:
            # Fade out
            opacity = self.windowOpacity()
            self.setWindowOpacity(opacity - 0.1)
        else:
            # Animation complete, move to next page
            self.timer.stop()
            self.close()
            self.next_page()

    def next_page(self):
        # Show WriteUPImageForm
        self.writeup_form = QWidget()
        self.writeup_form.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)  # Remove window decorations
        self.writeup_form.setFixedSize(1024, 600)  # Set size to match display
        self.writeup_ui = WriteUPImageForm()
        self.writeup_ui.setupUi(self.writeup_form)
        self.writeup_form.installEventFilter(self)
        self.writeup_form.show()

    def eventFilter(self, obj, event):
        if obj == self.writeup_form and event.type() in [QEvent.MouseButtonPress, QEvent.TouchBegin]:
            self.show_login_form()
            return True
        return super().eventFilter(obj, event)

    def show_login_form(self):
        # Create login form
        self.login_form = QWidget()
        self.login_ui = Login_page()
        self.login_ui.setupUi(self.login_form)

        # Set up fade-in animation for login form
        self.fade_in_animation = QPropertyAnimation(self.login_form, b"windowOpacity")
        self.fade_in_animation.setDuration(500)
        self.fade_in_animation.setStartValue(0)
        self.fade_in_animation.setEndValue(1)
        self.fade_in_animation.setEasingCurve(QEasingCurve.InOutQuad)

        # Set up fade-out animation for writeup form
        self.fade_out_animation = QPropertyAnimation(self.writeup_form, b"windowOpacity")
        self.fade_out_animation.setDuration(500)
        self.fade_out_animation.setStartValue(1)
        self.fade_out_animation.setEndValue(0)
        self.fade_out_animation.setEasingCurve(QEasingCurve.InOutQuad)
        self.fade_out_animation.finished.connect(self.writeup_form.close)

        # Show login form and start animations
        self.login_form.show()
        self.fade_in_animation.start()
        self.fade_out_animation.start()



class Login_page(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1024, 600)
        Form.setStyleSheet("background-color:black;")
        Form.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.wifi_window = None  # Initialize as None
        # Initialize keyboard tracking variables
        self.form = Form
        self.json_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "user_data")
        # Create directory if it doesn't exist
        if not os.path.exists(self.json_path):
            os.makedirs(self.json_path)
        self.rpi_keyboard = RPiKeyboard()
        self.rpi_keyboard.show()
        
        

        self.frame = QtWidgets.QFrame(Form)
        self.frame.setGeometry(QtCore.QRect(0, 0, 1024, 40))
        self.frame.setStyleSheet("background-color:#1f2836;")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")

        #database initalize
        self.db = DatabaseConnection()
        self.db.connect()

        self.label_2 = QtWidgets.QLabel(self.frame)
        self.label_2.setGeometry(QtCore.QRect(60, 0, 281, 41))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet("color:white;")
        self.label_2.setObjectName("label_2")

        self.label_3 = QtWidgets.QLabel(self.frame)
        self.label_3.setGeometry(QtCore.QRect(930, 0, 71, 41))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(14)
        font.setBold(False)
        font.setWeight(50)
        self.label_3.setFont(font)
        self.label_3.setStyleSheet("color:white;")
        self.label_3.setObjectName("label_3")

        self.label_9 = QtWidgets.QLabel(self.frame)
        self.label_9.setGeometry(QtCore.QRect(5, 8, 44, 23))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.label_9.setFont(font)
        self.label_9.setText("")
        self.label_9.setPixmap(QtGui.QPixmap(":/newPrefix/Vekaria Healthcare Logo/VHC Logo.png"))
        self.label_9.setScaledContents(True)
        self.label_9.setObjectName("label_9")

        self.wifiIcon = WifiStatusLabel(self.frame)
        self.wifiIcon.setGeometry(QtCore.QRect(868, 5, 41, 31))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.wifiIcon.setFont(font)
        self.wifiIcon.setPixmap(QtGui.QPixmap(":/vlogo/logo12.png"))
        self.wifiIcon.clicked.connect(self.open_wifi_page)
        # self.wifiIcon.icked.connect(self.wifi_update)

        self.label_4 = QtWidgets.QLabel(Form)
        self.label_4.setGeometry(QtCore.QRect(0, 50, 1024, 40))
        font = QtGui.QFont()
        font.setFamily("Helvetica Rounded")
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.label_4.setFont(font)
        self.label_4.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_4.setStyleSheet("QFrame{\n"
"background:none;\n"
"color:#f2f5f3;\n"
"}")
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName("label_4")

        self.frame_2 = QtWidgets.QFrame(Form)
        self.frame_2.setGeometry(QtCore.QRect(200, 115, 624, 430))
        self.frame_2.setStyleSheet("QFrame{\n"
"background-color:#1f2836;\n"
"border-radius:30px;\n"
"border:1px solid white;\n"
"\n"
"};\n"
"color:white;")
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")

        # Username field setup
        self.username = QtWidgets.QLineEdit(self.frame_2)
        self.username.setGeometry(QtCore.QRect(62, 50, 500, 61))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.username.setFont(font)
        self.username.setStyleSheet(" QLineEdit {\n"
"                background-color: #334155;\n"
"                border:1px solid white;\n"
"                border-radius: 15px;\n"
"                padding: 5px;\n"
"                padding-left: 30px;\n"
"                color: #94a3b8;\n"
"            }")
        self.username.setObjectName("username")
        # self.username.installEventFilter(self)

        # Password field setup
        self.password = QtWidgets.QLineEdit(self.frame_2)
        self.password.setGeometry(QtCore.QRect(62, 140, 500, 61))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.password.setFont(font)
        self.password.setStyleSheet(" QLineEdit {\n"
"                background-color: #334155;\n"
"                border: 1px solid white;\n"
"                border-radius: 15px;\n"
"                padding: 5px;\n"
"                padding-left: 30px;\n"
"                color: #94a3b8;\n"
"            }")
        self.password.setObjectName("password")
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        # self.password.installEventFilter(self)

        # Password toggle button
        self.togglePassword = QtWidgets.QPushButton(self.frame_2)
        self.togglePassword.setGeometry(QtCore.QRect(570, 155, 30, 30))
        self.togglePassword.setStyleSheet("""
            QPushButton {
                border: none;
                background-color: transparent;
                color: white;
            }
        """)
        self.togglePassword.setText("👁")
        self.togglePassword.clicked.connect(self.toggle_password_visibility)
        self.password_visible = False

        self.login = QtWidgets.QPushButton(self.frame_2)
        self.login.setGeometry(QtCore.QRect(230, 350, 161, 51))
        font = QtGui.QFont()
        font.setPointSize(-1)
        font.setBold(True)
        font.setWeight(75)
        self.login.setFont(font)
        self.login.setStyleSheet("\n"
"    QPushButton {\n"
"        background-color: transparent;\n"
"        color: white;\n"
"        border: 1px solid white;\n"
"        padding: 10px 20px;\n"
"        font-size: 24px;\n"
"        border-radius: 1px;\n"
"        font-weight: bold;\n"
"        transition: all 0.3s;\n"
"        margin: 2px;\n"
"        border-bottom: 1px solid white;\n"
"        border-right: 1px solid white;\n"
"    }\n"
"    QPushButton:hover {\n"
"        background-color: rgba(33, 150, 243, 0.1);\n"
"        border: 2px solid #64B5F6;\n"
"        color: #64B5F6;\n"
"        border-bottom: 4px solid #42A5F5;\n"
"        border-right: 3px solid #42A5F5;\n"
"        margin: 2px;\n"
"    }\n"
"    QPushButton:pressed {\n"
"        background-color: rgba(33, 150, 243, 0.2);\n"
"        border: 2px solid white;\n"
"        border-bottom: 2px solid white;\n"
"        border-right: 2px solid white;\n"
"        margin-top: 4px;\n"
"        margin-left: 2px;\n"
"        padding-top: 11px;\n"
"        padding-left: 21px;\n"
"    }\n"
"    QPushButton:disabled {\n"
"        background-color: transparent;\n"
"        color: #B0B0B0;\n"
"        border: 2px solid #B0B0B0;\n"
"        border-bottom: 4px solid #909090;\n"
"        border-right: 3px solid #909090;\n"
"    }")
        self.login.setObjectName("login")

        self.label_7 = QtWidgets.QLabel(self.frame_2)
        self.label_7.setGeometry(QtCore.QRect(112, 210, 400, 71))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.label_7.setFont(font)
        self.label_7.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_7.setStyleSheet("QFrame{\n"
"backgorund:none;\n"
"border:none;\n"
"color:#f2f5f3;\n"
"}")
        self.label_7.setAlignment(QtCore.Qt.AlignCenter)
        self.label_7.setObjectName("label_7")

        self.frame_3 = QtWidgets.QFrame(self.frame_2)
        self.frame_3.setGeometry(QtCore.QRect(110, 270, 491, 41))
        self.frame_3.setStyleSheet("border:none;")
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")

        # Radio buttons setup with new styling
        self.frame_3.setStyleSheet("""
            QFrame {
                border: none;
                background: transparent;
            }
            
            QRadioButton {
                color: white;
                border-radius: 10px;
            }
            
            QRadioButton::indicator {
                width: 18px;
                height: 18px;
                border-radius: 9px;
                
            }
            
            QRadioButton::indicator:checked {
                background-color: #42A5F5;
                
            }
            
            QRadioButton:checked {
                background-color: rgba(66, 165, 245, 0.2);
                
            }
        """)

        # Radio buttons setup
        self.radioButton = QtWidgets.QRadioButton(self.frame_3)
        self.radioButton.setGeometry(QtCore.QRect(11, 11, 106, 19))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.radioButton.setFont(font)
        self.radioButton.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.radioButton.setStyleSheet("QRadioButton{\n"
"color:white;\n"
"background:none;\n"
"}")
        self.radioButton.setChecked(False)
        self.radioButton.setObjectName("radioButton")

        self.radioButton_2 = QtWidgets.QRadioButton(self.frame_3)
        self.radioButton_2.setEnabled(True)
        self.radioButton_2.setGeometry(QtCore.QRect(190, 11, 80, 19))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.radioButton_2.setFont(font)
        self.radioButton_2.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.radioButton_2.setStyleSheet("QRadioButton{\n"
"color:white;\n"
"background:none;\n"
"align-item:center;\n"
"align-content:center;\n"
"justify-content:center;\n"
"}")
        self.radioButton_2.setChecked(True)
        self.radioButton_2.setObjectName("radioButton_2")

        self.radioButton_3 = QtWidgets.QRadioButton(self.frame_3)
        self.radioButton_3.setGeometry(QtCore.QRect(328, 11, 71, 19))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.radioButton_3.setFont(font)
        self.radioButton_3.setStyleSheet("QRadioButton{\n"
"color:white;\n"
"background:none;\n"
"}")
        self.radioButton_3.setObjectName("radioButton_3")

        # Time and date labels
        self.Time = QtWidgets.QLabel(Form)
        self.Time.setGeometry(QtCore.QRect(960, 550, 55, 16))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        self.Time.setFont(font)
        self.Time.setStyleSheet("color:white;")
        self.Time.setObjectName("Time")

        self.date = QtWidgets.QLabel(Form)
        self.date.setGeometry(QtCore.QRect(934, 570, 71, 20))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        self.date.setFont(font)
        self.date.setStyleSheet("color:white;")
        self.date.setObjectName("date")

        # Setup timer for date and time updates
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_datetime)
        self.timer.start(1000)  # Update every second
        
        # Initial datetime update
        self.update_datetime()
        # Add this to the setupUi method
# Add this to the setupUi method
# Add this to the setupUi method
        self.rpi_keyboard = RPiKeyboard(Form)
        self.rpi_keyboard.move(Form.x(), Form.y() + Form.height())
        self.rpi_keyboard.username_field = self.username
        self.username.mousePressEvent = lambda event: self.rpi_keyboard.show_keyboard()
        self.password.mousePressEvent = lambda event: self.rpi_keyboard.show_keyboard()
        
        self.retranslateUi(Form)
        self.wifiIcon.clicked.connect(self.open_wifi_page)
        self.login.clicked.connect(self.handle_login)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def open_wifi_page(self):
        globaladc.buzzer_1()
        if self.wifi_window is None:
            self.wifi_window = WifiPage()
            self.wifi_window.show()
        else:
            self.wifi_window.activateWindow()


    def show_flicker_controller(self):
        pass

    def return_to_login(self):
        """Return to login page when home button is clicked"""
        # Hide flicker controller
        if hasattr(self, 'flicker_window'):
            self.flicker_window.hide()
            self.flicker_window.deleteLater()
            self.flicker_window = None
        
        # Clear the login form
        self.username.clear()
        self.password.clear()
        self.radioButton_2.setChecked(True)  # Reset to Clinic mode
        
        # Show the login form again
        self.form.show()


    def update_datetime(self):
        """Update the date and time labels with current values"""
        current_datetime = QDateTime.currentDateTime()
        self.Time.setText(current_datetime.toString('HH:mm'))
        self.date.setText(current_datetime.toString('dd-MM-yyyy'))

    def check_wifi_status(self):
        """
        Check the WiFi connection status based on the 'wifi_status.json' file.
        Perform different actions based on the connection status.

        Args:
            app_dir (str): The directory where the 'wifi_status.json' file is located.

        Returns:
            None
        """
        wifi_status_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'wifi_status.json')

        if os.path.exists(wifi_status_file):
            try:
                with open(wifi_status_file, 'r') as f:
                    wifi_status = json.load(f)

                if wifi_status['wifi_connected']:
                    # Perform actions when WiFi is connected
                    print("WiFi is connected. You can proceed with your application.")
                else:
                    # Perform actions when WiFi is not connected
                    print("WiFi is not connected. Please connect to the network.")
            except (FileNotFoundError, json.JSONDecodeError):
                print("Error: Could not read the 'wifi_status.json' file.")
        else:
            print("Error: 'wifi_status.json' file not found.")


    def closeEvent(self, event):
        """Clean up keyboard process when closing"""
        self.hide_keyboard()
        event.accept()

    def toggle_password_visibility(self):
        """Toggle password field visibility"""
        self.password_visible = not self.password_visible
        if self.password_visible:
            self.password.setEchoMode(QtWidgets.QLineEdit.Normal)
            self.togglePassword.setText("🔒")
        else:
            self.password.setEchoMode(QtWidgets.QLineEdit.Password)
            self.togglePassword.setText("👁")



    def generate_user_json(self, user_data,opeartion_mode):
        """Generate JSON file with user information"""
        try:
            # Create user info dictionary
            user_info = {
                "username": user_data['username'],
                "first_name": user_data['first_name'],
                "last_name": user_data['last_name'],
                "title": user_data['title'] if user_data['title'] else "",
                "login_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "is_doctor": user_data['is_doctor'],
                "is_operator": user_data['is_operator'],
                "user_id": user_data['id'],
                'opeartion_mode':opeartion_mode
                
            }

            # Create filename with timestamp
            filename = f"user_{user_data['username']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            filepath = os.path.join(self.json_path, filename)

            # Write to JSON file
            with open(filepath, 'w') as json_file:
                json.dump(user_info, json_file, indent=4)

            # Also create/update a latest user file
            latest_filepath = os.path.join(self.json_path, "latest_user.json")
            with open(latest_filepath, 'w') as json_file:
                json.dump(user_info, json_file, indent=4)

            return filepath
        except Exception as e:
            print(f"Error generating user JSON: {e}")
            return None
    def handle_login(self):
        """Handle login button click"""
        globaladc.buzzer_1()
        username = self.username.text().strip()
        password = self.password.text().strip()

        if not username or not password:
            # messagebox.showwarning('Error', 'Please enter both username and password')
            QMessageBox.warning(None, "Error", "Please enter both username and password")
            

            return

        # Get selected operation mode
        if self.radioButton.isChecked():
            operation_mode = "Eye Camp"
        elif self.radioButton_2.isChecked():
            operation_mode = "Clinic"
        else:
            operation_mode = "Demo"

        # Verify login
        user = self.db.verify_login(username, password)

        if user:
            # Generate JSON file
            json_file = self.generate_user_json(user,operation_mode)
            if json_file:
                QMessageBox.information(None, "Success", f'Welcome {user["title"] + " " if user["title"] else ""}{user["first_name"]} {user["last_name"]}')


                # Create and show the FlickerController instance
                # self.show_flicker_controller()
                self.form.hide()
                self.doctor_window = QtWidgets.QWidget()
                self.doctor_ui = HomePpage()  # From doctor.py
                self.doctor_ui.setupUi(self.doctor_window)
                self.doctor_window.show()
            else:
                QMessageBox.warning(None, "Warning", 'Login successful but failed to save user data')
        else:
            QMessageBox.critical(None, "Error", 'Invalid username or password')

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label_2.setText(_translate("Form", "Vekaria Healthcare"))
        self.label_3.setText(_translate("Form", "V1.0"))
        self.label_4.setText(_translate("Form", "Macular Densitometer"))
        self.username.setPlaceholderText(_translate("Form", "Username"))
        self.password.setPlaceholderText(_translate("Form", "Password"))
        self.login.setText(_translate("Form", "LOGIN"))
        self.label_7.setText(_translate("Form", "Operation Mode"))
        self.radioButton.setText(_translate("Form", "Eye Camp"))
        self.radioButton_2.setText(_translate("Form", "Clinic"))
        self.radioButton_3.setText(_translate("Form", "Demo"))


class HomePpage(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1024, 600)
        Form.setStyleSheet("background-color:#101826;")
        Form.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.form = Form
        self.frame = QtWidgets.QFrame(Form)
        self.frame.setGeometry(QtCore.QRect(0, 0, 1024, 40))
        self.frame.setStyleSheet("background-color:black;")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.label_2 = QtWidgets.QLabel(self.frame)
        self.label_2.setGeometry(QtCore.QRect(60, 0, 281, 41))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet("color:white;")
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.frame)
        self.label_3.setGeometry(QtCore.QRect(930, 0, 71, 41))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(14)
        font.setBold(False)
        font.setWeight(50)
        self.label_3.setFont(font)
        self.label_3.setStyleSheet("color:white;")
        self.label_3.setObjectName("label_3")
        self.label_9 = QtWidgets.QLabel(self.frame)
        self.label_9.setGeometry(QtCore.QRect(5, 8, 44, 23))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.label_9.setFont(font)
        self.label_9.setText("")
        self.label_9.setPixmap(QtGui.QPixmap(":/newPrefix/Vekaria Healthcare Logo/VHC Logo.png"))
        self.label_9.setScaledContents(True)
        self.label_9.setObjectName("label_9")
        self.wifiIcon = WifiStatusLabel(self.frame)
        self.wifiIcon.setGeometry(QtCore.QRect(868, 5, 41, 31))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.wifiIcon.setFont(font)
        self.wifiIcon.setPixmap(QtGui.QPixmap(":/vlogo/logo12.png"))
        self.wifiIcon.clicked.connect(self.open_wifi_page)
        self.label_4 = QtWidgets.QLabel(Form)
        self.label_4.setGeometry(QtCore.QRect(0, 50, 1024, 40))
        font = QtGui.QFont()
        font.setFamily("Helvetica Rounded")
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.label_4.setFont(font)
        self.label_4.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_4.setStyleSheet("QFrame{\n"
"background:none;\n"
"color:#f2f5f3;\n"
"}")
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(960, 550, 55, 16))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        self.label.setFont(font)
        self.label.setStyleSheet("color:white;")
        self.label.setObjectName("label")
        self.label_5 = QtWidgets.QLabel(Form)
        self.label_5.setGeometry(QtCore.QRect(934, 570, 71, 20))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        self.label_5.setFont(font)
        self.label_5.setStyleSheet("color:white;")
        self.label_5.setObjectName("label_5")
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(347, 150, 330, 61))
        font = QtGui.QFont()
        font.setPointSize(-1)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton.setFont(font)
        self.pushButton.clicked.connect(self.createUser)
        self.pushButton.setStyleSheet("\n"
"    QPushButton {\n"
"        background-color: transparent;\n"
"        color: white;\n"
"        border: 1px solid white;\n"
"        padding: 10px 20px;\n"
"        font-size: 24px;\n"
"        border-radius: 1px;\n"
"        font-weight: bold;\n"
"        transition: all 0.3s;\n"
"        margin: 2px;\n"
"        /* Add subtle initial shadow */\n"
"        border-bottom: 1px solid white;\n"
"        border-right: 1px solid white;\n"
"    }\n"
"    \n"
"    QPushButton:hover {\n"
"        background-color: rgba(33, 150, 243, 0.1);\n"
"        border: 2px solid #64B5F6;\n"
"        color: #64B5F6;\n"
"        /* Enhanced hover effect */\n"
"        border-bottom: 4px solid #42A5F5;\n"
"        border-right: 3px solid #42A5F5;\n"
"        margin: 2px;\n"
"    }\n"
"    \n"
"    QPushButton:pressed {\n"
"        background-color: rgba(33, 150, 243, 0.2);\n"
"        border: 2px solid #1976D2;\n"
"        /* Create pressed effect */\n"
"        border-bottom: 2px solid #1976D2;\n"
"        border-right: 2px solid #1976D2;\n"
"        margin-top: 4px;\n"
"        margin-left: 2px;\n"
"        padding-top: 11px;\n"
"        padding-left: 21px;\n"
"    }\n"
"    \n"
"    QPushButton:disabled {\n"
"        background-color: transparent;\n"
"        color: #B0B0B0;\n"
"        border: 2px solid #B0B0B0;\n"
"        border-bottom: 4px solid #909090;\n"
"        border-right: 3px solid #909090;\n"
"    }\n"
"")
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(Form)
        self.pushButton_2.setGeometry(QtCore.QRect(347, 280, 330, 61))
        font = QtGui.QFont()
        self.pushButton_2.clicked.connect(self.viewReports)
        font.setPointSize(-1)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setStyleSheet("\n"
"\n"
"    QPushButton {\n"
"        background-color: transparent;\n"
"        color: white;\n"
"        border: 1px solid white;\n"
"        padding: 10px 20px;\n"
"        font-size: 24px;\n"
"        border-radius: 1px;\n"
"        font-weight: bold;\n"
"        transition: all 0.3s;\n"
"        margin: 2px;\n"
"        /* Add subtle initial shadow */\n"
"        border-bottom: 1px solid white;\n"
"        border-right: 1px solid white;\n"
"    }\n"
"    QPushButton:hover {\n"
"        background-color: rgba(33, 150, 243, 0.1);\n"
"        border: 2px solid #64B5F6;\n"
"        color: #64B5F6;\n"
"        /* Enhanced hover effect */\n"
"        border-bottom: 4px solid #42A5F5;\n"
"        border-right: 3px solid #42A5F5;\n"
"        margin: 2px;\n"
"    }\n"
"    \n"
"    QPushButton:pressed {\n"
"        background-color: rgba(33, 150, 243, 0.2);\n"
"        border: 2px solid #1976D2;\n"
"        /* Create pressed effect */\n"
"        border-bottom: 2px solid #1976D2;\n"
"        border-right: 2px solid #1976D2;\n"
"        margin-top: 4px;\n"
"        margin-left: 2px;\n"
"        padding-top: 11px;\n"
"        padding-left: 21px;\n"
"    }\n"
"    \n"
"    QPushButton:disabled {\n"
"        background-color: transparent;\n"
"        color: #B0B0B0;\n"
"        border: 2px solid #B0B0B0;\n"
"        border-bottom: 4px solid #909090;\n"
"        border-right: 3px solid #909090;\n"
"    }\n"
"")
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_3 = QtWidgets.QPushButton(Form)
        self.pushButton_3.setGeometry(QtCore.QRect(347, 410, 330, 61))
        font = QtGui.QFont()
        self.pushButton_3.clicked.connect(self.testMode)
        font.setPointSize(-1)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_3.setFont(font)
        self.pushButton_3.setStyleSheet("\n"
"    QPushButton {\n"
"        background-color: transparent;\n"
"        color: white;\n"
"        border: 1px solid white;\n"
"        padding: 10px 20px;\n"
"        font-size: 24px;\n"
"        border-radius: 1px;\n"
"        font-weight: bold;\n"
"        transition: all 0.3s;\n"
"        margin: 2px;\n"
"        /* Add subtle initial shadow */\n"
"        border-bottom: 1px solid white;\n"
"        border-right: 1px solid white;\n"
"    }\n"
"    \n"
"    QPushButton:hover {\n"
"        background-color: rgba(33, 150, 243, 0.1);\n"
"        border: 2px solid #64B5F6;\n"
"        color: #64B5F6;\n"
"        /* Enhanced hover effect */\n"
"        border-bottom: 4px solid #42A5F5;\n"
"        border-right: 3px solid #42A5F5;\n"
"        margin: 2px;\n"
"    }\n"
"    \n"
"    QPushButton:pressed {\n"
"        background-color: rgba(33, 150, 243, 0.2);\n"
"        border: 2px solid #1976D2;\n"
"        /* Create pressed effect */\n"
"        border-bottom: 2px solid #1976D2;\n"
"        border-right: 2px solid #1976D2;\n"
"        margin-top: 4px;\n"
"        margin-left: 2px;\n"
"        padding-top: 11px;\n"
"        padding-left: 21px;\n"
"    }\n"
"    \n"
"    QPushButton:disabled {\n"
"        background-color: transparent;\n"
"        color: #B0B0B0;\n"
"        border: 2px solid #B0B0B0;\n"
"        border-bottom: 4px solid #909090;\n"
"        border-right: 3px solid #909090;\n"
"    }\n"
"")
        self.pushButton_3.setObjectName("pushButton_3")

        self.userInfoLabel = QtWidgets.QLabel(Form)
        self.userInfoLabel.setGeometry(QtCore.QRect(20, 150, 280, 40))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.userInfoLabel.setFont(font)
        self.userInfoLabel.setStyleSheet("color: white;")
        self.userInfoLabel.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.userInfoLabel.setObjectName("userInfoLabel")

        self.wifi_window = None
        self.pushButton_3.clicked.connect(self.testMode)
        self.check_user_role()
        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)
        
    def check_user_role(self):
        """Check user role from latest_user.json and show/hide buttons accordingly"""
        try:
            json_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "user_data", "latest_user.json")
            
            if os.path.exists(json_path):
                with open(json_path, 'r') as file:
                    user_data = json.load(file)
                
                # Check if user is an operator
                is_operator = user_data.get('is_operator', 0) == 1
                
                                # Check if user is an operator
                is_operator = user_data.get('is_operator', 0) == 1
                
                # Set user info label
                title = user_data.get('title', '')
                first_name = user_data.get('first_name', '')
                last_name = user_data.get('last_name', '')
                
                # Format user info with title if available
                if title:
                    user_info = f"Welcome,\n{title} {first_name} {last_name}"
                else:
                    user_info = f"Welcome,\n{first_name} {last_name}"
                
                self.userInfoLabel.setText(user_info)

                # Hide create user button only for operators
                self.pushButton.setVisible(not is_operator)
                
                # Show other buttons for everyone
                self.pushButton_2.setVisible(True)  # View Reports
                self.pushButton_3.setVisible(True)  # Test Mode
                
                if is_operator:
                    # If operator: move buttons up (original Create User and View Reports positions)
                    self.pushButton_2.setGeometry(QtCore.QRect(347, 150, 330, 61))  # Move View Reports up
                    self.pushButton_3.setGeometry(QtCore.QRect(347, 280, 330, 61))  # Move Test Mode up
                else:
                    # If not operator: set original positions for all buttons
                    self.pushButton.setGeometry(QtCore.QRect(347, 150, 330, 61))   # Create User at top
                    self.pushButton_2.setGeometry(QtCore.QRect(347, 280, 330, 61))  # View Reports in middle
                    self.pushButton_3.setGeometry(QtCore.QRect(347, 410, 330, 61))  # Test Mode at bottom
                
            else:
                # If no user data found, show error and hide all buttons
                QMessageBox.warning(self.form, 'Error', 'No user data found. Please log in again.')
                self.pushButton.setVisible(False)
                self.pushButton_2.setVisible(False)
                self.pushButton_3.setVisible(False)
                
        except Exception as e:
            QMessageBox.critical(self.form, 'Error', f'Error loading user data: {str(e)}')
            self.pushButton.setVisible(False)
            self.pushButton_2.setVisible(False)
            self.pushButton_3.setVisible(False)

    def open_wifi_page(self):
        globaladc.buzzer_1()
        if self.wifi_window is None:
            self.wifi_window = WifiPage()
            self.wifi_window.show()
        else:
            self.wifi_window.activateWindow()

    def viewReports(self):
        globaladc.buzzer_1()

    def createUser(self):
        globaladc.buzzer_1()

    def testMode(self):
        globaladc.buzzer_1()
        self.form.hide()
        self.patient_info_widow = QtWidgets.QWidget()
        self.patient_info = Patient_info()  
        self.patient_info.setupUi(self.patient_info_widow)
        self.patient_info_widow.show()

    def update_datetime(self):
        """Update the date and time labels with current values"""
        current_datetime = QDateTime.currentDateTime()
        self.label.setText(current_datetime.toString('HH:mm'))
        self.label_5.setText(current_datetime.toString('dd-MM-yyyy'))

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label_2.setText(_translate("Form", "Vekaria Healthcare"))
        self.label_3.setText(_translate("Form", "V1.0"))
        self.label_4.setText(_translate("Form", "Home Page"))
        # self.label.setText(_translate("Form", "19:53"))
        # self.userInfoLabel.setText(_translate("Form", "Welcome"))
        # self.label_5.setText(_translate("Form", "12-10-2024"))
        self.pushButton.setText(_translate("Form", "Create User"))
        self.pushButton_2.setText(_translate("Form", "View Reports"))
        self.pushButton_3.setText(_translate("Form", "Test Mode"))




class Patient_info(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1031, 586)
        Form.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        Form.setStyleSheet("background-color:black;\n"
"border:none;")
        self.frame_2 = QtWidgets.QFrame(Form)
        self.form  = Form
        self.frame_2.setGeometry(QtCore.QRect(20, 120, 981, 460))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.frame_2.setFont(font)

        
        # Radio buttons setup with new styling
        
        self.frame_2.setStyleSheet("background-color:black;\n"
"color:white;")
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.label_6 = QtWidgets.QLabel(self.frame_2)
        self.label_6.setGeometry(QtCore.QRect(0, 20, 121, 31))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(16)
        font.setBold(False)
        font.setWeight(50)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.textEdit = QtWidgets.QTextEdit(self.frame_2)
        self.frame_2.setStyleSheet("""
            
            QFrame {
                border: none;
                background: transparent;
                color:white;
            }
            
            QRadioButton {
                color: white;
                border-radius: 10px;
            }
            
            QRadioButton::indicator {
                width: 18px;
                height: 18px;
                border-radius: 9px;
                
            }
            
            QRadioButton::indicator:checked {
                background-color: #42A5F5;
                
            }
            

        """)
        self.textEdit.setGeometry(QtCore.QRect(139, 20, 190, 31))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.textEdit.setFont(font)
        self.textEdit.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.textEdit.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.textEdit.setStyleSheet(" QTextEdit {\n"
"                background-color: #334155;\n"
"                border:1px solid white;\n"
"                border-radius: 10px;\n"
"                padding: 5px;\n"
"                padding-left: 30px;\n"
"                color: #94a3b8;\n"
"            }\n"
"\n"
"\n"
"QTextEdit {\n"
"        padding: 0px;\n"
"        margin: 0px;\n"
"    }\n"
"    QTextBrowser {\n"
"        padding: 0px;\n"
"        margin: 0px;\n"
"    }\n"
"\n"
"QTextEdit QScrollBar:vertical {\n"
"        width: 0px;  /* This hides the vertical scrollbar */\n"
"    }\n"
"    QTextEdit QScrollBar:horizontal {\n"
"        height: 0px;  /* This hides the horizontal scrollbar */\n"
"    }")
        self.textEdit.setObjectName("textEdit")
        self.label_9 = QtWidgets.QLabel(self.frame_2)
        self.label_9.setGeometry(QtCore.QRect(344, 20, 191, 31))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(16)
        font.setBold(False)
        font.setWeight(50)
        self.label_9.setFont(font)
        self.label_9.setObjectName("label_9")
        self.textEdit_2 = QtWidgets.QTextEdit(self.frame_2)
        self.textEdit_2.setGeometry(QtCore.QRect(491, 20, 165, 31))
        self.textEdit_2 = QtWidgets.QTextEdit(self.frame_2)
        self.textEdit_2.setGeometry(QtCore.QRect(491, 20, 165, 31))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.textEdit_2.setFont(font)
        self.textEdit_2.setStyleSheet(" QTextEdit {\n"
"                background-color: #334155;\n"
"                border:1px solid white;\n"
"                border-radius: 10px;\n"
"                padding: 5px;\n"
"                padding-left: 30px;\n"
"                color: #94a3b8;\n"
"            }\n"
"\n"
"\n"
"QTextEdit {\n"
"        padding: 0px;\n"
"        margin: 0px;\n"
"    }\n"
"    QTextBrowser {\n"
"        padding: 0px;\n"
"        margin: 0px;\n"
"    }\n"
"\n"
"QTextEdit QScrollBar:vertical {\n"
"        width: 0px;  /* This hides the vertical scrollbar */\n"
"    }\n"
"    QTextEdit QScrollBar:horizontal {\n"
"        height: 0px;  /* This hides the horizontal scrollbar */\n"
"    }")
        self.textEdit_2.setObjectName("textEdit_2")
        self.textEdit_3 = QtWidgets.QTextEdit(self.frame_2)
        self.textEdit_3.setGeometry(QtCore.QRect(801, 20, 175, 31))
        self.textEdit_3.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.textEdit_3.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.textEdit_2.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.textEdit_2.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.textEdit_3.setFont(font)
        self.textEdit_3.setStyleSheet(" QTextEdit {\n"
"                background-color: #334155;\n"
"                border:1px solid white;\n"
"                border-radius: 10px;\n"
"                padding: 5px;\n"
"                padding-left: 30px;\n"
"                color: #94a3b8;\n"
"            }\n"
"\n"
"\n"
"QTextEdit {\n"
"        padding: 0px;\n"
"        margin: 0px;\n"
"    }\n"
"    QTextBrowser {\n"
"        padding: 0px;\n"
"        margin: 0px;\n"
"    }\n"
"\n"
"QTextEdit QScrollBar:vertical {\n"
"        width: 0px;  /* This hides the vertical scrollbar */\n"
"    }\n"
"    QTextEdit QScrollBar:horizontal {\n"
"        height: 0px;  /* This hides the horizontal scrollbar */\n"
"    }")
        self.textEdit_3.setObjectName("textEdit_3")
        self.label_10 = QtWidgets.QLabel(self.frame_2)
        self.label_10.setGeometry(QtCore.QRect(670, 20, 121, 31))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(16)
        font.setBold(False)
        font.setWeight(50)
        self.label_10.setFont(font)
        self.label_10.setObjectName("label_10")
        self.label_7 = QtWidgets.QLabel(self.frame_2)
        self.label_7.setGeometry(QtCore.QRect(0, 80, 141, 31))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(16)
        font.setBold(False)
        font.setWeight(50)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")
        self.textEdit_4 = QtWidgets.QTextEdit(self.frame_2)
        self.textEdit_4.setGeometry(QtCore.QRect(141, 80, 190, 31))
        self.textEdit_4.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.textEdit_4.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.textEdit_4.setFont(font)
        self.textEdit_4.setStyleSheet(" QTextEdit {\n"
"                background-color: #334155;\n"
"                border:1px solid white;\n"
"                border-radius: 10px;\n"
"                padding: 5px;\n"
"                padding-left: 30px;\n"
"                color: #94a3b8;\n"
"            }\n"
"\n"
"\n"
"QTextEdit {\n"
"        padding: 0px;\n"
"        margin: 0px;\n"
"    }\n"
"    QTextBrowser {\n"
"        padding: 0px;\n"
"        margin: 0px;\n"
"    }\n"
"\n"
"QTextEdit QScrollBar:vertical {\n"
"        width: 0px;  /* This hides the vertical scrollbar */\n"
"    }\n"
"    QTextEdit QScrollBar:horizontal {\n"
"        height: 0px;  /* This hides the horizontal scrollbar */\n"
"    }")
        self.textEdit_4.setObjectName("textEdit_4")
        self.label_8 = QtWidgets.QLabel(self.frame_2)
        self.label_8.setGeometry(QtCore.QRect(0, 140, 121, 31))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(16)
        font.setBold(False)
        font.setWeight(50)
        self.label_8.setFont(font)
        self.label_8.setObjectName("label_8")
        self.label_11 = QtWidgets.QLabel(self.frame_2)
        self.label_11.setGeometry(QtCore.QRect(346, 80, 131, 31))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(16)
        font.setBold(False)
        font.setWeight(50)
        self.label_11.setFont(font)
        self.label_11.setObjectName("label_11")
        self.textEdit_5 = QtWidgets.QTextEdit(self.frame_2)
        self.textEdit_5.setGeometry(QtCore.QRect(487, 80, 165, 31))
        self.textEdit_5.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.textEdit_5.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.textEdit_5.setFont(font)
        self.textEdit_5.setStyleSheet(" QTextEdit {\n"
"                background-color: #334155;\n"
"                border:1px solid white;\n"
"                border-radius: 10px;\n"
"                padding: 5px;\n"
"                padding-left: 30px;\n"
"                color: #94a3b8;\n"
"            }\n"
"\n"
"\n"
"QTextEdit {\n"
"        padding: 0px;\n"
"        margin: 0px;\n"
"    }\n"
"    QTextBrowser {\n"
"        padding: 0px;\n"
"        margin: 0px;\n"
"    }\n"
"\n"
"QTextEdit QScrollBar:vertical {\n"
"        width: 0px;  /* This hides the vertical scrollbar */\n"
"    }\n"
"    QTextEdit QScrollBar:horizontal {\n"
"        height: 0px;  /* This hides the horizontal scrollbar */\n"
"    }")
        self.textEdit_5.setObjectName("textEdit_5")
        self.label_12 = QtWidgets.QLabel(self.frame_2)
        self.label_12.setGeometry(QtCore.QRect(676, 80, 121, 31))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(16)
        font.setBold(False)
        font.setWeight(50)
        self.label_12.setFont(font)
        self.label_12.setObjectName("label_12")
        self.textEdit_6 = QtWidgets.QTextEdit(self.frame_2)
        self.textEdit_6.setGeometry(QtCore.QRect(802, 80, 175, 31))
        self.textEdit_6.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.textEdit_6.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.textEdit_6.setFont(font)
        self.textEdit_6.setStyleSheet(" QTextEdit {\n"
"                background-color: #334155;\n"
"                border:1px solid white;\n"
"                border-radius: 10px;\n"
"                padding: 5px;\n"
"                padding-left: 30px;\n"
"                color: #94a3b8;\n"
"            }\n"
"\n"
"\n"
"QTextEdit {\n"
"        padding: 0px;\n"
"        margin: 0px;\n"
"    }\n"
"    QTextBrowser {\n"
"        padding: 0px;\n"
"        margin: 0px;\n"
"    }\n"
"\n"
"QTextEdit QScrollBar:vertical {\n"
"        width: 0px;  /* This hides the vertical scrollbar */\n"
"    }\n"
"    QTextEdit QScrollBar:horizontal {\n"
"        height: 0px;  /* This hides the horizontal scrollbar */\n"
"    }")
        self.textEdit_6.setObjectName("textEdit_6")
        self.label_13 = QtWidgets.QLabel(self.frame_2)
        self.label_13.setGeometry(QtCore.QRect(0, 200, 121, 31))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(16)
        font.setBold(False)
        font.setWeight(50)
        self.label_13.setFont(font)
        self.label_13.setObjectName("label_13")
        self.label_22 = QtWidgets.QLabel(self.frame_2)
        self.label_22.setGeometry(QtCore.QRect(0, 260, 121, 31))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(16)
        font.setBold(False)
        font.setWeight(50)
        self.label_22.setFont(font)
        self.label_22.setObjectName("label_22")
        self.label_23 = QtWidgets.QLabel(self.frame_2)
        self.label_23.setGeometry(QtCore.QRect(450, 260, 121, 31))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(16)
        font.setBold(False)
        font.setWeight(50)
        self.label_23.setFont(font)
        self.label_23.setObjectName("label_23")
        self.Diabetes_text = QtWidgets.QTextEdit(self.frame_2)
        self.Diabetes_text.setGeometry(QtCore.QRect(830, 260, 141, 31))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(16)
        font.setBold(False)
        font.setWeight(50)
        self.Diabetes_text.setFont(font)
        self.Diabetes_text.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.Diabetes_text.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.Diabetes_text.setStyleSheet(" QTextEdit {\n"
"                background-color: #334155;\n"
"                border:1px solid white;\n"
"                border-radius: 10px;\n"
"                padding: 5px;\n"
"                padding-left: 30px;\n"
"                color: #94a3b8;\n"
"            }\n"
"\n"
"\n"
"QTextEdit {\n"
"        padding: 0px;\n"
"        margin: 0px;\n"
"    }\n"
"    QTextBrowser {\n"
"        padding: 0px;\n"
"        margin: 0px;\n"
"    }\n"
"\n"
"QTextEdit QScrollBar:vertical {\n"
"        width: 0px;  /* This hides the vertical scrollbar */\n"
"    }\n"
"    QTextEdit QScrollBar:horizontal {\n"
"        height: 0px;  /* This hides the horizontal scrollbar */\n"
"    }")
        self.Diabetes_text.setObjectName("Diabetes_text")
        self.label_24 = QtWidgets.QLabel(self.frame_2)
        self.label_24.setGeometry(QtCore.QRect(450, 200, 200, 31))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(16)
        font.setBold(False)
        font.setWeight(50)
        self.label_24.setFont(font)
        self.label_24.setObjectName("label_24")
        self.label_26 = QtWidgets.QLabel(self.frame_2)
        self.label_26.setGeometry(QtCore.QRect(0, 320, 141, 31))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(16)
        font.setBold(False)
        font.setWeight(50)
        self.label_26.setFont(font)
        self.label_26.setObjectName("label_26")
        self.Diabetes_text_2 = QtWidgets.QTextEdit(self.frame_2)
        self.Diabetes_text_2.setGeometry(QtCore.QRect(830, 200, 141, 31))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(16)
        font.setBold(False)
        font.setWeight(50)
        self.Diabetes_text_2.setFont(font)
        self.Diabetes_text_2.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.Diabetes_text_2.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.Diabetes_text_2.setStyleSheet(" QTextEdit {\n"
"                background-color: #334155;\n"
"                border:1px solid white;\n"
"                border-radius: 10px;\n"
"                padding: 5px;\n"
"                padding-left: 30px;\n"
"                color: #94a3b8;\n"
"            }\n"
"\n"
"\n"
"QTextEdit {\n"
"        padding: 0px;\n"
"        margin: 0px;\n"
"    }\n"
"    QTextBrowser {\n"
"        padding: 0px;\n"
"        margin: 0px;\n"
"    }\n"
"\n"
"QTextEdit QScrollBar:vertical {\n"
"        width: 0px;  /* This hides the vertical scrollbar */\n"
"    }\n"
"    QTextEdit QScrollBar:horizontal {\n"
"        height: 0px;  /* This hides the horizontal scrollbar */\n"
"    }")
        self.Diabetes_text_2.setObjectName("Diabetes_text_2")
        self.pushButton_2 = QtWidgets.QPushButton(self.frame_2)
        self.pushButton_2.setGeometry(QtCore.QRect(410, 390, 161, 51))
        font = QtGui.QFont()
        font.setPointSize(-1)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setStyleSheet("\n"
"    QPushButton {\n"
"        background-color: transparent;\n"
"        color: white;\n"
"        border: 1px solid white;\n"
"        padding: 10px 20px;\n"
"        font-size: 24px;\n"
"        border-radius: 1px;\n"
"        font-weight: bold;\n"
"        transition: all 0.3s;\n"
"        margin: 2px;\n"
"        /* Add subtle initial shadow */\n"
"        border-bottom: 1px solid white;\n"
"        border-right: 1px solid white;\n"
"    }\n"
"    \n"
"    QPushButton:hover {\n"
"        background-color: rgba(33, 150, 243, 0.1);\n"
"        border: 2px solid #64B5F6;\n"
"        color: #64B5F6;\n"
"        /* Enhanced hover effect */\n"
"        border-bottom: 4px solid #42A5F5;\n"
"        border-right: 3px solid #42A5F5;\n"
"        margin: 2px;\n"
"    }\n"
"    \n"
"    QPushButton:pressed {\n"
"        background-color: rgba(33, 150, 243, 0.2);\n"
"        border: 2px solid white;\n"
"        /* Create pressed effect */\n"
"        border-bottom: 2px solid white;\n"
"        border-right: 2px solid white;\n"
"        margin-top: 4px;\n"
"        margin-left: 2px;\n"
"        padding-top: 11px;\n"
"        padding-left: 21px;\n"
"    }\n"
"    \n"
"    QPushButton:disabled {\n"
"        background-color: transparent;\n"
"        color: #B0B0B0;\n"
"        border: 2px solid #B0B0B0;\n"
"        border-bottom: 4px solid #909090;\n"
"        border-right: 3px solid #909090;\n"
"    }\n"
"")
        self.pushButton_2.setObjectName("pushButton_2")
        self.Acho_no = QtWidgets.QRadioButton(self.frame_2)
        self.Acho_no.setGeometry(QtCore.QRect(276, 200, 95, 31))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(16)
        font.setBold(False)
        font.setWeight(50)
        self.Acho_no.setFont(font)
        self.Acho_no.setChecked(False)
        self.Acho_no.setObjectName("Acho_no")
        self.Alcho_yes = QtWidgets.QRadioButton(self.frame_2)
        self.Alcho_yes.setGeometry(QtCore.QRect(157, 200, 95, 31))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(16)
        font.setBold(False)
        font.setWeight(50)
        self.Alcho_yes.setFont(font)
        self.Alcho_yes.setObjectName("Alcho_yes")
        self.male = QtWidgets.QRadioButton(self.frame_2)
        self.male.setGeometry(QtCore.QRect(157, 140, 95, 31))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(16)
        font.setBold(False)
        font.setWeight(50)
        self.male.setFont(font)
        self.male.setChecked(False)
        self.male.setObjectName("male")
        self.female = QtWidgets.QRadioButton(self.frame_2)
        self.female.setGeometry(QtCore.QRect(276, 140, 141, 31))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(16)
        font.setBold(False)
        font.setWeight(50)
        self.female.setFont(font)
        self.female.setObjectName("female")
        self.Dia_yes = QtWidgets.QRadioButton(self.frame_2)
        self.Dia_yes.setGeometry(QtCore.QRect(660, 260, 95, 31))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(16)
        font.setBold(False)
        font.setWeight(50)
        self.Dia_yes.setFont(font)
        self.Dia_yes.setObjectName("Dia_yes")
        self.Dia_no = QtWidgets.QRadioButton(self.frame_2)
        self.Dia_no.setGeometry(QtCore.QRect(750, 260, 61, 31))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(16)
        font.setBold(False)
        font.setWeight(50)
        self.Dia_no.setFont(font)
        self.Dia_no.setChecked(False)
        self.Dia_no.setObjectName("Dia_no")
        self.Bp_yes = QtWidgets.QRadioButton(self.frame_2)
        self.Bp_yes.setGeometry(QtCore.QRect(660, 200, 95, 31))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(16)
        font.setBold(False)
        font.setWeight(50)
        self.Bp_yes.setFont(font)
        self.Bp_yes.setObjectName("Bp_yes")
        self.Bp_no = QtWidgets.QRadioButton(self.frame_2)
        self.Bp_no.setGeometry(QtCore.QRect(750, 200, 61, 31))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(16)
        font.setBold(False)
        font.setWeight(50)
        self.Bp_no.setFont(font)
        self.Bp_no.setChecked(False)
        self.Bp_no.setObjectName("Bp_no")
        self.Alcho_yes_2 = QtWidgets.QRadioButton(self.frame_2)
        self.Alcho_yes_2.setGeometry(QtCore.QRect(157, 260, 95, 31))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(16)
        font.setBold(False)
        font.setWeight(50)
        self.Alcho_yes_2.setFont(font)
        self.Alcho_yes_2.setObjectName("Alcho_yes_2")
        self.Acho_no_2 = QtWidgets.QRadioButton(self.frame_2)
        self.Acho_no_2.setGeometry(QtCore.QRect(276, 260, 95, 31))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(16)
        font.setBold(False)
        font.setWeight(50)
        self.Acho_no_2.setFont(font)
        self.Acho_no_2.setChecked(False)
        self.Acho_no_2.setObjectName("Acho_no_2")
        self.Alcho_yes_3 = QtWidgets.QRadioButton(self.frame_2)
        self.Alcho_yes_3.setGeometry(QtCore.QRect(157, 320, 95, 31))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(16)
        font.setBold(False)
        font.setWeight(50)
        self.Alcho_yes_3.setFont(font)
        self.Alcho_yes_3.setObjectName("Alcho_yes_3")
        self.Acho_no_3 = QtWidgets.QRadioButton(self.frame_2)
        self.Acho_no_3.setGeometry(QtCore.QRect(276, 320, 141, 31))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(16)
        font.setBold(False)
        font.setWeight(50)
        self.Acho_no_3.setFont(font)
        self.Acho_no_3.setChecked(False)
        self.Acho_no_3.setObjectName("Acho_no_3")
        self.label_14 = QtWidgets.QLabel(self.frame_2)
        self.label_14.setGeometry(QtCore.QRect(450, 140, 131, 31))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(16)
        font.setBold(False)
        font.setWeight(50)
        self.label_14.setFont(font)
        self.label_14.setObjectName("label_14")
        self.frame = QtWidgets.QFrame(self.frame_2)
        self.frame.setGeometry(QtCore.QRect(570, 130, 291, 51))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.eye_R = QtWidgets.QRadioButton(self.frame_2)
        self.eye_R.setGeometry(QtCore.QRect(660, 140, 95, 31))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(16)
        font.setBold(False)
        font.setWeight(50)
        self.eye_R.setFont(font)
        self.eye_R.setCheckable(True)
        self.eye_R.setChecked(True)
        self.eye_R.setObjectName("eye_R")
        self.eye_L = QtWidgets.QRadioButton(self.frame_2)
        self.eye_L.setGeometry(QtCore.QRect(750, 140, 61, 31))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(16)
        font.setBold(False)
        font.setWeight(50)
        self.eye_L.setFont(font)
        self.eye_L.setChecked(False)
        self.eye_L.setObjectName("eye_L")
        self.label_4 = QtWidgets.QLabel(Form)
        self.label_4.setGeometry(QtCore.QRect(10, 50, 1011, 41))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(18)
        font.setBold(False)
        font.setWeight(50)
        self.label_4.setFont(font)
        self.label_4.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_4.setStyleSheet("color:white")
        self.label_4.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label_4.setObjectName("label_4")
        self.frame_4 = QtWidgets.QFrame(Form)
        self.frame_4.setGeometry(QtCore.QRect(1, 0, 1024, 40))
        self.frame_4.setStyleSheet("background-color:#101826;")
        self.frame_4.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_4.setObjectName("frame_4")
        self.label_15 = QtWidgets.QLabel(self.frame_4)
        self.label_15.setGeometry(QtCore.QRect(60, 0, 281, 41))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.label_15.setFont(font)
        self.label_15.setStyleSheet("color:white;")
        self.label_15.setObjectName("label_15")
        self.label_16 = QtWidgets.QLabel(self.frame_4)
        self.label_16.setGeometry(QtCore.QRect(930, 0, 71, 41))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(14)
        font.setBold(False)
        font.setWeight(50)
        self.label_16.setFont(font)
        self.label_16.setStyleSheet("color:white;")
        self.label_16.setObjectName("label_16")
        self.label_17 = QtWidgets.QLabel(self.frame_4)
        self.label_17.setGeometry(QtCore.QRect(5, 8, 44, 23))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.label_17.setFont(font)
        self.label_17.setText("")
        self.label_17.setPixmap(QtGui.QPixmap(":/newPrefix/Vekaria Healthcare Logo/VHC Logo.png"))
        self.label_17.setScaledContents(True)
        self.label_17.setObjectName("label_17")
        self.wifiIcon = WifiStatusLabel(self.frame)
        self.wifiIcon.setGeometry(QtCore.QRect(868, 5, 41, 31))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.wifiIcon.setFont(font)
        self.wifiIcon.setPixmap(QtGui.QPixmap(":/vlogo/logo12.png"))
        self.wifiIcon.clicked.connect(self.open_wifi_page)
        self.label_18 = QtWidgets.QLabel(self.frame_4)
        self.label_18.setGeometry(QtCore.QRect(870, 4, 41, 31))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.label_18.setFont(font)
        self.label_18.setText("")
        self.label_18.setPixmap(QtGui.QPixmap("../vekariahealthCare/icons/logo12.png"))
        self.label_18.setScaledContents(True)
        self.label_18.setObjectName("label_18")

        

        #gender group
        self.gender_group = QtWidgets.QButtonGroup(self.frame_2)
        self.gender_group.addButton(self.male)
        self.gender_group.addButton(self.female)

        #alcohol group
        self.alcohol_group = QtWidgets.QButtonGroup(self.frame_2)
        self.alcohol_group.addButton(self.Alcho_yes)
        self.alcohol_group.addButton(self.Acho_no)

        #somke group
        self.smoke_group = QtWidgets.QButtonGroup(self.frame_2)
        self.smoke_group.addButton(self.Alcho_yes_2)
        self.smoke_group.addButton(self.Acho_no_2)

        #food habit group
        self.food_habit_group = QtWidgets.QButtonGroup(self.frame_2)
        self.food_habit_group.addButton(self.Alcho_yes_3)
        self.food_habit_group.addButton(self.Acho_no_3)

        #eye side group
        self.eye_side_group = QtWidgets.QButtonGroup(self.frame_2)
        self.eye_side_group.addButton(self.eye_R)
        self.eye_side_group.addButton(self.eye_L)
        self.pushButton_2.clicked.connect(self.save_patient_data)

        #diabetes group
        self.diabetes_group = QtWidgets.QButtonGroup(self.frame_2)      
        self.diabetes_group.addButton(self.Dia_yes)
        self.diabetes_group.addButton(self.Dia_no)

        text_edits = [
                self.textEdit, self.textEdit_2, self.textEdit_3,
                self.textEdit_4, self.textEdit_5, self.textEdit_6,
                self.Diabetes_text, self.Diabetes_text_2
        ]

        for text_edit in text_edits:
                text_edit.focusInEvent = lambda e, edit=text_edit: self.show_keyboard(e, edit)
                text_edit.focusOutEvent = lambda e, edit=text_edit: self.hide_keyboard(e, edit)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def show_keyboard(self, event, text_edit):
        """Show onboard keyboard when text edit gains focus"""
        subprocess.Popen(['onboard'])
        text_edit.original_focusInEvent(event) if hasattr(text_edit, 'original_focusInEvent') else None

    def hide_keyboard(self, event, text_edit):
        """Hide onboard keyboard when text edit loses focus"""
        subprocess.run(['killall', 'onboard'])
        text_edit.original_focusOutEvent(event) if hasattr(text_edit, 'original_focusOutEvent') else None

    def open_wifi_page(self):
        globaladc.buzzer_1()
        if self.wifi_window is None:
            self.wifi_window = WifiPage()
            self.wifi_window.show()
        else:
            self.wifi_window.activateWindow()

    def save_patient_data(self):
        globaladc.buzzer_1()
        try:
                
                patient_data = {
                "first_name": self.textEdit.toPlainText().strip(),
                "middle_name": self.textEdit_2.toPlainText().strip(),
                "surname": self.textEdit_3.toPlainText().strip(),
                "dob": self.textEdit_4.toPlainText().strip(),
                "aadhaar": self.textEdit_5.toPlainText().strip(),
                "mobile": self.textEdit_6.toPlainText().strip(),
                "gender": "Male" if self.male.isChecked() else "Female",
                "alcohol": "Yes" if self.Alcho_yes.isChecked() else "No",
                "smoking": "Yes" if self.Alcho_yes_2.isChecked() else "No",
                "food_habit": "Veg" if self.Alcho_yes_3.isChecked() else "NON-Veg",
                "bp": {
                        "has_bp": "Yes" if self.Bp_yes.isChecked() else "No",
                        "value": self.Diabetes_text_2.toPlainText().strip()
                },
                "diabetes": {
                        "has_diabetes": "Yes" if self.Dia_yes.isChecked() else "No",
                        "value": self.Diabetes_text.toPlainText().strip()
                },
                "eye_side": "R" if self.eye_R.isChecked() else "L",
                "is_sync":False,
                "handler_id":0
                }
                
                current_login_usr = os.path.join(os.path.dirname(os.path.abspath(__file__)), "patient_data", filename)
                with open(current_login_usr, 'r') as f:
                     user_data = json.load(f)

                patient_data['handler_id'] = user_data['user_id']
                        
                
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"patient_{patient_data['first_name']}.json"
                filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), "patient_data", filename)
                
                # Create directory if it doesn't exist
                os.makedirs(os.path.dirname(filepath), exist_ok=True)
                
                with open(filepath, 'w') as f:
                        json.dump(patient_data, f, indent=4)

                self.form.hide()
                # self.flickerCon_window = QtWidgets.QWidget()
                self.flickerCon = FlickerController()  
                self.flickerCon.show()
                
                QMessageBox.information(None, "Success", "Patient data saved successfully!")
                
        except Exception as e:
                QMessageBox.critical(None, "Error", f"Error saving patient data: {str(e)}")

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label_6.setText(_translate("Form", "1st Name"))
        self.textEdit.setPlaceholderText("first name")
        self.label_9.setText(_translate("Form", "Mid. Name"))
        self.textEdit_2.setPlaceholderText("Middle Name")
        self.textEdit_3.setPlaceholderText("Surname")
        self.label_10.setText(_translate("Form", "Surname"))
        self.label_7.setText(_translate("Form", "DOB"))
        self.textEdit_4.setPlaceholderText("Date of Birth")
        self.label_8.setText(_translate("Form", "Gender"))
        self.label_11.setText(_translate("Form", "Aadhaar"))
        self.textEdit_5.setPlaceholderText("Aadhaar No")
        self.label_12.setText(_translate("Form", "Mobile"))
        self.textEdit_6.setPlaceholderText("+91XXXXXXXXX")
        self.label_13.setText(_translate("Form", "Alchohol "))
        self.label_22.setText(_translate("Form", "Smoking"))
        self.label_23.setText(_translate("Form", "Diabetes"))
        self.Diabetes_text.setPlaceholderText("97")
        self.label_24.setText(_translate("Form", "Blood Pressure"))
        self.label_26.setText(_translate("Form", "Food Habit"))
        self.Diabetes_text_2.setPlaceholderText("80/120")
        self.pushButton_2.setText(_translate("Form", "SUBMIT"))
        self.Acho_no.setText(_translate("Form", "No"))
        self.Alcho_yes.setText(_translate("Form", "Yes"))
        self.male.setText(_translate("Form", "Male"))
        self.female.setText(_translate("Form", "Female"))
        self.Dia_yes.setText(_translate("Form", "Yes"))
        self.Dia_no.setText(_translate("Form", "No"))
        self.Bp_yes.setText(_translate("Form", "Yes"))
        self.Bp_no.setText(_translate("Form", "No"))
        self.Alcho_yes_2.setText(_translate("Form", "Yes"))
        self.Acho_no_2.setText(_translate("Form", "No"))
        self.Alcho_yes_3.setText(_translate("Form", "Veg"))
        self.Acho_no_3.setText(_translate("Form", "NON-Veg"))
        self.label_14.setText(_translate("Form", "Eye Side"))
        self.eye_R.setText(_translate("Form", "R"))
        self.eye_L.setText(_translate("Form", "L"))
        self.label_4.setText(_translate("Form", "Macular Densitometer                                                  Patient-Registration"))
        self.label_15.setText(_translate("Form", "Vekaria Healthcare"))
        self.label_16.setText(_translate("Form", "V1.0"))





if __name__ == '__main__':
    app = QApplication(sys.argv)
    loading_screen = LoadingScreen()
    loading_screen.show()
    sys.exit(app.exec_())
