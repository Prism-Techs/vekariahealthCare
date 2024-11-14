from PyQt5.QtGui import QPainter, QPen, QColor
from PyQt5.QtCore import Qt, QTimer, QDateTime
from PyQt5.QtWidgets import QMessageBox
from PyQt5 import QtCore, QtGui, QtWidgets






class WifiStatusLabel(QtWidgets.QPushButton):
    """Custom QPushButton to draw red cross when disconnected"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.is_connected = False
        self._original_pixmap = None
        
        # Setup button properties
        self.setFlat(True)  # Make button background transparent
        self.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.setStyleSheet("""
            QPushButton {
                border: none;
                background-color: transparent;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.1);
            }
        """)

    def setIcon(self, icon):
        """Set icon and store original pixmap"""
        self._original_pixmap = icon.pixmap(self.size())
        super().setIcon(icon)
        self.setIconSize(self.size())
        self.update()

    def setPixmap(self, pixmap):
        """Convert pixmap to icon and set it"""
        icon = QtGui.QIcon(pixmap)
        self.setIcon(icon)
        self._original_pixmap = pixmap
        self.update()

    def paintEvent(self, event):
        super().paintEvent(event)  # Draw the button and icon
        
        if self._original_pixmap is None:
            return
        
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Calculate icon position
        icon_rect = QtCore.QRect(0, 0, self.width(), self.height())
        
        # If disconnected, draw the red cross
        if not self.is_connected:
            try:
                pen = QPen(QColor('red'))
                pen.setWidth(3)
                painter.setPen(pen)
                # Draw diagonal line
                painter.drawLine(0, self.height(), self.width(), 0)
            finally:
                painter.end()

    def update_connection_status(self, is_connected):
        """Update connection status and trigger repaint"""
        self.is_connected = is_connected
        self.update()

    def sizeHint(self):
        """Return the ideal size for the button"""
        if self._original_pixmap:
            return self._original_pixmap.size()
        return super().sizeHint()