#include <ESP8266WiFi.h>
#define LED1 D1
#define LED2 D2
#define LED3 D5
#define LED4 D6

// el programa funciona per relés en filera el HIGH és tancat
//i el LOW és obert

const char* ssid = "MOVISTAR_F7EF";
const char* password = "9EF1BF58B87A61B433ED";
unsigned char status_led=0;
WiFiServer server(80);

void setup() {
  Serial.begin(115200);
  WiFi.setSleepMode(WIFI_NONE_SLEEP);
  pinMode(LED1, OUTPUT); //reg 1
  pinMode(LED2, OUTPUT); //neutre
  pinMode(LED3, OUTPUT); //reg 2
  pinMode(LED4, OUTPUT); //reg3

  digitalWrite(LED1, HIGH);
  digitalWrite(LED2, HIGH);
  digitalWrite(LED3, HIGH);
  digitalWrite(LED4, HIGH);

 
  WiFi.begin(ssid, password);
  server.begin();
}

void loop() {
  WiFiClient client = server.available();
  if (client) {
    String req = client.readStringUntil('\r');
  client.flush();
  if(req.indexOf("/regun") != -1)
  {
    status_led=1;
    digitalWrite(LED1,LOW);
    digitalWrite(LED2,LOW);
    delay(10000);
    digitalWrite(LED1, HIGH);
    digitalWrite(LED2, HIGH);
    delay(1000);
    digitalWrite(LED4, LOW);
    digitalWrite(LED2,LOW);
    delay(10000);
    digitalWrite(LED4, HIGH);
    digitalWrite(LED2, HIGH);
    delay(1000);
    //inhabilitar reg 3
    
  }
  else if(req.indexOf("/regdos") != -1)
  {
    status_led=1; 
    // modificat el Led3pel Led4 tenir-ho en compte
    digitalWrite(LED3, LOW);
    digitalWrite(LED2, LOW);
    delay(10000);
    digitalWrite(LED3,HIGH);
    digitalWrite(LED2, HIGH);
    delay(1000);   
  }
  client.stop();
  }
}
  
  
  
  
