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
