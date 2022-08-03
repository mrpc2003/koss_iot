import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QTextEdit, QPushButton, QHBoxLayout,QVBoxLayout,QGridLayout
from PyQt5.QtGui import QPainter, QColor, QFont, QPen, QBrush, QPixmap
from PyQt5.QtCore import Qt
import random

class MyApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Box Layout")
        self.setGeometry(300,300,500,500)

        self.label1 = QLabel()
        self.label2 = QLabel()
        self.label3 = QLabel()
        self.label4 = QLabel()
        self.label5 = QLabel()

        self.hbox = QHBoxLayout()
        self.Cvbox = QVBoxLayout()
        self.Chbox = QHBoxLayout()
        self.setLayout(self.hbox)
        

        self.initUI()

    def initUI(self):
        self.label1.setText('label1')
        self.label2.setText('label2')
        self.label3.setText('label3')
        self.label4.setText('label4')
        self.label5.setText('label5')
        
        self.label1.setAlignment(Qt.AlignCenter)
        self.label2.setAlignment(Qt.AlignCenter)
        self.label3.setAlignment(Qt.AlignCenter)
        self.label4.setAlignment(Qt.AlignCenter)
        self.label5.setAlignment(Qt.AlignCenter)

        self.label1.setStyleSheet('background-color: yellow')
        self.label2.setStyleSheet('background-color: red')
        self.label3.setStyleSheet('background-color: blue')
        self.label4.setStyleSheet('background-color: pink')
        self.label5.setStyleSheet('background-color: gray')

        self.Chbox.addWidget(self.label1)
        self.Chbox.addWidget(self.label2)
        self.Cvbox.addWidget(self.label3)
        self.Cvbox.addWidget(self.label4)
        self.Cvbox.addWidget(self.label5)
        self.hbox.addLayout(self.Chbox)
        self.hbox.addLayout(self.Cvbox)
        
        self.show()
    
    



        
app = QApplication(sys.argv)
ex = MyApp()
app.exec_()