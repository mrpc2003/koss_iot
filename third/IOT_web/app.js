const express = require("express");
const app = express();
const path = require("path");
const bodyParser = require("body-parser");
const mqtt = require("mqtt");
const http = require("http");
const mongoose = require("mongoose");
const Sensors = require("./models/sensors");
const devicesRouter = require("./routes/devices");
require("dotenv/config");

app.use(express.static(__dirname + "/public"));
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: false }));
app.use("/devices", devicesRouter);

//MQTT접속 하기
const client = mqtt.connect("mqtt://192.168.1.48"); // 라즈베리파이 url
client.on("connect", () => {
  console.log("mqtt connect");
  client.subscribe("sensors");
});

client.on("message", async (topic, message) => {
  var obj = JSON.parse(message);
  var date = new Date();
  var year = date.getFullYear();
  var month = date.getMonth();
  var today = date.getDate();
  var hours = date.getHours();
  var minutes = date.getMinutes();
  var seconds = date.getSeconds();
  obj.created_at = new Date(
    Date.UTC(year, month, today, hours, minutes, seconds)
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
