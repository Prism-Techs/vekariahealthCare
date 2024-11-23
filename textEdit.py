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
        
        # Style the widget with pure black background
        self.setStyleSheet("""
            MultiValueBlock {
                background-color: #043770;
                border-radius: 8px;
            }
        """)
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Draw main background
        painter.setBrush(QColor('#043770'))
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(0, 0, self.width(), self.height(), 8, 8)
        
        # Draw 3D effect edges
        painter.setPen(QPen(QColor(255, 255, 255, 40), 2))
        painter.drawLine(2, 2, self.width()-2, 2)  # Top highlight
        painter.drawLine(2, 2, 2, self.height()-2)  # Left highlight
        
        painter.setPen(QPen(QColor(255, 255, 255, 20), 2))
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
            
            # Draw text (pure white)
            painter.setPen(QColor('white'))
            painter.drawText(text_rect, Qt.AlignCenter, str(value))
            
            # Draw separator line (except after last value)
            if i < len(self.values) - 1:
                line_y = int((i + 1) * text_height)
                
                # Draw bold white separator line
                painter.setPen(QPen(QColor('white'), 2))
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
        
        # Center the block
        container = QWidget()
        container_layout = QHBoxLayout(container)
        container_layout.addWidget(self.value_block)
        container_layout.setAlignment(Qt.AlignCenter)
        
        main_layout.addWidget(container)
        
        # Set window size
        self.setMinimumSize(200, 300)
        
        # Set pure black background for the window
        self.setStyleSheet("""
            QMainWindow {
                background-color: grey;
            }
            QWidget {
                background-color: grey;
            }
        """)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())