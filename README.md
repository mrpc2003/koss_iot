# koss_iot

- koss iot 특강
  - 3주차 과제
    - 코드 설명
    
    third\IOT_web내의 각 코드 파일에 line 별로 주석 설명을 하였습니다

    
    - 작동 영상
    
    https://user-images.githubusercontent.com/74747291/184285611-c67d4a21-e0c2-4578-b1e7-dd1a721ead90.mp4
    
    https://user-images.githubusercontent.com/74747291/184285623-1a84cb06-d4c8-4aa6-8b80-33bee98c09dc.mp4


  - 4주차 과제
    - 코드 설명
    
    4주차 과제.py 내에 line 별로 주석 설명을 하였습니다
     
    - 작동 영상
    
    https://user-images.githubusercontent.com/74747291/184285598-1d753f9e-ef82-4ea0-b223-08b1fd65c3c5.mp4


___
***
___

# 3주차 과제 중 app.js 코드 설명
``` C
const express = require("express"); // express 모듈 불러오기
const app = express(); // express 서버 생성
const path = require("path"); // path 모듈 불러오기
const bodyParser = require("body-parser"); // body-parser 모듈 불러오기
const mqtt = require("mqtt"); // mqtt 모듈 불러오기
const http = require("http"); // http 모듈 불러오기
const mongoose = require("mongoose"); // mongoose 모듈 불러오기
const Sensors = require("./models/sensors"); // 센서 모델 불러오기
const devicesRouter = require("./routes/devices"); // 디바이스 라우터 불러오기
require("dotenv/config"); // .env 파일 불러오기

app.use(express.static(__dirname + "/public")); // public 폴더를 static으로 사용
app.use(bodyParser.json()); // body-parser 사용
app.use(bodyParser.urlencoded({ extended: false })); // body-parser 사용
app.use("/devices", devicesRouter); // 라우터 사용

//MQTT접속 하기
const client = mqtt.connect("mqtt://192.168.1.48"); // 라즈베리파이 url 입력 (서버 주소)
client.on("connect", () => {
  // 접속 성공시 실행
  console.log("mqtt connect"); // 콘솔에 접속 성공 메시지 출력
  client.subscribe("sensors"); // 센서 정보 수신 시작
});

client.on("message", async (topic, message) => {
  // 센서 정보 수신 시 실행
  var obj = JSON.parse(message); // 센서 정보를 JSON 형식으로 변환
  var date = new Date(); // 현재 시간 가져오기
  var year = date.getFullYear(); // 현재 년도 가져오기
  var month = date.getMonth(); // 현재 월 가져오기
  var today = date.getDate(); // 현재 일 가져오기
  var hours = date.getHours(); // 현재 시간 가져오기
  var minutes = date.getMinutes(); // 현재 분 가져오기
  var seconds = date.getSeconds(); // 현재 초 가져오기
  obj.created_at = new Date( // 센서 정보에 시간 정보 추가
    Date.UTC(year, month, today, hours, minutes, seconds) // 시간 정보 설정
  );

  const sensors = new Sensors({
    // 센서 정보를 저장할 모델 생성
    tmp: obj.tmp, // 센서 정보에 온도 정보 추가
    hum: obj.humi, // 센서 정보에 습도 정보 추가
    pm1: obj.pm1, // 센서 정보에 PM1 정보 추가
    pm2: obj.pm25, // 센서 정보에 PM2.5 정보 추가
    pm10: obj.pm10, // 센서 정보에 PM10 정보 추가
    created_at: obj.created_at, // 센서 정보에 시간 정보 추가
  });

  try {
    // 센서 정보 저장 시도
    const saveSensors = await sensors.save(); // 센서 정보 저장
    console.log("insert OK"); // 콘솔에 센서 정보 저장 성공 메시지 출력
  } catch (err) {
    // 센서 정보 저장 실패시
    console.log({ message: err }); // 콘솔에 센서 정보 저장 실패 메시지 출력
  }
});
app.set("port", "3000"); // 포트 설정
var server = http.createServer(app); // 서버 생성
var io = require("socket.io")(server); // 소켓 서버 생성
io.on("connection", (socket) => {
  // 소켓 연결 시 실행
  //웹에서 소켓을 이용한 sensors 센서데이터 모니터링
  socket.on("socket_evt_mqtt", function (data) {
    // 소켓 이벤트 시 실행
    Sensors.find({}) // 센서 정보 조회
      .sort({ _id: -1 }) // 최신 정보부터 조회
      .limit(1) // 최신 1개 조회
      .then((data) => {
        // 센서 정보 조회 성공시
        socket.emit("socket_evt_mqtt", JSON.stringify(data[0])); // 소켓 이벤트 전송
      });
  });
  //웹에서 소켓을 이용한 LED ON/OFF 제어하기
  socket.on("socket_evt_led", (data) => {
    // 소켓 이벤트 시 실행
    var obj = JSON.parse(data); // 소켓 이벤트 데이터를 JSON 형식으로 변환
    client.publish("led", obj.led + ""); // LED 제어 소켓 전송
  });
});

//웹서버 구동 및 DATABASE 구동
server.listen(3000, (err) => {
  // 웹 서버 구동
  if (err) {
    // 웹 서버 구동 실패시
    return console.log(err); // 콘솔에 웹 서버 구동 실패 메시지 출력
  } else {
    // 웹 서버 구동 성공시
    console.log("server ready"); // 콘솔에 웹 서버 구동 성공 메시지 출력
    //Connection To DB
    mongoose.connect(
      // DB 연결
      process.env.MONGODB_URL, // DB 연결 주소
      { useNewUrlParser: true, useUnifiedTopology: true }, // DB 연결 옵션
      () => console.log("connected to DB!") // DB 연결 성공시 콘솔에 연결 메시지 출력
    );
  }
});
```

