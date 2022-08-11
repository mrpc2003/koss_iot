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
