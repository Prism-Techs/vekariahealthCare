from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import Qt, QPoint, QRect, pyqtSignal
from PyQt5.QtWidgets import (QDialog, QPushButton, QGridLayout, QVBoxLayout, 
                            QHBoxLayout, QLabel, QWidget)

class VirtualKeyboard(QDialog):
    def __init__(self, target_widget, parent=None):
        super().__init__(parent)
        self.target_widget = target_widget
        self.uppercase = False
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        # Debug flag
        self.debug_mode = True  # Set to True to enable debug prints
        
        # Resizing and dragging variables
        self.resize_margin = 1
        self.resizing = False
        self.resize_edge = None
        self.dragging = False
        self.offset = QPoint()
        
        self.setup_ui()
        self.setup_keyboard_layouts()
        self.create_buttons()
        self.apply_styles()
        
    def debug_print(self, message):
        if self.debug_mode:
            print(f"[VirtualKeyboard Debug] {message}")
            
    def setup_ui(self):
        self.debug_print("Setting up UI components")
        
        # Main layout
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(
            self.resize_margin, self.resize_margin,
            self.resize_margin, self.resize_margin
        )
        
        # Container widget
        self.container = QWidget()
        self.container.setObjectName("container")
        self.main_layout.addWidget(self.container)
        
        # Title bar
        self.title_bar = QWidget()
        self.title_bar_layout = QHBoxLayout(self.title_bar)
        self.title_bar_layout.setContentsMargins(0,0,0,0)
        
        self.title_label = QLabel("Virtual Keyboard")
        self.title_label.setStyleSheet("color: white; font-weight: bold;")
        self.title_bar_layout.addWidget(self.title_label)


        self.title_bar.setFixedHeight(30)

        
        # Container layout
        self.container_layout = QVBoxLayout(self.container)
        self.container_layout.setContentsMargins(0, 0, 0, 0)
        self.container_layout.addWidget(self.title_bar)
        
        # Keyboard grid
        self.keyboard_widget = QWidget()
        self.keyboard_layout = QGridLayout(self.keyboard_widget)
        self.keyboard_layout.setSpacing(6)
        self.container_layout.addWidget(self.keyboard_widget)
        
        # Set minimum size
        self.setMinimumSize(600, 300)
        
    def setup_keyboard_layouts(self):
        self.debug_print("Setting up keyboard layouts")
        
        # Standard QWERTY layout
        self.qwerty_keys = [
            ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "Back"],
            ["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P", "@"],
            ["A", "S", "D", "F", "G", "H", "J", "K", "L", "Enter"],
            ["Shift", "Z", "X", "C", "V", "B", "N", "M", ",", ".", "?"],
            ["123", "Space", "-", "_", "/", "Cancel"]
        ]

        # Symbol layout
        self.symbol_keys = [
            ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "Back"],
            ["!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "+"],
            ["=", "{", "}", "[", "]", ";", ":", "'", '"', "Enter"],
            ["~", "`", "\\", "|", "<", ">", "€", "£", "¥", "¢", "?"],
            ["ABC", "Space", "-", "_", "/", "Cancel"]
        ]

        self.current_keys = self.qwerty_keys
        
    def create_buttons(self):
        self.debug_print("Creating keyboard buttons")
        
        # Clear existing buttons
        for i in reversed(range(self.keyboard_layout.count())): 
            self.keyboard_layout.itemAt(i).widget().setParent(None)

        # Create new buttons
        for row_index, row in enumerate(self.current_keys):
            for col_index, key in enumerate(row):
                button = QPushButton(key)
                
                # Style based on key type
                if key in ["Back", "Enter", "Shift", "123", "ABC", "Cancel", "Space"]:
                    button.setStyleSheet(
                        "QPushButton {background-color: #475569; border-radius: 5px;}"
                        "QPushButton:pressed {background-color: #64748b;}"
                    )
                else:
                    button.setStyleSheet(
                        "QPushButton {background-color: #334155; border-radius: 5px;}"
                        "QPushButton:pressed {background-color: #475569;}"
                    )
                
                button.clicked.connect(lambda checked, k=key: self.key_pressed(k))
                self.keyboard_layout.addWidget(button, row_index, col_index)
                
    def apply_styles(self):
        self.debug_print("Applying styles")
        
        self.setStyleSheet("""
            QDialog {
                background: transparent;
            }
            #container {
                background-color: #1e293b;
                border: 1px solid #475569;
                border-radius: 10px;
            }
            QPushButton {
                color: white;
                border-radius: 5px;
                min-width: 40px;
                min-height: 40px;
            }
        """)
        
    def get_resize_edge(self, pos):
        rect = self.rect()
        margin = self.resize_margin
        
        # Define regions for different edges
        left = QRect(0, margin, margin, rect.height() - 2 * margin)
        right = QRect(rect.width() - margin, margin, margin, rect.height() - 2 * margin)
        top = QRect(margin, 0, rect.width() - 2 * margin, margin)
        bottom = QRect(margin, rect.height() - margin, rect.width() - 2 * margin, margin)
        
        top_left = QRect(0, 0, margin, margin)
        top_right = QRect(rect.width() - margin, 0, margin, margin)
        bottom_left = QRect(0, rect.height() - margin, margin, margin)
        bottom_right = QRect(rect.width() - margin, rect.height() - margin, margin, margin)
        
        if left.contains(pos): return 'left'
        if right.contains(pos): return 'right'
        if top.contains(pos): return 'top'
        if bottom.contains(pos): return 'bottom'
        if top_left.contains(pos): return 'top-left'
        if top_right.contains(pos): return 'top-right'
        if bottom_left.contains(pos): return 'bottom-left'
        if bottom_right.contains(pos): return 'bottom-right'
        return None
        
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            pos = event.pos()
            self.resize_edge = self.get_resize_edge(pos)
            if self.resize_edge:
                self.debug_print(f"Started resizing from edge: {self.resize_edge}")
                self.resizing = True
                self.start_pos = event.globalPos()
                self.start_geometry = self.geometry()
            else:
                self.debug_print("Started dragging")
                self.dragging = True
                self.offset = event.globalPos() - self.pos()
            event.accept()

    def mouseMoveEvent(self, event):
        if self.resizing and event.buttons() & Qt.LeftButton:
            self.handle_resize(event)
        elif self.dragging and event.buttons() & Qt.LeftButton:
            self.handle_drag(event)
            
    def handle_resize(self, event):
        delta = event.globalPos() - self.start_pos
        new_geometry = QRect(self.start_geometry)
        min_width = self.minimumWidth()
        min_height = self.minimumHeight()
        
        try:
            if self.resize_edge in ['left', 'top-left', 'bottom-left']:
                if self.start_geometry.width() - delta.x() >= min_width:
                    new_geometry.setLeft(self.start_geometry.left() + delta.x())
            if self.resize_edge in ['right', 'top-right', 'bottom-right']:
                if self.start_geometry.width() + delta.x() >= min_width:
                    new_geometry.setRight(self.start_geometry.right() + delta.x())
            if self.resize_edge in ['top', 'top-left', 'top-right']:
                if self.start_geometry.height() - delta.y() >= min_height:
                    new_geometry.setTop(self.start_geometry.top() + delta.y())
            if self.resize_edge in ['bottom', 'bottom-left', 'bottom-right']:
                if self.start_geometry.height() + delta.y() >= min_height:
                    new_geometry.setBottom(self.start_geometry.bottom() + delta.y())
                    
            self.setGeometry(new_geometry)
            self.debug_print(f"Resizing to: {new_geometry}")
            
        except Exception as e:
            self.debug_print(f"Resize error: {str(e)}")
            
    def handle_drag(self, event):
        try:
            new_pos = event.globalPos() - self.offset
            self.move(new_pos)
            self.debug_print(f"Dragging to position: {new_pos}")
        except Exception as e:
            self.debug_print(f"Drag error: {str(e)}")
            
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            if self.dragging:
                self.debug_print("Stopped dragging")
            if self.resizing:
                self.debug_print("Stopped resizing")
            self.dragging = False
            self.resizing = False
            self.resize_edge = None
            event.accept()
            
    def enterEvent(self, event):
        self.update_cursor(event.pos())
        super().enterEvent(event)
        
    def leaveEvent(self, event):
        self.setCursor(Qt.ArrowCursor)
        super().leaveEvent(event)
        
    def update_cursor(self, pos):
        edge = self.get_resize_edge(pos)
        if edge in ['left', 'right']:
            self.setCursor(Qt.SizeHorCursor)
        elif edge in ['top', 'bottom']:
            self.setCursor(Qt.SizeVerCursor)
        elif edge in ['top-left', 'bottom-right']:
            self.setCursor(Qt.SizeFDiagCursor)
        elif edge in ['top-right', 'bottom-left']:
            self.setCursor(Qt.SizeBDiagCursor)
        else:
            self.setCursor(Qt.ArrowCursor)
            
    def key_pressed(self, key):
        self.debug_print(f"Key pressed: {key}")
        
        try:
            # Try to trigger buzzer if available
            from globalvar import globaladc
            globaladc.buzzer_1()
        except Exception as e:
            self.debug_print(f"Buzzer error: {e}")

        try:
            if key == "Back":
                self.target_widget.backspace()
            elif key == "Enter":
                self.close()
                self.target_widget.keyboard = None
            elif key == "Space":
                self.target_widget.insert(" ")
            elif key == "Shift":
                self.handle_shift()
            elif key == "123":
                self.switch_to_symbols()
            elif key == "ABC":
                self.switch_to_qwerty()
            elif key == "Cancel":
                self.close()
                self.target_widget.keyboard = None
            else:
                self.target_widget.insert(key.upper() if self.uppercase else key.lower())
        except Exception as e:
            self.debug_print(f"Key press error: {str(e)}")
            
    def handle_shift(self):
        self.uppercase = not self.uppercase
        for i in range(self.keyboard_layout.count()):
            button = self.keyboard_layout.itemAt(i).widget()
            if isinstance(button, QPushButton) and len(button.text()) == 1:
                button.setText(button.text().upper() if self.uppercase else button.text().lower())
                
    def switch_to_symbols(self):
        self.debug_print("Switching to symbols layout")
        self.current_keys = self.symbol_keys
        self.create_buttons()
        
    def switch_to_qwerty(self):
        self.debug_print("Switching to QWERTY layout")
        self.current_keys = self.qwerty_keys
        self.create_buttons()