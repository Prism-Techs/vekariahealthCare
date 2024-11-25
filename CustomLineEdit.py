from customKeyboard import VirtualKeyboard
from globalvar import  globaladc as buzzer
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import QLineEdit
from PyQt5 import QtCore, QtGui, QtWidgets


class CustomLineEdit(QtWidgets.QLineEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.keyboard = None

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        # Show keyboard on mouse press
        self.show_keyboard()

    def show_keyboard(self):
        if self.keyboard is None or not self.keyboard.isVisible():
            keyboard_width = 800
            keyboard_height = 400
            
            # Get main window geometry
            main_window = self.window()
            window_rect = main_window.geometry()
            
            # Calculate keyboard position
            keyboard_x = window_rect.x() + (window_rect.width() - keyboard_width) // 2
            keyboard_y = window_rect.y() + window_rect.height() - keyboard_height - 50
            
            self.keyboard = VirtualKeyboard(self, main_window)
            self.keyboard.setFixedSize(keyboard_width, keyboard_height)
            self.keyboard.move(keyboard_x, keyboard_y)
            self.keyboard.show()


class CustomTextEdit(QtWidgets.QTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.keyboard = None

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        # Show keyboard on mouse press
        self.show_keyboard()

    def show_keyboard(self):
        if self.keyboard is None or not self.keyboard.isVisible():
            keyboard_width = 800
            keyboard_height = 400
            
            # Get main window geometry
            main_window = self.window()
            window_rect = main_window.geometry()
            
            # Calculate keyboard position
            keyboard_x = window_rect.x() + (window_rect.width() - keyboard_width) // 2
            keyboard_y = window_rect.y() + window_rect.height() - keyboard_height - 50
            
            self.keyboard = VirtualKeyboard(self, main_window)
            self.keyboard.setFixedSize(keyboard_width, keyboard_height)
            self.keyboard.move(keyboard_x, keyboard_y)
            self.keyboard.show()