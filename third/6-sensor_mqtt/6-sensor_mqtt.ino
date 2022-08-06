#include <ESP8266WiFi.h> // Wifi 라이브러리 추가
#include <PubSubClient.h> // MQTT client 라이브러리 
#include <Wire.h> //I2C 통신을 위한 라이브러리
#include <Adafruit_Sensor.h> // BME280(온습도)
#include <Adafruit_BME280.h> // BME280(온습도)
#include <SoftwareSerial.h> // SoftwareSerial 통신을 위한 라이브러리
#include "PMS.h" // PMS7003m(미세먼지)

SoftwareSerial Serial_PMS(D6, D7); //Tx, Rx
PMS pms(Serial_PMS); // 사용할 센서 이름(연결된 시리얼)
PMS::DATA data; // 데이터를 받아올 객체

Adafruit_BME280 bme; // I2C
int led_pin = D5; //led 핀 설정

const char* ssid = "507-701"; //사용하는 Wifi 이름
const char* password = "01067372666"; // 비밀번호
const char* mqtt_server = "192.168.1.48"; //mqtt 서버 주소(라즈베리파이에서 ifconfig로 inet 주소 확인)**꼭 수정!!!!!!!!!!!!!
const char* clientName = "pi"; // client 이름(생일 추천드려요~)

WiFiClient espClient; // 인터넷과 연결할 수 있는 client 생성
PubSubClient client(espClient); // 해당 client를 mqtt client로 사용할 수 있도록 설정

//Wifi 연결
void setup_wifi() {
   delay(10);
   Serial.println();
   Serial.print("Connecting to ");
   Serial.println(ssid);
   WiFi.mode(WIFI_STA);
   WiFi.begin(ssid, password);
   while(WiFi.status() != WL_CONNECTED)
   {
     delay(500);
     Serial.print(".");
   }
   Serial.println("");
   Serial.println("WiFi connected");
   Serial.println("IP address: ");
   Serial.println(WiFi.localIP()); 
}

//메시지가 들어왔을 때 처리하는 callback 함수
void callback(char* topic, byte* payload, unsigned int uLen) {
  char pBuffer[uLen+1];
  int i;
  for(i = 0; i < uLen; i++)
  {
    pBuffer[i]=(char)payload[i];
  }
  Serial.println(pBuffer); // 1 or 2
  if(pBuffer[0]=='1')
  {
    digitalWrite(led_pin, HIGH); // 1이면 led 켜기
  }
  else if(pBuffer[0]=='2')
  {
    digitalWrite(led_pin, LOW); // 2면 led 끄기
  } 
}

//mqtt 연결
void reconnect() {
  //연결될 때까지 시도
  while (!client.connected())
  {
    Serial.print("Attempting MQTT connection...");
    if (client.connect(clientName))
    {
      //연결 성공
      Serial.println("connected");
      client.subscribe("led"); // led 토픽 구독
    } 
    else 
    {
      //연결실패하면 현재 상태 출력하고 5초 후 다시 시도
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      delay(5000);
    }
  }
}

void setup() {
  pinMode(led_pin, OUTPUT);
  Serial.begin(115200); // 시리얼 통신 시작
  Serial_PMS.begin(9600); // 소프트웨어 시리얼 통신 시작
  Serial.println("Start sensor");
  bme.begin();  //bme센서 가동
  setup_wifi(); //Wifi 연결
  client.setServer(mqtt_server, 1883); //mqtt 서버와 연결(ip, 1883)
  client.setCallback(callback); //callback 함수 세팅
}

void loop() {
  if (!client.connected())
  {
    reconnect(); //mqtt 연결이 안되어있다면 다시 연결
  }
  client.loop(); //연결을 계속해서 유지하고 들어오는 메시지를 확인할 수 있도록 함

  if(pms.read(data)) // 만약 PMS센서에서 받은 값이 존재한다면
  {
    float t = bme.readTemperature(); //섭씨 온도 가져오기
    float h = bme.readHumidity(); //습도 가져오기

    //받은 3종류의 미세먼지 센서 값을 정수로 저장
    int pm1 = data.PM_AE_UG_1_0;  
    int pm25 = data.PM_AE_UG_2_5;
    int pm10 = data.PM_AE_UG_10_0;
  
    char message[70] = ""; // 문자열을 위한 공간 마련
    sprintf(message, "{\"tmp\":%.2f,\"humi\":%.2f,\"pm1\":%d,\"pm25\":%d,\"pm10\":%d}", t, h, pm1, pm25, pm10); //JSON 문자열의 형식으로 온도, 습도, 미세먼지 데이터 담기

    Serial.print("Publish message: ");
    Serial.println(message);
    client.publish("sensors", message); // 만든 문자열을 mqtt 서버에 publish
  
    delay(1000); // 1초(1000ms) 주기 
  }
}
