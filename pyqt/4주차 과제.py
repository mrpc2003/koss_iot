import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QTextEdit, QPushButton, QHBoxLayout,QVBoxLayout,QGridLayout
from PyQt5.QtGui import QPainter, QColor, QFont, QPen, QBrush, QPixmap
from PyQt5.QtCore import Qt
import random

class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        worst_img = QLabel("finedust\worst.png")
        worst_img.setPixmap(QPixmap("finedust\worst.png"))
        worst = QLabel('매우 나쁨')

        bad_img = QLabel("finedust\\bad.png")
        bad_img.setPixmap(QPixmap("finedust\\bad.png"))
        bad = QLabel('나쁨')

        good_img = QLabel("finedust\good.png")
        good_img.setPixmap(QPixmap("finedust\good.png"))
        good = QLabel('좋음')

        best_img = QLabel("finedust\\best.png")
        best_img.setPixmap(QPixmap("finedust\\best.png"))
        best = QLabel('매우 좋음')

        vbox1 = QVBoxLayout()
        vbox2 = QVBoxLayout()
        
        vbox1.addWidget(worst_img)
        vbox1.addWidget(worst)

        vbox2.addWidget(good_img)
        vbox2.addWidget(good)

        hbox= QHBoxLayout()
        hbox.addLayout(vbox1)
        hbox.addLayout(vbox2)

        self.show()
        # self.text = 'Hello Weniv World!'
        # self.setGeometry(300, 300, 400, 300)
        # self.setWindowTitle('기본위치')
       

app = QApplication(sys.argv)
ex = MyApp()
app.exec_()