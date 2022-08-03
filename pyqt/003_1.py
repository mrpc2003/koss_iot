import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QTextEdit, QPushButton
from PyQt5.QtGui import QPainter, QColor, QFont, QPen, QBrush
from PyQt5.QtCore import Qt
import random

class myapp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        # 테스트버튼 = QPushButton('버튼입니다', self)
        # 테스트버튼.setGeometry(50,200,100,40)
        # 테스트버튼.move(50,100)
        # 테스트버튼.resize(100,50)
        # 테스트버튼.setFixedSize(w,h)
        # 테스트버튼.setFixedWidth(w)
        # 테스트버튼.setFixedHeight(h)
        
        파이라벨 = QLabel('나는 파이',self)
        파이라벨.move(60,20)
        썬라벨 = QLabel('나는 파이',self)
        썬라벨.move(230,60)
        
        파이이미지 = QLabel(self)
        파이이미지.move(230,60)
        썬이미지 = QLabel(self)
        썬이미지.move(230,60)

        파이버튼 = QLabel('파이',self)
        파이버튼.move(230,60)
        썬버튼 = QLabel('썬',self)
        썬버튼.move(230,60)

        self.text = 'Hello Weniv World!'
        self.setGeometry(400, 100, 200, 600)
        self.setWindowTitle('기본위치')
        self.show()


        
app = QApplication(sys.argv)
ex = myapp()
app.exec_()