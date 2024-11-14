import os
import subprocess
from PyQt5 import QtCore, QtWidgets

class RPiKeyboard(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.layout)

    def show_keyboard(self):
        try:
            # Set Onboard to stay on top using gsettings
            subprocess.run([
                'gsettings', 'set', 
                'org.onboard', 'force-to-top', 'true'
            ], stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
            
            subprocess.run([
                'gsettings', 'set',
                'org.onboard', 'window-state-sticky', 'true'
            ], stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
        except:
            pass

        # Launch onboard with stay-on-top flags
        self.keyboard_process = subprocess.Popen([
            'onboard',
            '--force-to-top',
            '--state', 'SHOWING'
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        # Give a moment for keyboard to appear then ensure it's on top
        QtCore.QTimer.singleShot(500, self.ensure_keyboard_on_top)

    def ensure_keyboard_on_top(self):
        """Make sure keyboard stays on top"""
        try:
            # Use xdotool to force keyboard window to top
            subprocess.run([
                'xdotool', 'search', '--name', 'Onboard',
                'windowraise'
            ], stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
        except:
            pass

    def hide_keyboard(self):
        """Hide the onboard keyboard"""
        try:
            if hasattr(self, 'keyboard_process') and self.keyboard_process:
                self.keyboard_process.terminate()
                self.keyboard_process = None
                
            # Kill any running onboard process
            try:
                subprocess.run(['killall', 'onboard'], 
                            stderr=subprocess.DEVNULL, 
                            stdout=subprocess.DEVNULL)
            except:
                pass
        except Exception as e:
            print(f"Error hiding keyboard: {e}")

    def closeEvent(self, event):
        """Clean up keyboard process when closing"""
        self.hide_keyboard()
        event.accept()