# 3주차 과제 중 MQTT.HTML 코드 설명
``` C
<!DOCTYPE html>
<!--html로 작성-->
<html>
  <!--html 시작-->
  <head>
    <!--head 시작-->
    <meta charset="utf-8" />
    <!--유니코드 사용-->
    <title>iot test</title>
    <!--웹 페이지 제목 -> iot test로 설정-->
    <!--bootstrap를 사용하기 위한 테마 설정-->
    <link
      rel="stylesheet"
      href="https://cdn.jsdelivr.net/npm/bootswatch@4.5.2/dist/sketchy/bootstrap.min.css"
      integrity="sha384-RxqHG2ilm4r6aFRpGmBbGTjsqwfqHOKy1ArsMhHusnRO47jcGqpIQqlQK/kmGy9R"
      crossorigin="anonymous"
    />
    <!--google font -> font 설정 -->
    <link rel="preconnect" href="https://fonts.googleapis.com" />
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
    <link
      href="https://fonts.googleapis.com/css2?family=Dongle:wght@300&family=Inter&display=swap"
      rel="stylesheet"
    />

    <script type="text/javascript" src="/socket.io/socket.io.js"></script>
    <!--socket.io 사용-->
    <script src="http://code.jquery.com/jquery-3.3.1.min.js"></script>
    <!--jquery 사용-->

    <!--javascript 시작-->
    <script type="text/javascript">
      var socket = null; //socket 선언 및 초기화
      $; //jquery 선언 및 초기화
      var timer = null; //timer 선언 및 초기화
      $(document).ready(function () { //jquery 시작 부분 -> 웹 페이지가 준비되면 실행됨
        socket = io.connect(); // 3000port 연결 후 socket에 저장
        // Node.js보낸 데이터를 수신하는 부분
        socket.on("socket_evt_mqtt", function (data) { //socket_evt_mqtt 이벤트 수신
          data = JSON.parse(data); //json 형식으로 변환 후 data에 저장
          console.log(data); //data 출력
          $(".mqttlist").html( //mqttlist 에 html 출력
            "<li>" +
              " tmp: " +
              data.tmp +
              "°C" + //온도 값 출력
              " hum: " +
              data.hum +
              "%" + //습도 값 출력
              " pm1: " +
              data.pm1 +  //pm1 값 출력
              " pm2.5: " +
              data.pm2 + //pm2.5 값 출력
              " pm10: " +
              data.pm10 + //pm10 값 출력
              "</li>"
          );
        });
        if (timer == null) { //timer가 null이면
          timer = window.setInterval("timer1()", 1000);  //1초마다 timer1 함수 실행
        }
      });

      function timer1() {   //timer1 함수 시작
        socket.emit("socket_evt_mqtt", JSON.stringify({})); //socket_evt_mqtt 이벤트 송신
        console.log("---------"); //콘솔 출력
      }

      function ledOnOff(value) { //ledOnOff 함수 시작
        // {"led":1}, {"led":2}
        socket.emit("socket_evt_led", JSON.stringify({ led: Number(value) })); //socket_evt_led 이벤트 송신
      }

      // ajax = Asynchronous JavaScript and XML
      function ajaxledOnOff(value) { //ajaxledOnOff 함수 시작
        if (value == "1") var value = "on"; //value가 1이면 on으로 설정
        else if (value == "2") var value = "off"; //value가 2이면 off으로 설정
        $.ajax({ //ajax 시작
          url: "http://localhost:3000/devices/led", //local url 설정
          type: "post", //post 설정
          data: { flag: value }, //flag에 value 설정
          success: ledStatus, //ledStatus 함수 실행
          error: function (request, status, error) { //에러 시 실행
            alert( //알림창 출력
              "code:" +
                request.status + //에러 코드 출력
                "\n" +  //줄바꿈
                "message:" +
                request.responseText + //에러 메세지 출력
                "\n" + //줄바꿈
                "error:" +
                error //에러 출력
            );
          },
        });
      }

      function ledStatus(obj) { //ledStatus 함수 시작
        $("#led").html("<font color='red'>" + obj.led + "</font> 되었습니다."); //led 출력
      }
    </script>
  </head>
  <body>
    <h2
      style="
        background: linear-gradient(
          to right,
          #a7a3ff,
          #ffa7a3,
          #671cc4,
          #5673bd
        );
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-family: 'Dongle', sans-serif;
        text-align: center;
      "
    >
      socket 이용한 센서 모니터링 서비스
    </h2>
    <div id="msg">
      <div id="mqtt_logs">
        <ul class="mqttlist"></ul>
        <br />
      </div>

      <h2
        style="
          border-bottom: 1px solid #688ff4;
          padding: 0.1em;
          border-top: 1px solid #688ff4;
          padding: 0.1em;
          font-family: 'Dongle', sans-serif;
          text-align: center;
        "
      >
        socket 통신 방식(LED제어)
      </h2>
      <!-- <button onclick="ledOnOff(1)">LED_ON</button> -->
      <button
        onclick="ledOnOff(1)"
        type="button"
        class="btn btn-danger"
        control-id="ControlID-50"
      >
        LED_ON
      </button>

      <!-- <button onclick="ledOnOff(2)">LED_OFF</button> -->
      <button
        onclick="ledOnOff(2)"
        type="button"
        class="btn btn-success"
        control-id="ControlID-47"
      >
        LED_OFF
      </button>

      <h2
        style="
          border-bottom: 1px solid #688ff4;
          padding: 0.1em;
          border-top: 1px solid #688ff4;
          padding: 0.1em;
          font-family: 'Dongle', sans-serif;
          text-align: center;
        "
      >
        RESTfull Service 통신 방식(LED제어)
      </h2>
      <!-- <button onclick="ajaxledOnOff(1)">LED_ON</button> -->
      <button
        onclick="ajaxledOnOff(1)"
        type="button"
        class="btn btn-danger"
        control-id="ControlID-50"
      >
        LED_ON
      </button>

      <!-- <button onclick="ajaxledOnOff(2)">LED_OFF</button> -->
      <button
        onclick="ajaxledOnOff(2)"
        type="button"
        class="btn btn-success"
        control-id="ControlID-47"
      >
        LED_OFF
      </button>
      <div
        id="led"
        style="
          border-bottom: 1px solid #688ff4;
          padding: 0.1em;
          border-top: 1px solid #688ff4;
          padding: 0.1em;
          font-family: 'Dongle', sans-serif;
          font-size: larger;
          text-align: center;
        "
      >
        LED STATUS
      </div>
    </div>
  </body>
  <!-- body 종료 -->
</html>
<!-- html 종료 -->
```

