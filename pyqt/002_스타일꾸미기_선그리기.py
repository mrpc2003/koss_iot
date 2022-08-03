import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QTextEdit, QPushButton
from PyQt5.QtGui import QPainter, QColor, QFont, QPen, QBrush
from PyQt5.QtCore import Qt

class myapp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.text = 'Hello Weniv World!'
        self.setGeometry(150, 300, 250, 500)
        self.setWindowTitle('QPainter!')
        self.show()

    def paintEvent(self, Event):
        paint = QPainter()
        paint.begin(self)
        self.drawLine(paint)
        paint.end()

    def drawLine(self, paint):
        pen = QPen(Qt.blue, 4, Qt.SolidLine)
        paint.setPen(pen)
        paint.drawLine(100, 40, 400, 40)

        pen.setStyle(Qt.DashLine)
        pen.setColor(Qt.yellow)
        paint.setPen(pen)
        paint.drawLine(100, 80, 400, 80)

        pen.setStyle(Qt.DashDotLine)
        pen.setColor(Qt.red)
        paint.setPen(pen)
        paint.drawLine(100, 120, 400, 120)

        pen.setStyle(Qt.DashDotDotLine)
        pen.setColor(Qt.darkMagenta)
        paint.setPen(pen)
        paint.drawLine(100, 120, 400, 120)

        pen.setStyle(Qt.DotLine)
        pen.setColor(Qt.darkMagenta)
        paint.setPen(pen)
        paint.drawLine(100, 200, 400, 200)

        pen.setStyle(Qt.CustomDashLine)
        pen.setDashPattern([4,4,5,4])
        pen.setColor(Qt.darkGray)
        pen.setWidth(8)
        paint.setPen(pen)
        paint.drawLine(100, 240, 400, 240)


        
app = QApplication(sys.argv)
ex = myapp()
app.exec_()