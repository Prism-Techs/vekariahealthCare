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
        # Launch onboard without unsupported options
        self.keyboard_process = subprocess.Popen([
            'onboard'
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        # Wait a moment and raise the window to the top using xdotool
        QtCore.QTimer.singleShot(500, self.ensure_keyboard_on_top)

    def ensure_keyboard_on_top(self):
        """Ensure the Onboard keyboard window stays on top using xdotool."""
        try:
            subprocess.run([
                'xdotool', 'search', '--name', 'Onboard',
                'windowraise'
            ], stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
        except Exception as e:
            print(f"Error raising Onboard window: {e}")

    def hide_keyboard(self):
        """Hide the onboard keyboard."""
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
        """Clean up keyboard process when closing."""
        self.hide_keyboard()
        event.accept()
