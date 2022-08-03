#include "DHT.h"//DHT11 라이브러리 추가

DHT dht(D3, DHT11);// D3번 핀에 연결된 DHT11센서를 dht라는 객체로 생성

void setup() {
  Serial.begin(115200);//시리얼 통신 시작
  Serial.println("Start sensor");
  dht.begin();//dht센서 가동
}

void loop() {
  float t = dht.readTemperature();//섭씨 온도 가져오기(dht.readTemperature(true) -> 화씨 온도)
  float h = dht.readHumidity();//습도 가져오기

  Serial.print("Temperature: ");
  Serial.print(t);
  Serial.print("C\t");
  Serial.print("Humidity: ");
  Serial.print(h);
  Serial.println("%"); //센서 값 출력하기
  delay(1000); // 1초(1000ms) 주기
}
