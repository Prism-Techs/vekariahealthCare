# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\Patient-info.ui'
#
# Created by: PyQt5 UI code generator 5.15.11
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from  PyQt5.QtCore  import Qt

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1031, 586)
        Form.setStyleSheet("background-color:black;\n"
"border:none;")
        self.frame_2 = QtWidgets.QFrame(Form)
        self.frame_2.setGeometry(QtCore.QRect(20, 120, 981, 460))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.frame_2.setFont(font)
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
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.textEdit_2.setFont(font)
        self.textEdit_2.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.textEdit_2.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
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
        self.Diabetes_text.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.Diabetes_text.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(14)
        font.setBold(False)
        font.setWeight(50)
        self.Diabetes_text.setFont(font)
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
        self.Diabetes_text_2.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.Diabetes_text_2.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(16)
        font.setBold(False)
        font.setWeight(50)
        self.Diabetes_text_2.setFont(font)
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
        font.setFamily("Helvetica Neue")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setStyleSheet(" QPushButton {\n"
"                background-color: #1f2836;\n"
"                color: white;\n"
"                border: none;\n"
"                border-radius: 25px;\n"
"                padding: 10px;\n"
"                border:1px solid white;\n"
"            }\n"
"QPushButton::pressed{\n"
"    background-color:grey;\n"
"}\n"
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
        self.male.setChecked(True)
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
        self.Dia_no.setChecked(True)
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
        self.Bp_no.setChecked(True)
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
        self.Acho_no_2.setChecked(True)
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
        self.Acho_no_3.setChecked(True)
        self.Acho_no_3.setObjectName("Acho_no_3")
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
        self.wifiIcon_2 = QtWidgets.QLabel(self.frame_4)
        self.wifiIcon_2.setGeometry(QtCore.QRect(860, 0, 51, 41))
        self.wifiIcon_2.setStyleSheet("color:white;")
        self.wifiIcon_2.setText("")
        self.wifiIcon_2.setPixmap(QtGui.QPixmap(":/wifilogo/wifi.png"))
        self.wifiIcon_2.setScaledContents(True)
        self.wifiIcon_2.setObjectName("wifiIcon_2")
        self.label_18 = QtWidgets.QLabel(self.frame_4)
        self.label_18.setGeometry(QtCore.QRect(870, 4, 41, 31))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.label_18.setFont(font)
        self.label_18.setText("")
        self.label_18.setPixmap(QtGui.QPixmap(".\\../vekariahealthCare/icons/logo12.png"))
        self.label_18.setScaledContents(True)
        self.label_18.setObjectName("label_18")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label_6.setText(_translate("Form", "1st Name"))
        self.textEdit.setHtml(_translate("Form", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Helvetica Neue\'; font-size:14pt; font-weight:600; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Ved</p></body></html>"))
        self.label_9.setText(_translate("Form", "Mid. Name"))
        self.textEdit_2.setHtml(_translate("Form", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Helvetica Neue\'; font-size:14pt; font-weight:600; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">P</p></body></html>"))
        self.textEdit_3.setHtml(_translate("Form", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Helvetica Neue\'; font-size:14pt; font-weight:600; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Shah</p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.label_10.setText(_translate("Form", "Surname"))
        self.label_7.setText(_translate("Form", "DOB"))
        self.textEdit_4.setHtml(_translate("Form", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Helvetica Neue\'; font-size:14pt; font-weight:600; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">21/03/2004</p></body></html>"))
        self.label_8.setText(_translate("Form", "Gender"))
        self.label_11.setText(_translate("Form", "Aadhaar"))
        self.textEdit_5.setHtml(_translate("Form", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Helvetica Neue\'; font-size:14pt; font-weight:600; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">98584762689</p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.label_12.setText(_translate("Form", "Moblie"))
        self.textEdit_6.setHtml(_translate("Form", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Helvetica Neue\'; font-size:14pt; font-weight:600; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">8200160069</p></body></html>"))
        self.label_13.setText(_translate("Form", "Alchohol "))
        self.label_22.setText(_translate("Form", "Smoking"))
        self.label_23.setText(_translate("Form", "Diabetes"))
        self.Diabetes_text.setHtml(_translate("Form", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Helvetica Neue\'; font-size:16pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Arial\'; font-weight:600;\">97</span></p></body></html>"))
        self.label_24.setText(_translate("Form", "Blood Pressure"))
        self.label_26.setText(_translate("Form", "Food Habit"))
        self.Diabetes_text_2.setHtml(_translate("Form", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Helvetica Neue\'; font-size:16pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Arial\'; font-weight:600;\">80/120</span></p></body></html>"))
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
        self.label_4.setText(_translate("Form", "Macular Densitometer                                                  Patient-Registration"))
        self.label_15.setText(_translate("Form", "Vekaria Healthcare"))
        self.label_16.setText(_translate("Form", "V1.0"))


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