# 3주차 과제 중 devices.js 코드 설명
``` C
var express = require("express"); // express 모듈 불러오기
var router = express.Router(); // express 라우터 모듈 불러오기
const mqtt = require("mqtt"); // mqtt 모듈 불러오기
const Sensors = require("../models/sensors"); // 센서 모델 불러오기
// MQTT Server 접속 설정
const client = mqtt.connect("mqtt://192.168.1.48"); // 라즈베리파이 url 입력 (서버 주소)
//웹에서 rest-full 요청받는 부분(POST) web - > ras pi -> arduino -> led control
router.post("/led", function (req, res, next) {
  // led 제어 함수
  res.set("Content-Type", "text/json"); // 응답 타입 설정
  if (req.body.flag == "on") {
    // MQTT->led : 1
    client.publish("led", "1"); // LED ON 전송
    res.send(JSON.stringify({ led: "on" })); //웹에서 전송받은 데이터를 다시 전송
  } else {
    // MQTT->led : 2

    client.publish("led", "2"); // LED OFF 전송
    res.send(JSON.stringify({ led: "off" })); //웹에서 전송받은 데이터를 다시 전송
  }
});
module.exports = router; // 모듈 내보내기
```


# 4주차 과제 코드 설명


``` C
import sys  # python의 interpreter를 제어할 수 있는 방법을 제공
# matplotlib의 graph에서 font를 설정하기 위한 font manager import
import matplotlib.font_manager as fm  # font manager import
from PyQt5.QtCore import Qt  # PyQt5의 QtCore를 import
from PyQt5.QtGui import QFont, QPixmap, QFontDatabase  # PyQt5의 QtGui를 import
# PyQt5의 QtWidgets를 import
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QHBoxLayout, QVBoxLayout, QMainWindow
# matplotlib의 FigureCanvasQTAgg를 import
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure  # matplotlib의 Figure를 import
from pymongo import MongoClient  # Python에서 mongoDB를 이용하기 위한 라이브러리로 pymongo를 사용
# mongoDB의 내 데이터베이스 주소를 입력
client = MongoClient(
    "mongodb+srv://mrpc2003:rainb0w12@Cluster0.yxiwiyk.mongodb.net/?retryWrites=true&w=majority")

db = client['test']  # 'test' 이름의 데이터 베이스를 db변수로 지정
collection = db['sensors']  # 'sensors' 이름의 collections를 collection 변수로 지정


class MyApp(QMainWindow):  # MyApp 클래스를 만드는데 QMainWindow 클래스를 상속받는다

    def __init__(self):  # 파이썬의 생성자명은 __init__ 고정이므로 첫번째 고정값은 self -> instance 이름을 self로 지정
        super().__init__()  # 다른 class의 속성 및 method를 자동으로 불러와 해당 class에서도 사용이 가능하도록 함

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
        # 생성할 창의 위치 (왼쪽에서 떨어진 값, 위쪽에서 떨어진 값, 창의 크기 가로, 창의 크기 세로)
        self.setGeometry(300, 100, 600, 600)
        self.show()  # 창 보여주기

    def update_canvas(self):  # graph 업데이트 함수 작성
        path = 'Noto_Sans_KR\\NotoSansKR-Regular.otf'  # font path 설정
        # graph에 표시되는 font와 size 설정
        fontprop = fm.FontProperties(fname=path, size=18)

        self.dynamic_ax.clear()  # graph 화면 초기화
        # mongoDB에서 id값을 기준으로 최신순 정렬을 하여 변수 d에 1개만 저장
        d = collection.find().sort('_id', -1).limit(1)
        for i in d:  # 변수 d에 위치한 데이터를 i로 보냄
            # created_at에 해당하는 데이터를 임시 변수 createdtime에 저장
            createdtime = str(i['created_at'])
            # 년-월-일-시-분-초 데이터에서 시-분-초 데이터만 가져오도록 슬라이싱
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
            loc=(0, 1), ncol=3, fontsize=10, frameon=True, shadow=True)  # 그래프에 범례 생성 (위치는 (0,1), 열은 3, 폰트크기는 10, 프레임은 True, 쉐도우는 True)
        # x축 이름을 '시간'으로 설정, font는 변수 fontprop에서 가져옴(noto sans)
        self.dynamic_ax.set_xlabel('시간', fontproperties=fontprop)
        # y축 이름을 '㎍/㎥'으로 설정, font는 변수 fontprop에서 가져옴(noto sans)
        self.dynamic_ax.set_ylabel('㎍/㎥', fontproperties=fontprop)
        self.dynamic_ax.grid(True, axis='y')  # 그래프에서 y축 방향으로 그리드 생성
        self.dynamic_ax.figure.canvas.draw()  # 그래프 그리기


# py파일은 하나의 module 형태로 만들어진다 -> 어느 파일에서 import하는지에 따라서 __name__ 값이 달라진다.
if __name__ == '__main__':
    # 즉 자기가 직접 실행하기 위해서 필요한 구문
    app = QApplication(sys.argv)  # QApplication 객체 생성
    ex = MyApp()  # 생성자의 self는 ex를 전달받게 된다

    id = QFontDatabase.addApplicationFont(
        "Noto_Sans_KR\\NotoSansKR-Bold.otf")  # noto-sans font를 등록하고 id를 반환받는다
    _fontstr = QFontDatabase.applicationFontFamilies(
        id)[0]  # 전달받은 id에 해당하는 font를 가져옴
    _font = QFont(_fontstr)  # 변수 _font에 noto-sans의 font id값 지정
    app.setFont(_font)  # app의 font 설정

    # app 객체를 실행시키고, system의 x버튼을 누르면 실행되고 있는 App를 종료시켜준다
    sys.exit(app.exec_())
```
