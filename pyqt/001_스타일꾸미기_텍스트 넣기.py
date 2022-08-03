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
        self.drawText(Event, paint)
        paint.end()

    def drawText(self, event, paint):
        paint.setPen(QColor(10, 10, 10))
        paint.setFont(QFont('Decorative', 10))
        paint.drawText(130, 100, 'Hello World!!')
        paint.drawText(event.rect(), Qt.AlignCenter, self.text)

app = QApplication(sys.argv)
ex = myapp()
app.exec_()