import sys
import matplotlib.font_manager as fm
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPixmap, QFontDatabase
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QHBoxLayout, QVBoxLayout, QMainWindow
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from pymongo import MongoClient  # pip install pymongo, pip install dnspython

client = MongoClient(
    "mongodb+srv://mrpc2003:rainb0w12@Cluster0.yxiwiyk.mongodb.net/?retryWrites=true&w=majority")

db = client['test']
collection = db['sensors']


class MyApp(QMainWindow):

    def __init__(self):
        super().__init__()

        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)

        dynamic_canvas = FigureCanvas(Figure(figsize=(5, 5)))

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

        # pm1TitleFont = self.pm1title.font()
        # pm2TitleFont = self.pm2title.font()
        # pm10TitleFont = self.pm10title.font()
        # imgStatusFont = self.imgstatus.font()

        # pm1TitleFont.setPointSize(20)
        # pm2TitleFont.setPointSize(20)
        # pm10TitleFont.setPointSize(20)
        # imgStatusFont.setPointSize(50)

        # imgStatusFont.setBold(True)

        # self.pm1title.setFont(pm1TitleFont)
        # self.pm2title.setFont(pm2TitleFont)
        # self.pm10title.setFont(pm10TitleFont)
        # self.imgstatus.setFont(imgStatusFont)


        vbox1.addWidget(self.pm1title)
        vbox1.addWidget(self.pm2title)
        vbox1.addWidget(self.pm10title)

        hbox1.addWidget(self.imgstatus)
        hbox1.addWidget(self.status)
        vbox2.addLayout(hbox1)

        vbox.addLayout(vbox1)
        vbox.addLayout(vbox2)
        vbox.addWidget(dynamic_canvas)

        self.createdtime = list()
        self.pm1 = list()
        self.pm2 = list()
        self.pm10 = list()

        self.dynamic_ax = dynamic_canvas.figure.subplots()
        self.timer = dynamic_canvas.new_timer(
            1000, [(self.update_canvas, (), {})])
        self.timer.start()

        self.setWindowTitle('실내 미세먼지 농도 측정기')
        self.setGeometry(300, 100, 600, 600)
        self.show()

    def update_canvas(self):
        path = 'Noto_Sans_KR\\NotoSansKR-Regular.otf'
        fontprop = fm.FontProperties(fname=path, size=18)

        self.dynamic_ax.clear()
        d = collection.find().sort('_id', -1).limit(1)
        for i in d:
            createdtime = str(i['created_at'])
            self.createdtime.append(createdtime[11:])
            self.pm1.append(int(i['pm1']))  # y축 좌표에는 센서 값
            self.pm2.append(int(i['pm2']))  # y축 좌표에는 센서 값
            self.pm10.append(int(i['pm10']))  # y축 좌표에는 센서 값

        if len(self.createdtime) >= 6:
            del self.createdtime[0]
            del self.pm1[0]
            del self.pm2[0]
            del self.pm10[0]

        self.pm1title.setText(f'현재 실내 pm1 농도는 {self.pm1[-1]}에요')
        self.pm2title.setText(f'현재 실내 pm2 농도는 {self.pm2[-1]}에요')
        self.pm10title.setText(f'현재 실내 pm10 농도는 {self.pm10[-1]}에요')

        if 0 <= self.pm10[-1] <= 30 or 0 <= self.pm2[-1] <= 15:
            self.status.setText('좋음')
            self.imgstatus.setPixmap(
                QPixmap("finedust\\best.png").scaled(50, 50))

        if 31 <= self.pm10[-1] <= 50 or 16 <= self.pm2[-1] <= 25:
            self.status.setText('보통')
            self.imgstatus.setPixmap(
                QPixmap("finedust\\good.png").scaled(50, 50))

        if 51 <= self.pm10[-1] <= 100 or 26 <= self.pm2[-1] <= 50:
            self.status.setText('나쁨')
            self.imgstatus.setPixmap(
                QPixmap("finedust\\bad.png").scaled(50, 50))

        if 101 <= self.pm10[-1] or 51 <= self.pm2[-1]:
            self.status.setText('매우 나쁨')
            self.imgstatus.setPixmap(
                QPixmap("finedust\\worst.png").scaled(50, 50))

        self.dynamic_ax.plot(self.createdtime, self.pm1,
                             color='limegreen', label='pm1', marker=".")
        self.dynamic_ax.plot(self.createdtime, self.pm2,
                             color='violet', label='pm2.5', marker=".")
        self.dynamic_ax.plot(self.createdtime, self.pm10,
                             color='dodgerblue', label='pm10', marker=".")
        self.dynamic_ax.legend(
            loc=(0, 1), ncol=3, fontsize=10, frameon=True, shadow=True)
        self.dynamic_ax.set_xlabel('시간', fontproperties=fontprop)
        self.dynamic_ax.set_ylabel('㎍/㎥', fontproperties=fontprop)
        self.dynamic_ax.grid(True, axis='y')
        self.dynamic_ax.figure.canvas.draw()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()

    id = QFontDatabase.addApplicationFont("Noto_Sans_KR\\NotoSansKR-Bold.otf")
    _fontstr = QFontDatabase.applicationFontFamilies(id)[0]
    _font = QFont(_fontstr)
    app.setFont(_font)

    sys.exit(app.exec_())
