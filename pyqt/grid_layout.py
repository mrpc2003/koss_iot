import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QTextEdit, QPushButton, QHBoxLayout,QVBoxLayout,QGridLayout
from PyQt5.QtGui import QPainter, QColor, QFont, QPen, QBrush, QPixmap
from PyQt5.QtCore import Qt
import random

class myapp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        insert = QPushButton('insert')
        home = QPushButton('home')
        pageUp = QPushButton('pageUp')
        delete = QPushButton('delete')
        end = QPushButton('end')
        pageDown = QPushButton('pageDown')
        keyboard = QPushButton('keyboard')
        

        grid = QGridLayout()
        grid.setSpacing(25)

        grid.addWidget(insert, 0, 0)
        grid.addWidget(home, 0, 1)
        grid.addWidget(pageUp, 0, 2)

        grid.addWidget(delete, 1, 0)
        grid.addWidget(end, 1, 1)
        grid.addWidget(pageDown, 1, 2)

        grid.addWidget(keyboard, 2,0,2,3,alignment=Qt.AlignHCenter) #수평 방향으로 가운데로 설정
        self.setLayout(grid)



        self.text = 'Hello Weniv World!'
        self.setGeometry(300, 300, 400, 300)
        self.setWindowTitle('기본위치')
        self.show()


        
app = QApplication(sys.argv)
ex = myapp()
app.exec_()