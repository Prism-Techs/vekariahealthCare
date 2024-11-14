import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QTimer, Qt, QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import QPixmap
from login import Ui_Form
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtCore import QTimer, Qt, QPropertyAnimation, QEasingCurve, QEvent
from PyQt5.QtGui import QPixmap
from imagewrite import Ui_Form as WriteUPImageForm



class LoadingScreen(QWidget):
    def __init__(self):
        super().__init__()
        # Set size for 7-inch display (assuming 1024x600 resolution)
        self.setFixedSize(1024, 600)
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.CustomizeWindowHint | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.label = QLabel(self)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setGeometry(0, 0, 1024, 600)

        # Replace 'path/to/your/logo.png' with the actual path to your logo
        self.pixmap = QPixmap('logo.png')
        self.label.setPixmap(self.pixmap.scaled(1, 1, Qt.KeepAspectRatio, Qt.SmoothTransformation))

        self.timer = QTimer()
        self.timer.timeout.connect(self.animate_logo)
        self.timer.start(50)  # Adjust for faster/slower animation

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
        self.login_ui = Ui_Form()
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

if __name__ == '__main__':
    app = QApplication(sys.argv)
    loading_screen = LoadingScreen()
    loading_screen.show()
    sys.exit(app.exec_())
