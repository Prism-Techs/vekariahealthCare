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
from . import patient_page 


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
        self.patient_info = patient_page()  
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





if __name__ == '__main__':
    app = QApplication(sys.argv)
    loading_screen = LoadingScreen()
    loading_screen.show()
    sys.exit(app.exec_())
