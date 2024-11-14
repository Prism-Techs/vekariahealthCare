from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import QPropertyAnimation, QEasingCurve, QTimer

class FlickerButton(QtWidgets.QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setupButton()
        self.is_on = False
        
    def setupButton(self):
        # Base style
        self.setStyleSheet("""
            QPushButton {
                background-color: #000000;
                color: #ffffff;
                border: 2px solid #333333;
                border-radius: 10px;
                padding: 10px 20px;
                font-size: 16px;
                font-weight: bold;
                min-width: 120px;
                min-height: 40px;
            }
            QPushButton:hover {
                background-color: #1a1a1a;
                border-color: #444444;
            }
        """)
        
        # Setup animations
        self.setupAnimations()
        
        # Setup flicker timer
        self.flicker_timer = QTimer(self)
        self.flicker_timer.timeout.connect(self.toggleFlicker)
        
        # Connect click event
        self.clicked.connect(self.handleClick)
        
    def setupAnimations(self):
        # Press down animation
        self.press_anim = QPropertyAnimation(self, b"geometry")
        self.press_anim.setEasingCurve(QEasingCurve.OutBounce)
        self.press_anim.setDuration(300)
        
        # Pop up animation
        self.release_anim = QPropertyAnimation(self, b"geometry")
        self.release_anim.setEasingCurve(QEasingCurve.OutBounce)
        self.release_anim.setDuration(300)
        
    def handleClick(self):
        self.is_on = not self.is_on
        if self.is_on:
            self.startFlicker()
            self.setText("Flicker Mode ON")
            self.setStyleSheet("""
                QPushButton {
                    background-color: #000000;
                    color: #00ff00;
                    border: 2px solid #00ff00;
                    border-radius: 10px;
                    padding: 10px 20px;
                    font-size: 16px;
                    font-weight: bold;
                    min-width: 120px;
                    min-height: 40px;
                }
                QPushButton:hover {
                    background-color: #1a1a1a;
                    border-color: #00ff00;
                    color: #00ff00;
                }
            """)
        else:
            self.stopFlicker()
            self.setText("Flicker Mode OFF")
            self.setStyleSheet("""
                QPushButton {
                    background-color: #000000;
                    color: #ffffff;
                    border: 2px solid #333333;
                    border-radius: 10px;
                    padding: 10px 20px;
                    font-size: 16px;
                    font-weight: bold;
                    min-width: 120px;
                    min-height: 40px;
                }
                QPushButton:hover {
                    background-color: #1a1a1a;
                    border-color: #444444;
                }
            """)
        
        # Trigger pop animation
        self.animateClick()
        
    def animateClick(self):
        # Get current geometry
        geo = self.geometry()
        
        # Press down animation
        self.press_anim.setStartValue(geo)
        pressed_geo = geo.adjusted(0, 5, 0, 5)  # Move down 5 pixels
        self.press_anim.setEndValue(pressed_geo)
        self.press_anim.start()
        
        # Pop up animation after delay
        QTimer.singleShot(150, self.animateRelease)
        
    def animateRelease(self):
        geo = self.geometry()
        self.release_anim.setStartValue(geo)
        release_geo = geo.adjusted(0, -5, 0, -5)  # Move up 5 pixels
        self.release_anim.setEndValue(release_geo)
        self.release_anim.start()
        
    def startFlicker(self):
        self.flicker_timer.start(500)  # Flicker every 500ms
        
    def stopFlicker(self):
        self.flicker_timer.stop()
        
    def toggleFlicker(self):
        if self.is_on:
            current_style = self.styleSheet()
            if "color: #00ff00" in current_style:
                # Switch to dim
                self.setStyleSheet("""
                    QPushButton {
                        background-color: #000000;
                        color: white;
                        border: 2px solid white;
                        border-radius: 10px;
                        padding: 10px 20px;
                        font-size: 16px;
                        font-weight: bold;
                        min-width: 120px;
                        min-height: 40px;
                    }
                    QPushButton:hover {
                        background-color: #1a1a1a;
                        border-color: #006400;
                        color: #006400;
                    }
                """)
            else:
                # Switch to bright
                self.setStyleSheet("""
                    QPushButton {
                        background-color: white;
                        color: black;
                        border: 2px solid black;
                        border-radius: 10px;
                        padding: 10px 20px;
                        font-size: 16px;
                        font-weight: bold;
                        min-width: 120px;
                        min-height: 40px;
                    }
                    QPushButton:hover {
                        background-color: #1a1a1a;
                        border-color: #00ff00;
                        color: #00ff00;
                    }
                """)

# Example usage
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Flicker Button Demo")
        self.setStyleSheet("background-color: #121212;")
        
        # Create central widget
        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)
        
        # Create layout
        layout = QtWidgets.QVBoxLayout(central_widget)
        layout.setAlignment(QtCore.Qt.AlignCenter)
        
        # Create flicker button
        self.flicker_button = FlickerButton("Flicker Mode OFF")
        layout.addWidget(self.flicker_button)
        
        # Set window size
        self.setMinimumSize(300, 200)

# Run the application
if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())