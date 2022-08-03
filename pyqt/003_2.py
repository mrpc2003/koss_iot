import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QTextEdit, QPushButton, QHBoxLayout, QVBoxLayout, QGridLayout
from PyQt5.QtGui import QPainter, QColor, QFont, QPen, QBrush, QPixmap
from PyQt5.QtCore import Qt
import random


class myapp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        label1_img = QLabel("img-20200924T011502Z-001\img\weniv-licat.png")
        label1_img.setPixmap(
            QPixmap("img-20200924T011502Z-001\img\weniv-licat.png"))
        label1 = QLabel('내 이름은 라이캣')

        label2_img = QLabel("img-20200924T011502Z-001\img\weniv-mura.png")
        label2_img.setPixmap(
            QPixmap("img-20200924T011502Z-001\img\weniv-mura.png"))
        label2 = QLabel('내 이름은 뮤라')

        vbox1 = QVBoxLayout()
        vbox2 = QVBoxLayout()

        vbox1.addWidget(label1_img)
        vbox1.addWidget(label1)

        vbox2.addWidget(label2_img)
        vbox2.addWidget(label2)

        hbox = QHBoxLayout()
        hbox.addLayout(vbox1)
        hbox.addLayout(vbox2)

        self.text = 'Hello Weniv World!'
        self.setGeometry(300, 300, 400, 300)
        self.setWindowTitle('기본위치')
        self.show()


app = QApplication(sys.argv)
ex = myapp()
app.exec_()
