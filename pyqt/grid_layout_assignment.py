import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QTextEdit, QPushButton, QHBoxLayout,QVBoxLayout,QGridLayout
from PyQt5.QtGui import QPainter, QColor, QFont, QPen, QBrush, QPixmap
from PyQt5.QtCore import Qt, QCoreApplication

class myapp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        grid = QGridLayout()
        self.setLayout(grid)
        
        # self.setGeometry(300, 300, 400, 300)
        # self.setWindowTitle('기본위치')
        self.des()
        self.form()
        self.button()

        grid.addWidget(self.titleDes,0,0)
        grid.addWidget(self.authorDes,1,0)
        grid.addWidget(self.textDes,2,0)
        grid.addWidget(self.titleForm,0,1)
        grid.addWidget(self.authorForm,1,1)
        grid.addWidget(self.textForm,2,1)
        grid.addWidget(self.submitBtn,0,2)
        grid.addWidget(self.resetBtn,1,2)
        grid.addWidget(self.closeBtn,2,2)
        self.show()

        
    def des(self):
        self.titleDes = QLabel('Title:')
        self.authorDes = QLabel('Author:')
        self.textDes = QLabel('Text:')

    def form(self):
        self.titleForm = QLineEdit()
        self.authorForm = QLineEdit()
        self.textForm = QTextEdit()

    def button(self):
        self.submitBtn = QPushButton('submit')
        self.submitBtn.clicked.connect(self.submit)

        self.resetBtn = QPushButton('reset')
        self.resetBtn.clicked.connect(self.reset)

        self.closeBtn = QPushButton('exit')        
        self.closeBtn.clicked.connect(self.close)

    def submit(self):
        self.title = self.titleForm.text()
        self.author = self.authorForm.text()
        self.text = self.textForm.toPlainText()
        print(f"title: {self.title}\nauthor: {self.author}\ntext:{self.text}")

    def reset(self):
        self.titleForm.clear()
        self.authorForm.clear()
        self.textForm.clear()

    def close(self):
        return QCoreApplication.instance().quit()

        

app = QApplication(sys.argv)
ex = myapp()
app.exec_()