#include <SoftwareSerial.h> // SoftwareSerial을 사용하기 위한 라이브러리
#include "PMS.h" // PMS센서를 사용하기 위한 라이브러리
SoftwareSerial Serial_PMS(D6, D7); // 시리얼 이름(Tx, Rx)
PMS pms(Serial_PMS); // 사용할 센서 이름(시리얼)
PMS::DATA data; // 데이터를 받아올 객체

void setup() {
 Serial.begin(115200); // 시리얼 통신 시작
 Serial_PMS.begin(9600); // 소프트웨어 시리얼 통신 시작
}

void loop() {
  if(pms.read(data))// 만약 PMS센서에서 받은 값이 존재한다면
  {
    //받은 3종류의 미세먼지 센서 값을 정수로 저장해주고
    int pm1 = data.PM_AE_UG_1_0;
    int pm25 = data.PM_AE_UG_2_5;
    int pm10 = data.PM_AE_UG_10_0;
    
    char message[64]=""; 
    sprintf(message, "{\"pm1\":%d,\"pm25\":%d,\"pm10\":%d}", pm1, pm25, pm10); // message에 JSON 문자열 형식으로 표현
    
    Serial.println(message); // message 출력
    delay(3000); // 3초
  }
}
