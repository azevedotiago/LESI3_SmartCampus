/*
  
  Project: Smart Energy Campus");
  Year: 2022 / 2023");
        LESI @ IPCA");
  Authors: 2727 Nuno Mendes");
           Tiago Azevedo");
           Francisco Pereira");
           Rosario Silva");

*/

#include "WiFiEsp.h"


//#ifndef HAVE_HWSERIAL1
#include "SoftwareSerial.h"
SoftwareSerial softserial(4, 5);  // RX, TX
//#endif
// network info variables
byte mac[6];
IPAddress ip;

//char ssid[] = "smartenergy";   // your network SSID (name)
//char pass[] = "20222023lesi";  // your network password

char ssid[] = "digitalchip";   // your network SSID (name)
char pass[] = "A253311201";  // your network password

int status = WL_IDLE_STATUS;
int reqCount = 0;  // number of requests received

#define LED 6 // pino do LED, porta PWM
#define LDR 0 // pino de input do sensor de luz
#define PIR 3 // pino de input do sensor de movimento
#define LEDWIFION 10  // wireless conetado e a funcionar
#define LEDWIFIOFF 11 // wireless nao conetado
#define MAXLED 32
#define LDRmax 1000
#define LDRmin 40
#define LDRmed 600    // 600 para efeitos de testes dentro de casa
#define TIMEmax 10 // tempo maximo LEDs ligados
#define valLEDmin 2 // valor dos LEDs quando ligados mas sem movimentom, em standby 

int valLED = 0;
int valLDR = 0;
int valPIR = 0; 
int statePIR = LOW;  // sem deteção de movimento
uint32_t timer = 0;     // temporizador para o tempo dos LEDs ligados 
uint32_t timer2 = 0;

WiFiEspServer server(80);

void info() {
  Serial.println("\n\nSmart Energy Campus @ IPCA 2022/2023\n");
}

void test() {
  Serial.println("\n[Testing]");
  delay(1000);

  Serial.print("\n- Ilumination...");
  // aumentar o brilho
  Serial.print("\n Bright up ");
  for(int i=0; i<=255; i++) {
    if ((i % 2) == 0) Serial.print("+");
    analogWrite(LED, i);
    delay(10);
  }
  // reduzir o brilho
  Serial.print("\n Bright down ");
  for(int i=255; i>=0; i--){
    if ((i % 2) == 0) Serial.print("-");
    analogWrite(LED, i);
    delay(10);
  }
  analogWrite(LED, 0);

  Serial.print("\n\n- Light Sensor LDR... "); 
  for(int i=0; i<=255; i++) {
    if ((i % 30) == 0) Serial.print("\n");
    valLDR = analogRead(LDR);
    Serial.print(" ");
    Serial.print(valLDR);
    delay(10);
  }
  valLDR = 0;


  Serial.print("\n\n- Motion Sensor PIR... "); 
  for(int i=0; i<=255; i++) {
    if ((i % 60) == 0) Serial.print("\n");
    valPIR = digitalRead(PIR);
    Serial.print(" ");
    Serial.print(valPIR);
    delay(10);
    //if (i == 255) i=0;
  }
  valPIR = LOW;

  Serial.print("\n\n- Network LEDs... "); 
  for(int i=0; i<=10; i++) {
    analogWrite(LEDWIFION, 0);
    analogWrite(LEDWIFIOFF, MAXLED);
    delay(100);
    analogWrite(LEDWIFION, MAXLED);
    analogWrite(LEDWIFIOFF, 0);
    delay(100);
  }
  analogWrite(LEDWIFION, 0);
  analogWrite(LEDWIFIOFF, 0);

  Serial.println("\n");
}


void setup() {
  pinMode(LED, OUTPUT);
  pinMode(LEDWIFION, OUTPUT);
  pinMode(LEDWIFIOFF, OUTPUT);
  pinMode(LDR, INPUT);
  pinMode(PIR, INPUT);
  analogWrite(LED, 0); // Desliga os LEDs
  analogWrite(LEDWIFION, 0);
  analogWrite(LEDWIFIOFF, MAXLED);


  // initialize serial for debugging
  Serial.begin(9600);

  // Info do projeto
  info();

  // Testando os componentes externos
  test();

  // initialize serial for ESP module
  analogWrite(LEDWIFIOFF, MAXLED);
  Serial.println("\n[Network connection]");
  softserial.begin(115200);
  softserial.write("AT+CIOBAUD=9600\r\n");
  softserial.write("AT+RST\r\n");
  softserial.begin(9600);
  // initialize ESP module
  WiFi.init(&softserial);

  // check for the presence of the shield
  if (WiFi.status() == WL_NO_SHIELD) {
    Serial.println("WiFi shield not present");
    // don't continue
    while (true)
      ;
  }

  // attempt to connect to WiFi network
  while (status != WL_CONNECTED) {
    analogWrite(LED, 255);
    analogWrite(LEDWIFION, MAXLED);
    analogWrite(LEDWIFIOFF, 0);
    delay(100);
    analogWrite(LED, 64);
    analogWrite(LEDWIFION, 0);
    analogWrite(LEDWIFIOFF, MAXLED);
    delay(100);
    analogWrite(LED, 255);
    analogWrite(LEDWIFION, MAXLED);
    analogWrite(LEDWIFIOFF, 0);
    delay(100);
    analogWrite(LED, 64);
    analogWrite(LEDWIFION, 0);
    analogWrite(LEDWIFIOFF, MAXLED);
    delay(100);

    Serial.print("Attempting to connect to WPA SSID: ");
    Serial.println(ssid);
    // Connect to WPA/WPA2 network
    status = WiFi.begin(ssid, pass);
    analogWrite(LED, 0);
  }

  Serial.println("You're connected to the network");
  printWifiStatus();
  analogWrite(LEDWIFION, MAXLED);
  analogWrite(LEDWIFIOFF, 0);

  // start the web server on port 80
  server.begin();
}

