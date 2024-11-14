# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\wifi.ui'
#
# Created by: PyQt5 UI code generator 5.15.11
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5.QtGui import QPainter, QPen, QColor
from PyQt5.QtCore import Qt, QTimer, QDateTime
from PyQt5.QtWidgets import QMessageBox
from PyQt5 import QtCore, QtGui, QtWidgets
import subprocess
import json
import os
import threading
import time
import re


class WifiStatusLabel(QtWidgets.QLabel):
    """Custom QLabel to draw red cross when disconnected"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.is_connected = False


    def paintEvent(self, event):
        super().paintEvent(event)
        if not self.is_connected:
            painter = QPainter(self)
            pen = QPen(QColor('red'))
            pen.setWidth(3)
            painter.setPen(pen)
            painter.drawLine(0, self.height(), self.width(), 0)

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1024, 600)
        Form.setStyleSheet("background-color:black;")
        self.frame = QtWidgets.QFrame(Form)
        self.frame.setGeometry(QtCore.QRect(0, 0, 1024, 40))
        self.frame.setStyleSheet("background-color:#1f2836;")
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
        self.wifiIcon.setText("")
        self.wifiIcon.setPixmap(QtGui.QPixmap(":/vlogo/logo12.png"))
        self.wifiIcon.setScaledContents(True)
        self.wifiIcon.setObjectName("wifiIcon")
        self.label_4 = QtWidgets.QLabel(Form)
        self.label_4.setGeometry(QtCore.QRect(10, 40, 1024, 40))
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
        self.frame_2.setGeometry(QtCore.QRect(210, 110, 624, 391))
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
        self.wifi_name = QtWidgets.QComboBox(self.frame_2)
        self.wifi_name.setGeometry(QtCore.QRect(112, 50, 400, 61))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.wifi_name.setFont(font)
        self.wifi_name.setStyleSheet("""
        QComboBox {
                background-color: #334155;
                border: 1px solid white;
                border-radius: 15px;
                padding: 5px;
                padding-left: 30px;
                color: #94a3b8;
        }
        QComboBox::drop-down {
                border: none;
                width: 50px;
        }
        QComboBox::down-arrow {
                image: url(dropdown-arrow.png);
                width: 20px;
                height: 20px;
        }
        QComboBox QAbstractItemView {
                background-color: #334155;
                border: 1px solid white;
                selection-background-color: #1f2836;
                color: white;
                padding: 5px;
        }
        """)
        self.wifi_name.setObjectName("wifi_name")
        self.wifi_name.setPlaceholderText("Select WiFi Network")
        self.password = QtWidgets.QLineEdit(self.frame_2)
        self.password.setGeometry(QtCore.QRect(112, 140, 400, 61))
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
        self.connect = QtWidgets.QPushButton(self.frame_2)
        self.connect.setGeometry(QtCore.QRect(333, 280, 181, 51))
        font = QtGui.QFont()
        font.setPointSize(-1)
        font.setBold(True)
        font.setWeight(75)
        self.connect.setFont(font)
        self.connect.setStyleSheet("\n"
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
        self.connect.setObjectName("connect")
        self.refresh = QtWidgets.QPushButton(self.frame_2)
        self.refresh.setGeometry(QtCore.QRect(520, 70, 31, 21))
        self.refresh.setStyleSheet("background:transparent;")
        self.refresh.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/vlogo/refreshbutton.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.refresh.setIcon(icon)
        self.refresh.setAutoDefault(True)
        self.refresh.setObjectName("refresh")
        self.forget = QtWidgets.QPushButton(self.frame_2)
        self.forget.setGeometry(QtCore.QRect(118, 280, 181, 51))
        font = QtGui.QFont()
        font.setPointSize(-1)
        font.setBold(True)
        font.setWeight(75)
        self.forget.setFont(font)
        self.forget.setStyleSheet("\n"
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
        self.forget.setObjectName("forget")
        self.date = QtWidgets.QLabel(Form)
        self.date.setGeometry(QtCore.QRect(930, 577, 71, 20))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        self.date.setFont(font)
        self.date.setStyleSheet("color:white;")
        self.date.setObjectName("date")
        self.time = QtWidgets.QLabel(Form)
        self.time.setGeometry(QtCore.QRect(956, 558, 55, 16))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        self.time.setFont(font)
        self.time.setStyleSheet("color:white;")
        self.time.setObjectName("time")


                # Password toggle button
        self.togglePassword = QtWidgets.QPushButton(self.frame_2)
        self.togglePassword.setGeometry(QtCore.QRect(520, 155, 30, 30))
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
        self.wifi_status_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "wifi_status.json")
        
        # Connect buttons to functions
        self.connect.clicked.connect(self.connect_wifi)
        self.forget.clicked.connect(self.forget_wifi)
        self.refresh.clicked.connect(self.scan_wifi_networks)
        
        # Setup timer for wifi status check
        self.status_timer = QTimer()
        self.status_timer.timeout.connect(self.check_wifi_status)
        self.status_timer.start(5000)  # Check every 5 seconds
        
        # Initial checks
        self.check_wifi_status()
        self.scan_wifi_networks()

        self.update_datetime() 
        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def update_datetime(self):
        """Update the date and time labels with current values"""
        current_datetime = QDateTime.currentDateTime()
        self.time.setText(current_datetime.toString('HH:mm'))
        self.date.setText(current_datetime.toString('dd-MM-yyyy'))


    def toggle_password_visibility(self):
        """Toggle password field visibility"""
        self.password_visible = not self.password_visible
        if self.password_visible:
            self.password.setEchoMode(QtWidgets.QLineEdit.Normal)
            self.togglePassword.setText("🔒")
        else:
            self.password.setEchoMode(QtWidgets.QLineEdit.Password)
            self.togglePassword.setText("👁")

    def update_wifi_status_json(self, is_connected):
        """Update WiFi status in JSON file"""
        try:
            status = {
                "wifi_connected": is_connected,
                "last_updated": QDateTime.currentDateTime().toString("yyyy-MM-dd HH:mm:ss"),
                "network_name": self.get_current_wifi() if is_connected else None
            }
            
            with open(self.wifi_status_file, 'w') as f:
                json.dump(status, f, indent=4)
                
        except Exception as e:
            print(f"Error updating WiFi status JSON: {e}")

    def check_wifi_status(self):
        """Check current WiFi status and update UI and JSON"""
        try:
            current_wifi = self.get_current_wifi()
            is_connected = bool(current_wifi)
            
            # Update icon and connection status
            self.wifiIcon.is_connected = is_connected
            if is_connected:
                self.wifiIcon.setPixmap(QtGui.QPixmap(":/vlogo/logo12.png"))
            else:
                self.wifiIcon.setPixmap(QtGui.QPixmap(":/vlogo/logo12.png"))
            
            # Force repaint to update red cross
            self.wifiIcon.repaint()
            
            # Update JSON status
            self.update_wifi_status_json(is_connected)
            
        except Exception as e:
            print(f"Error checking WiFi status: {e}")
            self.wifiIcon.is_connected = False
            self.wifiIcon.repaint()
            self.update_wifi_status_json(False)

    def scan_wifi_networks(self):
        """Scan available WiFi networks"""
        try:
            result = subprocess.run(['iwlist', 'wlan0', 'scan'], 
                                  capture_output=True, text=True)
            networks = []
            
            for line in result.stdout.split('\n'):
                if 'ESSID' in line:
                    essid = line.split('ESSID:"')[1].split('"')[0]
                    if essid:
                        networks.append(essid)
            
            self.wifi_name.clear()
            self.wifi_name.setText("")  # Clear current text
            if networks:
                self.wifi_name.setText(networks[0])  # Set first network as default
                
        except Exception as e:
            self.show_message("Error", f"Failed to scan networks: {str(e)}")

    def connect_wifi(self):
        """Connect to selected WiFi network"""
        ssid = self.wifi_name.text().strip()
        password = self.password.text().strip()
        
        if not ssid:
            self.show_message("Error", "Please enter a network name")
            return
            
        try:
            wpa_config = f'''
            network={{
                ssid="{ssid}"
                psk="{password}"
                key_mgmt=WPA-PSK
            }}
            '''
            
            with open('/tmp/wpa_supplicant.conf', 'w') as f:
                f.write(wpa_config)
            
            subprocess.run(['sudo', 'cp', '/tmp/wpa_supplicant.conf', 
                          '/etc/wpa_supplicant/wpa_supplicant.conf'])
            
            subprocess.run(['sudo', 'ifdown', 'wlan0'])
            subprocess.run(['sudo', 'ifup', 'wlan0'])
            
            def check_connection():
                for _ in range(20):  # Try for 20 seconds
                    if self.is_connected(ssid):
                        self.check_wifi_status()
                        self.show_message("Success", f"Connected to {ssid}")
                        return
                    time.sleep(1)
                self.check_wifi_status()
                self.show_message("Error", "Failed to connect to network")
            
            threading.Thread(target=check_connection).start()
            
        except Exception as e:
            self.check_wifi_status()
            self.show_message("Error", f"Failed to connect: {str(e)}")

    def forget_wifi(self):
        """Forget selected WiFi network"""
        ssid = self.wifi_name.text().strip()
        
        if not ssid:
            self.show_message("Error", "Please select a network to forget")
            return
            
        try:
            with open('/etc/wpa_supplicant/wpa_supplicant.conf', 'r') as f:
                config = f.read()
            
            new_config = re.sub(
                f'network={{\n\s*ssid="{ssid}"[^}}]*}}',
                '',
                config,
                flags=re.MULTILINE
            )
            
            with open('/tmp/wpa_supplicant.conf', 'w') as f:
                f.write(new_config)
                
            subprocess.run(['sudo', 'cp', '/tmp/wpa_supplicant.conf', 
                          '/etc/wpa_supplicant/wpa_supplicant.conf'])
            
            self.check_wifi_status()
            self.show_message("Success", f"Forgotten network: {ssid}")
            self.scan_wifi_networks()
            
        except Exception as e:
            self.show_message("Error", f"Failed to forget network: {str(e)}")

    def get_current_wifi(self):
        """Get current connected WiFi name"""
        try:
            result = subprocess.run(['iwgetid', '-r'], capture_output=True, text=True)
            return result.stdout.strip()
        except:
            return None

    def is_connected(self, ssid):
        """Check if connected to specific network"""
        current = self.get_current_wifi()
        return current == ssid

    def show_message(self, title, message):
        """Show styled message box"""
        msg = QMessageBox()
        msg.setStyleSheet("""
            QMessageBox {
                background-color: #1f2836;
            }
            QMessageBox QLabel {
                color: white;
                font-weight: bold;
                font-size: 16px;
            }
            QPushButton {
                color: white;
                background-color: transparent;
                border: 1px solid white;
                padding: 5px;
            }
        """)
        msg.information(None, title, message)


    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label_2.setText(_translate("Form", "Vekaria Healthcare"))
        self.label_3.setText(_translate("Form", "V1.0"))
        self.label_4.setText(_translate("Form", "Macular Densitometer"))
        # self.wifi_name.setPlaceholderText(_translate("Form", "Wi-Fi Name"))
        self.password.setPlaceholderText(_translate("Form", "Password"))
        self.connect.setText(_translate("Form", "CONNECT"))
        self.forget.setText(_translate("Form", "FORGET"))
        # self.date.setText(_translate("Form", "12-10-2024"))
        # self.time.setText(_translate("Form", "19:53"))
import vekarialogo_rc
import wifi_rc


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
