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


class MyApp(QMainWindow):  # MyApp 클래스를 만드는데 QMainWindow 클래스를 상속받는다

    def __init__(self):  # 파이썬의 생성자명은 __init__ 고정이므로 첫번째 고정값은 self -> instance 이름을 self로
        super().__init__()

        self.main_widget = QWidget()  # 프로그램의 메인 위젯 설정
        self.setCentralWidget(self.main_widget)  # 메인 위젯 가운데 정렬 설정

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

        self.dynamic_ax = dynamic_canvas.figure.subplots()  # matplotlib의 figure에 plot 추가
        self.timer = dynamic_canvas.new_timer(  # 1초 (1000ms)마다 graph 업데이트
            1000, [(self.update_canvas, (), {})])
        self.timer.start()  # 타이머 시작

        self.setWindowTitle('실내 미세먼지 농도 측정기')  # 프로그램 title 설정
        # 생성할 창의 위치 왼쪽에서 떨어진 값, 위쪽에서 떨어진 값, 창의 크기 가로, 창의 크기 세로
        self.setGeometry(300, 100, 600, 600)
        self.show()  # 창 보여주기

    def update_canvas(self):  # graph 업데이트 함수 작성
        path = 'Noto_Sans_KR\\NotoSansKR-Regular.otf'  # font path 설정
        # graph에 표시되는 font와 size 설정
        fontprop = fm.FontProperties(fname=path, size=18)

        self.dynamic_ax.clear()  # graph 화면 초기화
        # mongoDB에서 id값을 기준으로 최신순 정렬을 하여 변수 d에 1개만 저장
        d = collection.find().sort('_id', -1).limit(1)
        for i in d:
            createdtime = str(i['created_at'])
            self.createdtime.append(createdtime[11:])
            self.pm1.append(int(i['pm1']))  # y축 좌표에는 센서 값
            self.pm2.append(int(i['pm2']))  # y축 좌표에는 센서 값
            self.pm10.append(int(i['pm10']))  # y축 좌표에는 센서 값

        if len(self.createdtime) >= 6:  # (그래프 영역이 겹쳐서 보이지 않도록 하기 위해서) 가져온 데이터가 6개 보다 많아진다면
            del self.createdtime[0]  # 가장 첫번째 시간 데이터 삭제
            del self.pm1[0]  # 가장 첫번째 pm1 데이터 삭제
            del self.pm2[0]  # 가장 첫번째 pm2 데이터 삭제
            del self.pm10[0]  # 가장 첫번째 pm10 데이터 삭제

        self.pm1title.setText(
            f'현재 실내 pm1 농도는 {self.pm1[-1]}에요')  # 실내 pm1 농도 업데이트
        self.pm2title.setText(
            f'현재 실내 pm2 농도는 {self.pm2[-1]}에요')  # 실내 pm2.5 농도 업데이트
        self.pm10title.setText(
            f'현재 실내 pm10 농도는 {self.pm10[-1]}에요')  # 실내 pm10 농도 업데이트

        # 만약 pm10 농도가 30이하이거나 pm2 농도가 15이하일 때
        if 0 <= self.pm10[-1] <= 30 or 0 <= self.pm2[-1] <= 15:
            self.status.setText('좋음')  # '좋음' 출력
            self.imgstatus.setPixmap(
                QPixmap("finedust\\best.png").scaled(50, 50))  # 현재상태 좋음 사진으로 교체

        # 만약 pm10 농도가 31이상 50이하이거나 pm2 농도가 16이상 25이하일 때
        if 31 <= self.pm10[-1] <= 50 or 16 <= self.pm2[-1] <= 25:
            self.status.setText('보통')  # '보통' 출력
            self.imgstatus.setPixmap(
                QPixmap("finedust\\good.png").scaled(50, 50))  # 현재상태 보통 사진으로 교체

        # 만약 pm10 농도가 51이상 100이하이거나 pm2 농도가 26이상 50이하일 때
        if 51 <= self.pm10[-1] <= 100 or 26 <= self.pm2[-1] <= 50:
            self.status.setText('나쁨')  # '나쁨' 출력
            self.imgstatus.setPixmap(
                QPixmap("finedust\\bad.png").scaled(50, 50))  # 현재상태 나쁨 사진으로 교체

        # 만약 pm10 농도가 101이상이거나 pm2 농도가 51이상일 때
        if 101 <= self.pm10[-1] or 51 <= self.pm2[-1]:
            self.status.setText('매우 나쁨')  # "매우 나쁨" 출력
            self.imgstatus.setPixmap(
                QPixmap("finedust\\worst.png").scaled(50, 50))  # 현재상태 매우 나쁨 사진으로 교체

        self.dynamic_ax.plot(self.createdtime, self.pm1,
                             color='limegreen', label='pm1', marker=".")  # pm1 graph 생성 (x축은 시간, y축은 pm1 농도 데이터, 그래프 생성 데이터에는 .으로 표시, 색은 limegreen)
        self.dynamic_ax.plot(self.createdtime, self.pm2,
                             color='violet', label='pm2.5', marker=".")  # pm2.5 graph 생성 (x축은 시간, y축은 pm2.5 농도 데이터, 그래프 생성 데이터에는 .으로 표시, 색은 violet)
        self.dynamic_ax.plot(self.createdtime, self.pm10,
                             color='dodgerblue', label='pm10', marker=".")  # pm10 graph 생성 (x축은 시간, y축은 pm10 농도 데이터, 그래프 생성 데이터에는 .으로 표시, 색은 dodgerblue)
        self.dynamic_ax.legend(
            loc=(0, 1), ncol=3, fontsize=10, frameon=True, shadow=True)  # 범례 생성(그래프 위치, 표시 그래프, 범례 font size, 프레임 효과, 그림자 효과)
        # x축 이름을 '시간'으로 설정, font는 변수 fontprop에서 가져옴(noto sans)
        self.dynamic_ax.set_xlabel('시간', fontproperties=fontprop)
        # y축 이름을 '㎍/㎥'으로 설정, font는 변수 fontprop에서 가져옴(noto sans)
        self.dynamic_ax.set_ylabel('㎍/㎥', fontproperties=fontprop)
        self.dynamic_ax.grid(True, axis='y')  # 그래프에서 y축 방향으로 그리드 생성
        self.dynamic_ax.figure.canvas.draw()  # 그래프 생성


# py파일은 하나의 module 형태로 만들어진다 -> 어느 파일에서 import하는지에 따라서 __name__ 값이 달라진다.
if __name__ == '__main__':
    # 즉 자기가 직접 실행하기 위해서 필요한 구문
    app = QApplication(sys.argv)
    ex = MyApp()  # 생성자의 self는 ex를 전달받게 된다

    id = QFontDatabase.addApplicationFont("Noto_Sans_KR\\NotoSansKR-Bold.otf")
    _fontstr = QFontDatabase.applicationFontFamilies(id)[0]
    _font = QFont(_fontstr)
    app.setFont(_font)

    # app 객체를 실행시키고, system의 x버튼을 누르면 실행되고 있는 App를 종료시켜준다
    sys.exit(app.exec_())
