import wifi_rc
import vekarialogo_rc
from PyQt5 import QtCore, QtGui, QtWidgets
import subprocess


class Ui_Form(object):

    def setupUi(self, Form):

        Form.setObjectName("Form")

        Form.resize(1024, 600)

        Form.setStyleSheet("background-color:#101826;")

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

        self.label_9.setPixmap(QtGui.QPixmap(



            ":/newPrefix/Vekaria Healthcare Logo/VHC Logo.png"))

        self.label_9.setScaledContents(True)

        self.label_9.setObjectName("label_9")

        # Changed WiFi icon to button

        self.wifiButtonicon = QtWidgets.QPushButton(self.frame)

        self.wifiButtonicon.setGeometry(QtCore.QRect(868, 5, 41, 31))

        self.label_10 = QtWidgets.QLabel(self.frame)
        self.label_10.setGeometry(QtCore.QRect(868, 5, 41, 31))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.label_10.setFont(font)
        self.label_10.setText("")
        self.label_10.setPixmap(QtGui.QPixmap("icons/logo12.png"))
        self.label_10.setScaledContents(True)
        self.label_10.setObjectName("label_10")

        # self.wifiButtonicon.setStyleSheet("""

        # QPushButton {

        #         background-color: transparent;

        #         border: none;

        # }

        # QPushButton:hover {

        #         background-color: rgba(255, 255, 255, 0.1);

        # }

        # QPushButton:pressed {

        #         background-color: rgba(255, 255, 255, 0.2);

        # }

        # """)

        self.wifiButtonicon.setCursor(



            QtGui.QCursor(QtCore.Qt.PointingHandCursor))

        self.wifiButtonicon.setObjectName("wifiButtonicon")

        # Connect the click signal to the scan function

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

        self.wifiComboBox = QtWidgets.QComboBox(self.frame_2)

        self.wifiComboBox.setGeometry(QtCore.QRect(112, 50, 400, 61))

        font = QtGui.QFont()

        font.setPointSize(18)

        self.wifiComboBox.setFont(font)

        self.wifiComboBox.setStyleSheet("""



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



                border-radius: 0px;



                padding: 10px;



                selection-background-color: #1f2836;



                color: white;



            }



        """)

        self.wifiComboBox.setObjectName("wifiComboBox")

        self.wifiComboBox.addItem("Select WiFi Network")

        self.lineEdit_2 = QtWidgets.QLineEdit(self.frame_2)

        self.lineEdit_2.setGeometry(QtCore.QRect(112, 140, 400, 61))

        font = QtGui.QFont()

        font.setPointSize(18)

        self.lineEdit_2.setFont(font)

        self.lineEdit_2.setStyleSheet(" QLineEdit {\n"



                                      "                background-color: #334155;\n"



                                      "                border: 1px solid white;\n"



                                      "                border-radius: 15px;\n"



                                      "                padding: 5px;\n"



                                      "                padding-left: 30px;\n"



                                      "                color: #94a3b8;\n"



                                      "            }")

        self.lineEdit_2.setObjectName("lineEdit_2")

        self.wificonnect = QtWidgets.QPushButton(self.frame_2)

        self.wificonnect.setGeometry(QtCore.QRect(333, 280, 181, 51))

        font = QtGui.QFont()

        font.setFamily("Helvetica Neue")

        font.setPointSize(16)

        font.setBold(True)

        font.setWeight(75)

        self.wificonnect.setFont(font)

        self.wificonnect.setStyleSheet(" QPushButton {\n"



                                       "                background-color: #1f2836;\n"



                                       "                color: white;\n"



                                       "                border: none;\n"



                                       "                border-radius: 25px;\n"



                                       "                padding: 10px;\n"



                                       "                border:1px solid white;\n"



                                       "            }\n"



                                       "")

        self.wificonnect.setObjectName("pushButton")

        self.lineEdit_2.setPlaceholderText("Password")

        self.rescanButton = QtWidgets.QPushButton(self.frame_2)

        self.rescanButton.setGeometry(QtCore.QRect(500, 70, 93, 28))

        self.rescanButton.setObjectName("rescanButton")

        self.rescanButton.setIcon(QtGui.QIcon("refreshbutton.png"))

        self.rescanButton.setStyleSheet("""



            QPushButton {



                background-color: transparent;



                border-radius: 20px;



            }



           



        """)

        self.wifiForget = QtWidgets.QPushButton(self.frame_2)

        self.wifiForget.setGeometry(QtCore.QRect(118, 280, 181, 51))

        font = QtGui.QFont()

        font.setFamily("Helvetica Neue")

        font.setPointSize(16)

        font.setBold(True)

        font.setWeight(75)

        self.wifiForget.setFont(font)

        self.wifiForget.setStyleSheet(" QPushButton {\n"



                                      "                background-color: #1f2836;\n"



                                      "                color: white;\n"



                                      "                border: none;\n"



                                      "                border-radius: 25px;\n"



                                      "                padding: 10px;\n"



                                      "                border:1px solid white;\n"



                                      "            }\n"



                                      "")

        self.wifiForget.setObjectName("wifiForget")

        self.wifiForget.clicked.connect(lambda: self.forget_wifi())

        self.label_5 = QtWidgets.QLabel(Form)

        self.label_5.setGeometry(QtCore.QRect(930, 577, 71, 20))

        font = QtGui.QFont()

        font.setFamily("Helvetica Neue")

        self.label_5.setFont(font)

        self.label_5.setStyleSheet("color:white;")

        self.label_5.setObjectName("label_5")

        self.label = QtWidgets.QLabel(Form)

        self.label.setGeometry(QtCore.QRect(956, 558, 55, 16))

        font = QtGui.QFont()

        font.setFamily("Helvetica Neue")

        self.label.setFont(font)

        self.label.setStyleSheet("color:white;")

        self.label.setObjectName("label")

        self.add_status_indicators()

        self.retranslateUi(Form)

        self.rescanButton.clicked.connect(self.initial_wifi_scan)

        self.wificonnect.clicked.connect(self.connect_wifi)

        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):

        _translate = QtCore.QCoreApplication.translate

        Form.setWindowTitle(_translate("Form", "Form"))

        self.label_2.setText(_translate("Form", "Vekaria Healthcare"))

        self.label_3.setText(_translate("Form", "V1.0"))

        self.label_4.setText(_translate("Form", "Macular Densitometer"))

        self.wificonnect.setText(_translate("Form", "CONNECT"))

        # self.rescanButton.setText(_translate("Form", "PushButton"))

        self.wifiForget.setText(_translate("Form", "FORGET"))

        self.label_5.setText(_translate("Form", "12-10-2024"))

        self.label.setText(_translate("Form", "19:53"))

        self.initial_wifi_scan()

    def connect_wifi(self):

        try:

            # Get selected network and password

            selected_network = self.wifiComboBox.currentText()

            if "Select WiFi Network" in selected_network or "No networks found" in selected_network:

                print("Please select a valid network")

                return

            # Extract network name from combo box text

            if " - Signal:" in selected_network:

                network_name = selected_network.split(" - Signal:")[0]

            else:

                network_name = selected_network

            password = self.lineEdit_2.text()

            if not password:

                print("Please enter password")

                return

            print(f"Connecting to {selected_network}...")

            # Create wpa_supplicant configuration

            wpa_config = f'''



    ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev



    update_config=1



    country=US







    network={{



    ssid="{selected_network}"



    psk="{password}"



    key_mgmt=WPA-PSK



    }}



    '''

            # Write configuration to temporary file

            try:

                with open('/etc/wpa_supplicant/wpa_supplicant.conf', 'w') as f:

                    f.write(wpa_config)

            except PermissionError:

                # If permission denied, use sudo

                with open('temp_wpa.conf', 'w') as f:

                    f.write(wpa_config)

            subprocess.run(['sudo', 'mv', 'temp_wpa.conf',



                           '/etc/wpa_supplicant/wpa_supplicant.conf'])

            # Restart wireless interface

            subprocess.run(['sudo', 'ifconfig', 'wlan0', 'down'])

            subprocess.run(['sudo', 'ifconfig', 'wlan0', 'up'])

            # Reconfigure wireless interface

            subprocess.run(['sudo', 'wpa_cli', '-i', 'wlan0', 'reconfigure'])

            # Wait for connection

            import time

            time.sleep(5)  # Give it some time to connect

            # Check connection status

            result = subprocess.check_output(



                ['iwconfig', 'wlan0'], universal_newlines=True)

            if selected_network in result:

                print(f"Successfully connected to {selected_network}")

                self.update_connection_status(



                    connected=True, ssid=network_name)

                self.show_message("Success", f"Connected to {network_name}")

            else:

                self.update_connection_status(connected=False)

                self.show_message("Error", "Failed to connect to network")

            # Get IP address

            ip_result = subprocess.check_output(



                ['ip', 'addr', 'show', 'wlan0'], universal_newlines=True)

            if 'inet ' in ip_result:

                ip = ip_result.split('inet ')[1].split('/')[0]

                print(f"IP address: {ip}")

                self.show_message("Success", f"Connected to {
                                  selected_network}")

            else:

                print("Failed to connect")

                self.show_message("Error", "Failed to connect to network")

        except Exception as e:

            print(f"Error connecting to network: {e}")

            self.show_message("Error", f"Error connecting to network: {e}")

    def show_message(self, title, message):
        """Show a popup message"""

        msg = QtWidgets.QMessageBox()

        msg.setWindowTitle(title)

        msg.setText(message)

        msg.exec_()

    def forget_wifi(self):
        """Remove saved WiFi network"""

        try:

            selected_network = self.wifiComboBox.currentText()

            if "Select WiFi Network" in selected_network or "No networks found" in selected_network:

                print("Please select a valid network")

                return

            # If network name includes signal strength, extract just the name

            if " - Signal:" in selected_network:

                selected_network = selected_network.split(" - Signal:")[0]

            # Remove network from wpa_supplicant.conf

            subprocess.run(



                ['sudo', 'wpa_cli', '-i', 'wlan0', 'remove_network', 'all'])

            subprocess.run(['sudo', 'wpa_cli', '-i', 'wlan0', 'save_config'])

            # After forgetting the network, update status

            self.update_connection_status(connected=False)

            print(f"Forgot network: {selected_network}")

            self.show_message("Success", f"Forgot network: {selected_network}")

            # Optionally rescan networks

            self.initial_wifi_scan()

        except Exception as e:

            print(f"Error forgetting network: {e}")

            self.show_message("Error", f"Error forgetting network: {e}")

    def add_status_indicators(self):

        try:

            # Get current connection info

            result = subprocess.check_output(



                ['iwconfig', 'wlan0'], universal_newlines=True)

            # Check if connected to a network

            if 'ESSID:' in result:

                current_network = result.split('ESSID:')[1].split('"')[1]

                if current_network:  # If there's an actual network name

                    # Update icon to connected state

                    self.label_10.setPixmap(QtGui.QPixmap("icons/logo12.png"))

                    # Get signal strength for the connected network

                    try:

                        signal_info = subprocess.check_output(



                            ['iwconfig', 'wlan0'], universal_newlines=True)

                        if 'Signal level=' in signal_info:

                            signal_strength = signal_info.split(



                                'Signal level=')[1].split(' ')[0]

                            network_display = f"{
                                current_network} - Signal: {signal_strength}dBm"

                        else:

                            network_display = current_network

                            self.wifiComboBox.clear()

                            self.wifiComboBox.addItem(network_display)

                    except:

                        # If can't get signal strength, just show network name

                        self.wifiComboBox.clear()

                        self.wifiComboBox.addItem(current_network)

                else:

                    # Not connected to any network

                    self.set_disconnected_state()

            else:

                # No WiFi info found

                self.set_disconnected_state()

        except Exception as e:

            print(f"Error checking WiFi status: {e}")

            self.set_disconnected_state()

    def set_disconnected_state(self):
        """Helper method to set disconnected state UI elements"""

        self.label_10.setPixmap(QtGui.QPixmap("no-wifi.png"))

        self.wifiComboBox.clear()

        self.wifiComboBox.addItem("Not Connected")

    def update_connection_status(self, connected=False, ssid=None):

        if connected and ssid:

            try:

                signal_info = subprocess.check_output(



                    ['iwconfig', 'wlan0'], universal_newlines=True)

                if 'Signal level=' in signal_info:

                    signal_strength = signal_info.split(



                        'Signal level=')[1].split(' ')[0]

                    network_display = f"{ssid} - Signal: {signal_strength}dBm"

                else:

                    network_display = ssid

                    self.wifiComboBox.clear()

                    self.wifiComboBox.addItem(network_display)

            except:

                # If can't get signal strength, just show network name

                self.wifiComboBox.clear()

                self.wifiComboBox.addItem(ssid)

                # Update icon to connected state

                self.label_10.setPixmap(QtGui.QPixmap("icons/logo12.png"))

        else:

            self.set_disconnected_state()

    def initial_wifi_scan(self):

        try:

            print("Scanning for wifi networks....")

            self.wifiComboBox.clear()

            self.wifiComboBox.addItem("Scanning...")

            QtWidgets.QApplication.processEvents()

            # First check if already connected to a network

            try:

                result = subprocess.check_output(



                    ['iwconfig', 'wlan0'], universal_newlines=True)

                if 'ESSID:' in result:

                    current_network = result.split('ESSID:')[1].split('"')[1]

                    if current_network:

                        self.update_connection_status(



                            connected=True, ssid=current_network)

                    else:

                        self.update_connection_status(connected=False)

            except:

                self.update_connection_status(connected=False)

            # Proceed with network scan

            try:

                subprocess.call(['sudo', 'iwlist', 'wlan0', 'scan'])

                scan_result = subprocess.check_output(



                    ['sudo', 'iwlist', 'wlan0', 'scan'], universal_newlines=True)

                networks = []

                current_network = {}

                for line in scan_result.split('\n'):

                    line = line.strip()

                    if 'Cell' in line:

                        if current_network and 'ssid' in current_network:

                            networks.append(current_network)

                        current_network = {}

                    elif 'ESSID:' in line:

                        essid = line.split('ESSID:"')[1].split('"')[0]

                        if essid:  # Only add non-empty SSIDs

                            current_network['ssid'] = essid

                    elif 'Quality=' in line:

                        signal = line.split('Signal level=')[1].split(' ')[0]

                        current_network['signal'] = signal

                if current_network and 'ssid' in current_network:

                    networks.append(current_network)

                # Get currently connected network if any

                connected_ssid = None

                try:

                    result = subprocess.check_output(



                        ['iwconfig', 'wlan0'], universal_newlines=True)

                    if 'ESSID:' in result:

                        connected_ssid = result.split(



                            'ESSID:')[1].split('"')[1]

                except:

                    pass

                self.wifiComboBox.clear()

                if not networks:

                    if connected_ssid:

                        self.update_connection_status(



                            connected=True, ssid=connected_ssid)

                    else:

                        self.wifiComboBox.addItem("No networks found")

                else:

                    if not connected_ssid:

                        self.wifiComboBox.addItem("Select WiFi Network")

                    # Sort networks by signal strength

                    networks.sort(key=lambda x: int(



                        x.get('signal', '0')), reverse=True)

                    # Add networks to combo box

                    for network in networks:

                        display_text = f"{
                            network['ssid']} - Signal: {network['signal']}dBm"

                        self.wifiComboBox.addItem(display_text)

            except subprocess.CalledProcessError as e:

                print(f"Error scanning networks: {e}")

                if connected_ssid:

                    self.update_connection_status(



                        connected=True, ssid=connected_ssid)

                else:

                    self.wifiComboBox.clear()

                    self.wifiComboBox.addItem("Error scanning networks")

                    self.update_connection_status(connected=False)

        except Exception as e:

            print(f"Error in initial scan: {e}")

            self.wifiComboBox.clear()

            self.wifiComboBox.addItem("Error scanning networks")

            self.update_connection_status(connected=False)


if __name__ == "__main__":

    import sys

    app = QtWidgets.QApplication(sys.argv)

    Form = QtWidgets.QWidget()

    ui = Ui_Form()

    ui.setupUi(Form)

    Form.show()

    sys.exit(app.exec_())


# this is
