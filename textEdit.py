import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QLabel, 
                           QVBoxLayout, QHBoxLayout, QGraphicsDropShadowEffect)
from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QPainter, QPen, QColor, QLinearGradient, QGradient

class MultiValueBlock(QWidget):
    def __init__(self, values=None):
        super().__init__()
        self.values = values or ["25.6", "25.6", "25.6", "25.6"]
        self.setupUI()
        
    def setupUI(self):
        # Set fixed size for the block
        self.setFixedSize(120, 200)
        
        # Add drop shadow effect
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(15)
        shadow.setOffset(5, 5)
        shadow.setColor(QColor(0, 0, 0, 180))
        self.setGraphicsEffect(shadow)
        
        # Style the widget
        self.setStyleSheet("""
            MultiValueBlock {
                background-color: #2c3e50;
                border-radius: 8px;
            }
        """)
        
        # Make widget accept mouse hover events
        self.setMouseTracking(True)
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Create gradient background
        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0, QColor('#34495e'))
        gradient.setColorAt(1, QColor('#2c3e50'))
        
        # Draw main background with gradient
        painter.setBrush(gradient)
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(0, 0, self.width(), self.height(), 8, 8)
        
        # Draw 3D effect edges
        painter.setPen(QPen(QColor(255, 255, 255, 30), 2))
        painter.drawLine(2, 2, self.width()-2, 2)  # Top highlight
        painter.drawLine(2, 2, 2, self.height()-2)  # Left highlight
        
        painter.setPen(QPen(QColor(0, 0, 0, 60), 2))
        painter.drawLine(self.width()-2, 2, self.width()-2, self.height()-2)  # Right shadow
        painter.drawLine(2, self.height()-2, self.width()-2, self.height()-2)  # Bottom shadow
        
        # Set text properties
        painter.setPen(QColor('white'))
        font = painter.font()
        font.setPointSize(14)
        font.setBold(True)
        painter.setFont(font)
        
        # Calculate metrics
        text_height = self.height() / len(self.values)
        
        # Draw values and lines
        for i, value in enumerate(self.values):
            # Calculate rectangle for text
            y_pos = int(i * text_height)
            text_rect = QRect(0, y_pos, self.width(), int(text_height))
            
            # Draw text with shadow effect
            # Draw text shadow
            painter.setPen(QColor(0, 0, 0, 100))
            shadow_rect = QRect(text_rect)
            shadow_rect.translate(1, 1)
            painter.drawText(shadow_rect, Qt.AlignCenter, str(value))
            
            # Draw main text
            painter.setPen(QColor('white'))
            painter.drawText(text_rect, Qt.AlignCenter, str(value))
            
            # Draw separator line (except after last value)
            if i < len(self.values) - 1:
                line_y = int((i + 1) * text_height)
                
                # Draw bold separator line with 3D effect
                # Bottom shadow
                painter.setPen(QPen(QColor(0, 0, 0, 120), 3))
                painter.drawLine(8, line_y + 1, self.width() - 8, line_y + 1)
                
                # Main line
                painter.setPen(QPen(QColor(255, 255, 255, 180), 2))
                painter.drawLine(8, line_y, self.width() - 8, line_y)

    def setValues(self, values):
        self.values = values
        self.update()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Multi-Value 3D Block Display")
        self.setupUI()
        
    def setupUI(self):
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Create main layout
        main_layout = QVBoxLayout(central_widget)
        
        # Add some padding around the widget
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # Create block
        self.value_block = MultiValueBlock()
        self.value_block.setValues(["25.6", "25.6", "25.6", "25.6",'24.89'])
        
        # Center the block
        container = QWidget()
        container_layout = QHBoxLayout(container)
        container_layout.addWidget(self.value_block)
        container_layout.setAlignment(Qt.AlignCenter)
        
        main_layout.addWidget(container)
        
        # Set window size
        self.setMinimumSize(200, 300)
        
        # Set background color for the window
        self.setStyleSheet("""
            QMainWindow {
                background-color: black;
            }
            QWidget {
                background-color: black;
            }
        """)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())