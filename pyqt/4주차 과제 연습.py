import sys
from datetime import datetime
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QColor, QFont, QPen, QBrush, QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QTextEdit, QPushButton, QHBoxLayout, QVBoxLayout, QGridLayout
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from pymongo import MongoClient  # pip install pymongo, pip install dnspython

client = MongoClient(
    "mongodb+srv://mrpc2003:rainb0w12@Cluster0.yxiwiyk.mongodb.net/?retryWrites=true&w=majority")

db = client['test']


class MyApp(QMainWindow):

    def __init__(self):
        super().__init__()

        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)

        canvas = FigureCanvas(Figure(figsize=(4, 3)))
        vbox = QVBoxLayout(self.main_widget)
        vbox1 = QVBoxLayout(self.main_widget)
        vbox2 = QVBoxLayout(self.main_widget)
        hbox1 = QHBoxLayout(self.main_widget)

        self.pm1title = QLabel()
        self.pm2title = QLabel()
        self.pm10title = QLabel()
        self.imgstatus = QLabel()

        self.status = QLabel()

        self.pm1title.setAlignment(Qt.AlignCenter)
        self.pm2title.setAlignment(Qt.AlignCenter)
        self.pm10title.setAlignment(Qt.AlignCenter)
        self.imgstatus.setAlignment(Qt.AlignRight)

        vbox1.addWidget(self.pm1title)
        vbox1.addWidget(self.pm2title)
        vbox1.addWidget(self.pm10title)

        hbox1.addWidget(self.imgstatus)
        hbox1.addWidget(self.status)

        vbox2.addLayout(hbox1)

        vbox.addLayout(vbox1)
        vbox.addLayout(vbox2)

        vbox.addWidget(canvas)

        self.addToolBar(NavigationToolbar(canvas, self))

        self.ax = canvas.figure.subplots()
        self.x = list()
        self.createdtime = list()
        self.pm1 = list()
        self.pm2 = list()
        self.pm10 = list()

        # sensors 데이터베이스의 가장 최근 값 10개를 뒤집어서 가져옴
        for d, cnt in zip(db['sensors'].find(), range(10, 0, -1)):
            self.x.append(cnt)  # x축 좌표에는 카운트 값
            createdtime = (str(d['created_at']))
            self.createdtime.append(createdtime[11:])
            self.pm1.append(int(d['pm1']))  # y축 좌표에는 센서 값
            self.pm2.append(int(d['pm2']))  # y축 좌표에는 센서 값
            self.pm10.append(int(d['pm10']))  # y축 좌표에는 센서 값
        self.pm1title.setText(f'현재 실내 pm1 미세먼지 농도는 {self.pm1[-1]}에요')
        self.pm2title.setText(f'현재 실내 pm2 미세먼지 농도는 {self.pm2[-1]}에요')
        self.pm10title.setText(f'현재 실내 pm10 미세먼지 농도는 {self.pm10[-1]}에요')

        if 0 <= self.pm10[-1] <= 30 or 0 <= self.pm2[-1] <= 15:
            self.status.setText('좋음')
            self.imgstatus.setPixmap(
                QPixmap("finedust\\best.png").scaled(35, 35))

        if 31 <= self.pm10[-1] <= 50 or 16 <= self.pm2[-1] <= 25:
            self.status.setText('보통')
            self.imgstatus.setPixmap(
                QPixmap("finedust\\good.png").scaled(35, 35))

        if 51 <= self.pm10[-1] <= 100 or 26 <= self.pm2[-1] <= 50:
            self.status.setText('나쁨')
            self.imgstatus.setPixmap(
                QPixmap("finedust\\bad.png").scaled(35, 35))

        if 101 <= self.pm10[-1] or 51 <= self.pm2[-1]:
            self.status.setText('매우 나쁨')
            self.imgstatus.setPixmap(
                QPixmap("finedust\\worst.png").scaled(35, 35))

        finedustpm1 = self.ax.plot(self.createdtime, self.pm1, '-')
        finedustpm2 = self.ax.plot(self.createdtime, self.pm2, '-')
        finedustpm10 = self.ax.plot(self.createdtime, self.pm10, '-')
        finedustpm1
        finedustpm2
        finedustpm10

        self.setWindowTitle('Matplotlib in PyQt5')
        self.setGeometry(300, 100, 600, 400)
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
