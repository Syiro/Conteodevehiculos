from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtCore import Qt, QRect


class RectangleLabel(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.xmin = 0
        self.ymin = 0
        self.xmax = 0
        self.ymax = 0

    def setRectCoordinates(self, xmin, ymin, xmax, ymax):
        self.xmin = xmin
        self.ymin = ymin
        self.xmax = xmax
        self.ymax = ymax
        self.update()

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setPen(QPen(Qt.red, 2, Qt.SolidLine))
        painter.drawRect(QRect(self.xmin, self.ymin, self.xmax - self.xmin, self.ymax - self.ymin))