void inputs() {
  valLDR = analogRead(LDR);
  valPIR = digitalRead(PIR);
  if (valPIR == HIGH) statePIR = HIGH;
}

void outputs() {

  // LDRmax - sem sol, escuro
  // LDRmin - muito sol
  if (valLDR <= LDRmin ) valLDR=LDRmin;
  if (valLDR >= LDRmax) valLDR=LDRmax;
  long valLDRnew = (long) (valLDR * 100 / LDRmax ); // converter para percentagem 0% a 100%
  int valLEDnew =  (int) (255  * valLDRnew / 100);
  // if (valLEDnew < 0 ) valLEDnew=0;
  // if (valLEDnew > 254) valLEDnew=254;

  if (valLDR >= LDRmed) {
    if (statePIR==HIGH) {   // caso volte a detetar movimento reinicia o timer
      statePIR = LOW;
      timer = TIMEmax;
    } 
    

    if (timer>0) {
      timer = timer - (millis() - timer2);

      if (valLED < valLEDnew) ++valLED;
      if (valLED > valLEDnew) --valLED;
    } else {
      timer = 0;
    }

    analogWrite(LED, valLED);
  } else {
    valLED = valLEDmin;
    analogWrite(LED, valLED);
    statePIR = LOW;
    timer = 0;
  }

  Serial.print("\nLight value: ");
  Serial.print(valLED);
  Serial.print("| Light value 2: ");
  Serial.print(valLEDnew);
  Serial.print("| LDR value: ");
  Serial.print(valLDR);
  Serial.print("| LDR %: ");
  Serial.print(valLDRnew);
  Serial.print("| PIR value: ");
  Serial.print(valPIR);
  Serial.print("| PIR state: ");
  Serial.print(statePIR);
  Serial.print("| Timer: ");
  Serial.print(timer);
  delay(50);

  timer2 = millis();
}

void loop() {
  // funcao para fazer a leitura de todos os inputs (sensores)
  inputs();
  outputs();

  // listen for incoming clients
  WiFiEspClient client = server.available();
  if (client) {
    Serial.println("New client");
    // an http request ends with a blank line
    boolean currentLineIsBlank = true;
    while (client.connected()) {
      if (client.available()) {
        char c = client.read();
        Serial.write(c);
        // if you've gotten to the end of the line (received a newline
        // character) and the line is blank, the http request has ended,
        // so you can send a reply
        if (c == '\n' && currentLineIsBlank) {
          Serial.println("Sending response");

          // send a standard http response header
          // use \r\n instead of many println statements to speedup data send
          client.print(
            "HTTP/1.1 200 OK\r\n"
            "Content-Type: text/html\r\n"
            "Connection: close\r\n"  // the connection will be closed after completion of the response
            "Refresh: 5\r\n"        // refresh the page automatically every 5 sec
            "\r\n");
          client.print("<!DOCTYPE HTML>\r\n");
          client.print("<html>\r\n");
          client.print("<h4>Smart Energy Campus</h4>\r\n");
          client.print("<h1>Lamp Post</h1>\r\n");
          client.print("<h2>Network</h2>\r\n");
          client.print("Mac Address: ");
          client.print(mac[5],HEX);client.print(":");client.print(mac[4],HEX);client.print(":");client.print(mac[3],HEX);client.print(":");
          client.print(mac[2],HEX);client.print(":");client.print(mac[1],HEX);client.print(":");client.print(mac[0],HEX);
          client.print("<br>\r\n");
          client.print("IP Address: ");
          client.print(ip);
          client.print("<br>\r\n");
          client.print("<h2>Status</h2>\r\n");
          client.print("Light value: "); client.print(valLED); client.print("<br>\r\n");
          client.print("LDR value: "); client.print(valLDR); client.print("<br>\r\n");
          client.print("PIR value: "); client.print(valPIR); client.print("<br>\r\n");
          client.print("<br>\r\n");
          client.print("Requests received: ");
          client.print(++reqCount);
          client.print("<br>\r\n");


          client.print("</html>\r\n");
          break;
        }
        if (c == '\n') {
          // you're starting a new line
          currentLineIsBlank = true;
        } else if (c != '\r') {
          // you've gotten a character on the current line
          currentLineIsBlank = false;
        }
      }
    }
    // give the web browser time to receive the data
    delay(10);

    // close the connection:
    client.stop();
    Serial.println("Client disconnected");
  }
}


void printWifiStatus() {
  // print the SSID of the network you're attached to
  Serial.print("SSID: ");
  Serial.println(WiFi.SSID());

  // print your WiFi shield's IP address
  ip = WiFi.localIP();
  Serial.print("IP Address: ");
  Serial.println(ip);
  WiFi.macAddress(mac);
  Serial.print("MAC: ");
  Serial.print(mac[5],HEX);
  Serial.print(":");
  Serial.print(mac[4],HEX);
  Serial.print(":");
  Serial.print(mac[3],HEX);
  Serial.print(":");
  Serial.print(mac[2],HEX);
  Serial.print(":");
  Serial.print(mac[1],HEX);
  Serial.print(":");
  Serial.println(mac[0],HEX);


  // print where to go in the browser
  Serial.println();
  Serial.print("To see this page in action, open a browser to http://");
  Serial.println(ip);
  Serial.println();
}