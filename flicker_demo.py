

from PyQt5 import QtCore, QtGui, QtWidgets


from PyQt5 import QtCore, QtGui, QtWidgets
import threading
import time
from globalvar import globaladc
from wifi_update import WifiStatusLabel
from wifi_final import WifiPage


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        self.wifi_window = None  # Initialize as None

        Form.resize(1024, 600)
        Form.setStyleSheet("background-color:#000000;")
        self.frame_4 = QtWidgets.QFrame(Form)
        self.frame_4.setGeometry(QtCore.QRect(0, 0, 1024, 40))
        self.frame_4.setStyleSheet("background-color:#1f2836;")
        self.frame_4.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_4.setObjectName("frame_4")
        self.label_6 = QtWidgets.QLabel(self.frame_4)
        self.label_6.setGeometry(QtCore.QRect(60, 0, 281, 41))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.label_6.setFont(font)
        self.label_6.setStyleSheet("color:white;")
        self.label_6.setObjectName("label_6")
        self.label_8 = QtWidgets.QLabel(self.frame_4)
        self.label_8.setGeometry(QtCore.QRect(930, 0, 71, 41))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(14)
        font.setBold(False)
        font.setWeight(50)
        self.label_8.setFont(font)
        self.label_8.setStyleSheet("color:white;")
        self.label_8.setObjectName("label_8")
        self.label_11 = QtWidgets.QLabel(self.frame_4)
        self.label_11.setGeometry(QtCore.QRect(5, 8, 44, 23))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.label_11.setFont(font)
        self.label_11.setText("")
        self.label_11.setPixmap(QtGui.QPixmap(":/newPrefix/Vekaria Healthcare Logo/VHC Logo.png"))
        self.label_11.setScaledContents(True)
        self.label_11.setObjectName("label_11")
        self.label_12 = QtWidgets.QLabel(self.frame_4)
        self.label_12.setGeometry(QtCore.QRect(870, 4, 41, 31))
        # Update the pixmap path to use the resource system
        self.label_12.setPixmap(QtGui.QPixmap(":/vlogo/logo12.png"))
        self.label_12.setScaledContents(True)
        self.label_12.setObjectName("label_12")
        self.frame_5 = QtWidgets.QFrame(Form)
        self.frame_5.setGeometry(QtCore.QRect(280, 100, 691, 441))
        self.frame_5.setStyleSheet("QFrame{\n"
"background-color:#1f2836;\n"
"border-radius:30px;\n"
"\n"
"\n"
"};\n"
"color:white;")
        self.frame_5.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_5.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_5.setObjectName("frame_5")
        self.pushButton_2 = QtWidgets.QPushButton(self.frame_5)
        self.pushButton_2.setGeometry(QtCore.QRect(370, 350, 160, 51))
        font = QtGui.QFont()
        font.setFamily("Helvetica Rounded")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setStyleSheet(" QPushButton {\n"
"                background-color: black;\n"
"                color: white;\n"
"                border: none;\n"
"                border-radius: 15px;\n"
"                padding: 10px;\n"
"                border:2px solid white;\n"
"            }\n"
"")
        self.pushButton_2.setObjectName("pushButton_2")
        self.frame = QtWidgets.QFrame(self.frame_5)
        self.frame.setGeometry(QtCore.QRect(50, 120, 191, 221))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.upButton = QtWidgets.QPushButton(self.frame)
        self.upButton.setGeometry(QtCore.QRect(70, 10, 60, 60))
        self.upButton.setMinimumSize(QtCore.QSize(60, 60))
        self.upButton.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setPointSize(-1)
        font.setBold(True)
        font.setWeight(75)
        self.upButton.setFont(font)
        self.upButton.setStyleSheet(" QPushButton {\n"
"                background-color: black;\n"
"                color: white;\n"
"                border: 1px solid white;\n"
"                border-radius: 30px;\n"
"                font-size: 40px;\n"
"                font-weight: bold;\n"
"            }\n"
"            QPushButton:hover {\n"
"                background-color: #177bad;\n"
"            }\n"
"            QPushButton:pressed {\n"
"                background-color: #177bad;\n"
"            }\n"
"  QPushButton {\n"
"                text-align: center;\n"
"                justify-content:center;\n"
"                padding-bottom:9px;\n"
"            }")
        self.upButton.setObjectName("upButton")
        self.numberLabel = QtWidgets.QLabel(self.frame)
        self.numberLabel.setGeometry(QtCore.QRect(60, 86, 80, 60))
        self.numberLabel.setMinimumSize(QtCore.QSize(80, 60))
        self.numberLabel.setMaximumSize(QtCore.QSize(60, 40))
        font = QtGui.QFont()
        font.setFamily("Helvetica Rounded")
        font.setPointSize(28)
        font.setBold(True)
        font.setWeight(75)
        self.numberLabel.setFont(font)
        self.numberLabel.setStyleSheet("background-color: black;\n"
"color: white;\n"
"padding: 5px;\n"
"border:2px solid white;\n"
"border-radius: 5px;")
        self.numberLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.numberLabel.setObjectName("numberLabel")
        self.upButton_2 = QtWidgets.QPushButton(self.frame)
        self.upButton_2.setGeometry(QtCore.QRect(70, 160, 60, 60))
        self.upButton_2.setMinimumSize(QtCore.QSize(60, 60))
        self.upButton_2.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setPointSize(-1)
        self.upButton_2.setFont(font)
        self.upButton_2.setStyleSheet(" QPushButton {\n"
"                background-color: black;\n"
"                color: white;\n"
"                border: 1px solid white;\n"
"                border-radius: 30px;\n"
"                font-size: 50px;\n"
"            }\n"
"            QPushButton:hover {\n"
"                background-color: #177bad;\n"
"            }\n"
"            QPushButton:pressed {\n"
"                background-color: #177bad;\n"
"            }\n"
"  QPushButton {\n"
"                text-align: center;\n"
"                justify-content:center;\n"
"                padding-bottom:9px;\n"
"            }")
        self.upButton_2.setObjectName("upButton_2")
        self.label = QtWidgets.QLabel(self.frame_5)
        self.label.setGeometry(QtCore.QRect(100, 40, 131, 61))
        font = QtGui.QFont()
        font.setFamily("Helvetica Rounded")
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label.setStyleSheet("QLabel{\n"
"border:none;\n"
"color:white;\n"
"}")
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.pushButton_3 = QtWidgets.QPushButton(self.frame_5)
        self.pushButton_3.setGeometry(QtCore.QRect(350, 90, 240, 51))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_3.setFont(font)
        self.pushButton_3.setStyleSheet(" QPushButton {\n"
"                background-color: black;\n"
"                color: white;\n"
"                border: none;\n"
"                border-radius: 15px;\n"
"                padding: 10px;\n"
"                border:2px solid white;\n"
"            }\n"
"")
        self.pushButton_3.setObjectName("pushButton_3")
        self.label_2 = QtWidgets.QLabel(self.frame_5)
        self.label_2.setGeometry(QtCore.QRect(350, 170, 240, 50))
        font = QtGui.QFont()
        font.setFamily("Helvetica Rounded")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_2.setStyleSheet("QLabel{\n"
"border:none;\n"
"color:white;\n"
"}")
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.label_4 = QtWidgets.QLabel(Form)
        self.label_4.setGeometry(QtCore.QRect(10, 40, 1024, 51))
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
        self.pushButton_4 = QtWidgets.QPushButton(Form)
        self.pushButton_4.setGeometry(QtCore.QRect(10, 150, 240, 40))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(16)
        font.setBold(False)
        font.setWeight(50)
        self.pushButton_4.setFont(font)
        self.pushButton_4.setStyleSheet(" QPushButton {\n"
"                background-color: white;\n"
"                color: black;\n"
"                border: none;\n"
"                border:2px solid white;\n"
"            }\n"
"")
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_5 = QtWidgets.QPushButton(Form)
        self.pushButton_5.setGeometry(QtCore.QRect(10, 210, 240, 40))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(16)
        font.setBold(False)
        font.setWeight(50)
        self.pushButton_5.setFont(font)
        self.pushButton_5.setStyleSheet(" QPushButton {\n"
"                background-color: black;\n"
"                color: white;\n"
"                border: none;\n"
"                border:2px solid white;\n"
"            }\n"
"")
        self.pushButton_5.setObjectName("pushButton_5")
        self.pushButton_6 = QtWidgets.QPushButton(Form)
        self.pushButton_6.setGeometry(QtCore.QRect(10, 270, 240, 40))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(16)
        font.setBold(False)
        font.setWeight(50)
        self.pushButton_6.setFont(font)
        self.pushButton_6.setStyleSheet(" QPushButton {\n"
"                background-color: black;\n"
"                color: white;\n"
"                border: none;\n"
"                border:2px solid white;\n"
"            }\n"
"")
        self.pushButton_6.setObjectName("pushButton_6")
        self.pushButton_7 = QtWidgets.QPushButton(Form)
        self.pushButton_7.setGeometry(QtCore.QRect(10, 330, 240, 40))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(16)
        font.setBold(False)
        font.setWeight(50)
        self.pushButton_7.setFont(font)
        self.pushButton_7.setStyleSheet(" QPushButton {\n"
"                background-color: black;\n"
"                color: white;\n"
"                border: none;\n"
"                border:2px solid white;\n"
"            }\n"
"")
        self.pushButton_7.setObjectName("pushButton_7")
        self.pushButton_8 = QtWidgets.QPushButton(Form)
        self.pushButton_8.setGeometry(QtCore.QRect(10, 390, 240, 40))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(16)
        font.setBold(False)
        font.setWeight(50)
        self.pushButton_8.setFont(font)
        self.pushButton_8.setStyleSheet(" QPushButton {\n"
"                background-color: black;\n"
"                color: white;\n"
"                border: none;\n"
"                border:2px solid white;\n"
"            }\n"
"")
        self.pushButton_8.setObjectName("pushButton_8")
        self.pushButton_9 = QtWidgets.QPushButton(Form)
        self.pushButton_9.setGeometry(QtCore.QRect(10, 450, 240, 40))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(16)
        font.setBold(False)
        font.setWeight(50)
        self.pushButton_9.setFont(font)
        self.pushButton_9.setStyleSheet(" QPushButton {\n"
"                background-color: black;\n"
"                color: white;\n"
"                border: none;\n"
"                border:2px solid white;\n"
"            }\n"
"")
        self.pushButton_9.setObjectName("pushButton_9")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)


    def open_wifi_page(self):
        if self.wifi_window is None:
            self.wifi_window = WifiPage()
            self.wifi_window.show()
        else:
            self.wifi_window.activateWindow()

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label_6.setText(_translate("Form", "Vekaria Healthcare"))
        self.label_8.setText(_translate("Form", "V1.0"))
        self.pushButton_2.setText(_translate("Form", "HOME"))
        self.upButton.setText(_translate("Form", "+"))
        self.numberLabel.setText(_translate("Form", "0"))
        self.upButton_2.setText(_translate("Form", "-"))
        self.label.setText(_translate("Form", "Depth"))
        self.pushButton_3.setText(_translate("Form", "Flicker off"))
        self.label_2.setText(_translate("Form", "Press Button\n"
" To ON/OFF"))
        self.label_4.setText(_translate("Form", "Flicker Demo"))
        self.pushButton_4.setText(_translate("Form", "Flicker Demo"))
        self.pushButton_5.setText(_translate("Form", "CFF Fovea"))
        self.pushButton_6.setText(_translate("Form", "BRK Fovea"))
        self.pushButton_7.setText(_translate("Form", "CFF Para-Fovea"))
        self.pushButton_8.setText(_translate("Form", "BRK Para-Fovea"))
        self.pushButton_9.setText(_translate("Form", "Test Result"))



import vekarialogo_rc
import wifi_rc


