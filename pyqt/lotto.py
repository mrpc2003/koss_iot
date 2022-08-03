import sys, random
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QToolTip
from PyQt5.QtGui import QIcon, QPixmap, QFont
from PyQt5.QtCore import QCoreApplication

class Lotto(QWidget):
    def __init__(self):
        super().__init__()
        self.ui_init()
        self.cnt = 0
        self.lotto_num = ["00", "00", "00", "00", "00", "00"]

    def ui_init(self):
        self.image()
        self.button()
        self.num()

        self.setWindowTitle("Lotto")
        self.setWindowIcon(QIcon("img-20200924T011502Z-001\img\weniv-binky.png"))
        self.setGeometry(0, 0, 400, 400)
        self.show()

    def image(self):
        self.img = QLabel(self)
        self.img.setPixmap(QPixmap("img-20200924T011502Z-001\img\weniv-binky.png").scaled(35, 35))
        self.move(10, 10)

    def button(self):
        self.BUTTON = QPushButton("추첨", self)
        self.BUTTON.setFixedSize(340, 40)
        self.BUTTON.move(30, 290)
        self.BUTTON.clicked.connect(self.random)

        self.EXIT = QPushButton("종료", self)
        self.EXIT.setFixedSize(340, 40)
        self.EXIT.move(30, 340)
        self.EXIT.clicked.connect(self.close)

    def num(self):
        self.label = QLabel("00", self)
        self.label.setFont(QFont("Helvetica", pointSize=75, weight=2))
        self.label.move(150, 50)

        self.num1 = QLabel("00", self)
        self.num1.setFont(QFont("Helvetica", pointSize=30, weight=1))
        self.num1.move(30, 200)

        self.num2 = QLabel("00", self)
        self.num2.setFont(QFont("Helvetica", pointSize=30, weight=1))
        self.num2.move(90, 200)

        self.num3 = QLabel("00", self)
        self.num3.setFont(QFont("Helvetica", pointSize=30, weight=1))
        self.num3.move(150, 200)

        self.num4 = QLabel("00", self)
        self.num4.setFont(QFont("Helvetica", pointSize=30, weight=1))
        self.num4.move(210, 200)

        self.num5 = QLabel("00", self)
        self.num5.setFont(QFont("Helvetica", pointSize=30, weight=1))
        self.num5.move(270, 200)

        self.num6 = QLabel("00", self)
        self.num6.setFont(QFont("Helvetica", pointSize=30, weight=1))
        self.num6.move(325, 200)

    def random(self):
        if self.cnt == 6: #초기화 
            self.cnt = 0
            self.lotto_num = ["00", "00", "00", "00", "00", "00"]

        while True:
            ball = str(random.randint(1,46))
            if len(ball) == 1:
                ball = "0" + ball
            if ball not in self.lotto_num:
                break

        self.lotto_num[self.cnt] = ball
        print(ball)
        self.label.setText(ball)

        self.num1.setText(self.lotto_num[0])
        self.num2.setText(self.lotto_num[1])
        self.num3.setText(self.lotto_num[2])
        self.num4.setText(self.lotto_num[3])
        self.num5.setText(self.lotto_num[4])
        self.num6.setText(self.lotto_num[5])

        self.cnt += 1
        print("*"+str(self.cnt))

    def close(self):
        return QCoreApplication.instance().quit()

cnt = 0
loop = QApplication(sys.argv)
lotto_program = Lotto()
loop.exec_()