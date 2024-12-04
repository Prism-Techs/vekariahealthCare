import sys
from PyQt5 import QtCore, QtGui, QtWidgets
import time
import RPi.GPIO as GPIO
from threading import Thread, Event

class PeriodicThread(Thread):
    def __init__(self, interval, callback):
        super().__init__()
        self.interval = interval
        self.callback = callback
        self.stop_event = Event()
        self.is_started = False
        
    def run(self):
        self.is_started = True
        while not self.stop_event.is_set():
            self.callback()
            time.sleep(self.interval)
            
    def stop(self):
        self.stop_event.set()
        self.is_started = False

class CffFovea(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setupUi()
        self.initializeVariables()
        self.setupConnections()
        
    def initializeVariables(self):
        self.switch = 20  # GPIO pin for patient switch
        self.response_count = 0
        self.skip_event = True
        self.thread_created = False
        self.freq_val_start = 34.5
        self.freq_val = self.freq_val_start
        self.min_apr = 0
        self.max_apr = 0
        self.response_array = [0] * 5
        self.interval = 0.1  # Adjust as needed
        self.worker_thread = None
        
    def setupConnections(self):
        self.pushButton.clicked.connect(self.onMachineReady)
        self.pushButton_2.clicked.connect(self.onFlickerStart)
        self.pushButton_3.clicked.connect(self.onFlickerVisible)
        self.Home.clicked.connect(self.onHome)
        self.Next.clicked.connect(self.onNext)
        
    def setupUi(self):
        # Adding all the UI elements from the second file's setupUi method
        self.setObjectName("Form")
        self.resize(1024, 612)
        self.setStyleSheet("background-color:black;\ncolor:white;")
        
        # Create main frame
        self.frame = QtWidgets.QFrame(self)
        self.frame.setGeometry(QtCore.QRect(0, 0, 1031, 41))
        self.frame.setStyleSheet("background-color:#1f2836;\ncolor:white")
        
        # Add title labels
        self.label_2 = QtWidgets.QLabel(self.frame)
        self.label_2.setGeometry(QtCore.QRect(60, 0, 281, 41))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(16)
        font.setBold(True)
        self.label_2.setFont(font)
        self.label_2.setText("Vekaria Healthcare")
        
        # Add content frame
        self.frame_5 = QtWidgets.QFrame(self)
        self.frame_5.setGeometry(QtCore.QRect(280, 110, 711, 441))
        self.frame_5.setStyleSheet("""
        QFrame{
            background-color:#1f2836;
            border-radius:30px;
        };
        color:white;
        """)
        
        # Add main display
        self.data1 = QtWidgets.QLabel(self.frame_5)
        self.data1.setGeometry(QtCore.QRect(200, 60, 211, 50))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(28)
        self.data1.setFont(font)
        self.data1.setStyleSheet("color: white;")
        self.data1.setAlignment(QtCore.Qt.AlignCenter)
        self.data1.setText("34.5")
        
        # Add trial list
        self.final_data = QtWidgets.QTextEdit(self.frame_5)
        self.final_data.setGeometry(QtCore.QRect(580, 100, 111, 281))
        self.final_data.setStyleSheet("""
        QTextEdit {
            background-color: black;
            border: 2px solid Black;
            color: white;
            border-radius:0px;
        }
        """)
        
        # Add control buttons
        button_style = """
        QPushButton {
            border-radius: 5px;
            font-weight: bold;
            font-size: 14px;
            padding: 5px;
            font-family: Arial;
            color: white;
            background-color: #1a472a;
            border: 2px solid white;
        }
        QPushButton:hover {
            background-color: #2a5a3a;
        }
        """
        
        self.pushButton = QtWidgets.QPushButton("Machine Ready", self.frame_5)
        self.pushButton.setGeometry(QtCore.QRect(50, 230, 134, 41))
        self.pushButton.setStyleSheet(button_style)
        
        self.pushButton_2 = QtWidgets.QPushButton("Flicker Start", self.frame_5)
        self.pushButton_2.setGeometry(QtCore.QRect(50, 290, 134, 41))
        self.pushButton_2.setStyleSheet(button_style)
        
        self.pushButton_3 = QtWidgets.QPushButton("Flicker Visible", self.frame_5)
        self.pushButton_3.setGeometry(QtCore.QRect(50, 350, 134, 41))
        self.pushButton_3.setStyleSheet(button_style)
        
        # Navigation buttons
        nav_button_style = """
        QPushButton {
            background-color: transparent;
            color: white;
            border: 1px solid white;
            padding: 10px 20px;
            font-size: 24px;
            border-radius: 1px;
            font-weight: bold;
        }
        """
        
        self.Home = QtWidgets.QPushButton("Home", self.frame_5)
        self.Home.setGeometry(QtCore.QRect(300, 380, 121, 51))
        self.Home.setStyleSheet(nav_button_style)
        
        self.Next = QtWidgets.QPushButton("Next", self.frame_5)
        self.Next.setGeometry(QtCore.QRect(440, 380, 121, 51))
        self.Next.setStyleSheet(nav_button_style)

    def handleUserButton(self):
        if self.skip_event:
            self.startNewTrial()
        else:
            self.endTrial()
            
    def startNewTrial(self):
        self.skip_event = False
        if self.response_count == 0:
            self.freq_val = self.freq_val_start
        else:
            self.freq_val = self.min_apr + 6.5
            
        self.thread_created = True
        self.startFlicker()
        
    def endTrial(self):
        self.skip_event = True
        self.response_array[self.response_count] = self.freq_val
        self.updateTrialDisplay()
        self.response_count += 1
        
        if self.response_count == 5:
            self.finalizeTest()
            
    def updateTrialDisplay(self):
        current_text = self.final_data.toPlainText()
        new_text = f"{self.freq_val:.1f}\n{current_text}"
        self.final_data.setText(new_text)
        
    def finalizeTest(self):
        self.stopThread()
        self.calculateResults()
        self.showResults()
        
    def periodic_event(self):
        if not self.skip_event:
            self.freq_val = round(self.freq_val - 0.5, 1)
            self.data1.setText(f"{self.freq_val:.1f}")
            if self.freq_val < 5:
                self.skip_event = True
                self.thread_created = False
                self.freq_val = self.freq_val_start
                
    def setupGPIO(self):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.switch, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(self.switch, GPIO.RISING, callback=lambda x: self.handleUserButton())
        
    def startThread(self):
        if not self.worker_thread or not self.worker_thread.is_started:
            self.worker_thread = PeriodicThread(self.interval, self.periodic_event)
            self.worker_thread.start()
            
    def stopThread(self):
        if self.worker_thread and self.worker_thread.is_started:
            self.worker_thread.stop()
            self.worker_thread.join()
            
    def onMachineReady(self):
        self.setupGPIO()
        self.pushButton.setEnabled(False)
        self.pushButton_2.setEnabled(True)
        
    def onFlickerStart(self):
        self.startThread()
        self.pushButton_2.setEnabled(False)
        self.pushButton_3.setEnabled(True)
        
    def onFlickerVisible(self):
        # Handle flicker visible button press
        pass
        
    def onHome(self):
        self.stopThread()
        # Implement navigation to home screen
        
    def onNext(self):
        self.stopThread()
        # Implement navigation to next screen

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = CffFovea()
    window.show()
    sys.exit(app.exec_())