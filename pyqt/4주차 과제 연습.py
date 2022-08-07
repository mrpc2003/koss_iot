import sys
# matplotlib의 graph에서 font를 설정하기 위한 font manager import
import matplotlib.font_manager as fm
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPixmap, QFontDatabase
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QHBoxLayout, QVBoxLayout, QMainWindow
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from pymongo import MongoClient  # Python에서 mongoDB를 이용하기 위한 라이브러리로 pymongo를 사용
# mongoDB의 내 데이터베이스 주소를 입력
client = MongoClient(
    "mongodb+srv://mrpc2003:rainb0w12@Cluster0.yxiwiyk.mongodb.net/?retryWrites=true&w=majority")

db = client['test']  # 'test' 이름의 데이터 베이스를 db변수로 지정
collection = db['sensors']  # 'sensors' 이름의 collections를 collection 변수로 지정


class MyApp(QMainWindow):

    def __init__(self):
        super().__init__()

        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)

        # matplotlib의 그래프를 가로 5인치, 세로 5인치로 설정
        dynamic_canvas = FigureCanvas(Figure(figsize=(5, 5)))

        # {vbox1, (hbox1 ⊂ vbox2)} ⊂ vbox
        # 변수 vbox에 수직 box layout을 지정(메인이 되는 layout)
        vbox = QVBoxLayout(self.main_widget)
        vbox1 = QVBoxLayout(self.main_widget)  # 변수 vbox1에 수직 box layout을 지정
        vbox2 = QVBoxLayout(self.main_widget)  # 변수 vbox2에 수직 box layout을 지정
        hbox1 = QHBoxLayout(self.main_widget)  # 변수 hbox1에 수평 box layout을 지정

        self.pm1title = QLabel()  # 변수 self.pm1title에 라벨을 지정
        self.pm2title = QLabel()  # 변수 self.pm2title에 라벨을 지정
        self.pm10title = QLabel()  # 변수 self.pm10title에 라벨을 지정
        self.imgstatus = QLabel()  # 변수 self.imgstatus에 라벨을 지정
        self.status = QLabel()  # 변수 self.status에 라벨을 지정

        # 변수 self.pm1title을 가운데 정렬 시킴
        self.pm1title.setAlignment(Qt.AlignCenter)
        # 변수 self.pm2title을 가운데 정렬 시킴
        self.pm2title.setAlignment(Qt.AlignCenter)
        # 변수 self.pm10title을 가운데 정렬 시킴
        self.pm10title.setAlignment(Qt.AlignCenter)
        # 변수 self.imgstatus을 오른쪽 정렬 시킴
        self.imgstatus.setAlignment(Qt.AlignRight)

        vbox1.addWidget(self.pm1title)  # vbox1 layout에 변수 self.pm1title을 추가
        vbox1.addWidget(self.pm2title)  # vbox1 layout에 변수 self.pm2title을 추가
        vbox1.addWidget(self.pm10title)  # vbox1 layout에 변수 self.pm10title을 추가

        hbox1.addWidget(self.imgstatus)  # hbox1 layout에 변수 self.imgstatus을 추가
        hbox1.addWidget(self.status)  # hbox1 layout에 변수 self.status을 추가
        vbox2.addLayout(hbox1)  # vbox2 layout에 hbox1 layout을 추가

        vbox.addLayout(vbox1)  # vbox layout에 vbox1 layout을 추가
        vbox.addLayout(vbox2)  # vbox layout에 vbox1 layout을 추가
        # vbox layout에 matplotlib graph(dynamic_canvas)를 추가
        vbox.addWidget(dynamic_canvas)

        self.createdtime = list()  # mongoDB로 부터 시간정보를 가져오기 위한 변수 self.createdtime을 list형태로 지정
        self.pm1 = list()  # mongoDB로 부터 시간정보를 가져오기 위한 변수 self.createdtime을 list형태로 지정
        self.pm2 = list()  # mongoDB로 부터 시간정보를 가져오기 위한 변수 self.createdtime을 list형태로 지정
        self.pm10 = list()  # mongoDB로 부터 시간정보를 가져오기 위한 변수 self.createdtime을 list형태로 지정

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
