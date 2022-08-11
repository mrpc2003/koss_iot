const mongoose = require("mongoose"); // mongoose 모듈 불러오기
const SensorsSchema = mongoose.Schema({ // 설정한 스키마 정의
  tmp: { 
    type: String,
    required: true, 
  }, // 온도
  hum: {
    type: String,
    required: true,
  }, // 습도
  pm1: {
    type: String,
    require: true,
  }, // pm1
  pm2: {
    type: String,
    require: true,
  }, // pm2.5
  pm10: {
    type: String,
    require: true,
  }, // pm10
  created_at: {
    type: Date,
    default: Date.now,
  }, // 생성 시간
});
module.exports = mongoose.model("Sensors", SensorsSchema); // 모델 내보내기
