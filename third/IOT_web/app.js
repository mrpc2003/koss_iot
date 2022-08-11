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
const client = mqtt.connect("mqtt://192.168.1.48"); // 라즈베리파이 url
client.on("connect", () => {
  // 접속 성공시
  console.log("mqtt connect"); // 콘솔에 접속 성공 메시지 출력
  client.subscribe("sensors"); // 센서 정보 수신 시작
});

client.on("message", async (topic, message) => {
  // 센서 정보 수신 시
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
  // console.log(obj);

  const sensors = new Sensors({
    tmp: obj.tmp,
    hum: obj.humi,
    pm1: obj.pm1,
    pm2: obj.pm25,
    pm10: obj.pm10,
    created_at: obj.created_at,
  });

  try {
    const saveSensors = await sensors.save();
    console.log("insert OK");
  } catch (err) {
    console.log({ message: err });
  }
});
app.set("port", "3000");
var server = http.createServer(app);
var io = require("socket.io")(server);
io.on("connection", (socket) => {
  //웹에서 소켓을 이용한 sensors 센서데이터 모니터링
  socket.on("socket_evt_mqtt", function (data) {
    Sensors.find({})
      .sort({ _id: -1 })
      .limit(1)
      .then((data) => {
        //console.log(JSON.stringify(data[0]));
        socket.emit("socket_evt_mqtt", JSON.stringify(data[0]));
      });
  });
  //웹에서 소켓을 이용한 LED ON/OFF 제어하기
  socket.on("socket_evt_led", (data) => {
    var obj = JSON.parse(data);
    client.publish("led", obj.led + "");
  });
});

//웹서버 구동 및 DATABASE 구동
server.listen(3000, (err) => {
  if (err) {
    return console.log(err);
  } else {
    console.log("server ready");
    //Connection To DB
    mongoose.connect(
      process.env.MONGODB_URL,
      { useNewUrlParser: true, useUnifiedTopology: true },
      () => console.log("connected to DB!")
    );
  }
});
