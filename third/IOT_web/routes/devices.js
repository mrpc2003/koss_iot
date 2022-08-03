var express = require("express");
var router = express.Router();
const mqtt = require("mqtt");
const Sensors = require("../models/sensors");
// MQTT Server 접속
const client = mqtt.connect("mqtt://172.20.10.12"); // 라즈베리파이 url
//웹에서 rest-full 요청받는 부분(POST) web - > ras pi -> arduino -> led control
router.post("/led", function (req, res, next) {
  res.set("Content-Type", "text/json");
  if (req.body.flag == "on") {
    // MQTT->led : 1
    client.publish("led", "1");
    res.send(JSON.stringify({ led: "on" }));
  } else {
    client.publish("led", "2");
    res.send(JSON.stringify({ led: "off" }));
  }
});
module.exports = router;
