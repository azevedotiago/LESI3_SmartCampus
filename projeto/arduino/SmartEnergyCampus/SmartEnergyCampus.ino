#include <WiFiEsp.h>
#include <WiFiEspClient.h>
#include <WiFiEspServer.h>
#include <WiFiEspUdp.h>

/*
  
  Project: Smart Energy Campus
  Year: 2022 / 2023
        LESI @ IPCA
  Authors: 2727 Nuno Mendes
           21138 Rosario Silva
           21153 Tiago Azevedo
           21156 Francisco Pereira

*/

#include "WiFiEsp.h"
#include "WiFiEspClient.h"

//#ifndef HAVE_HWSERIAL1
#include "SoftwareSerial.h"
SoftwareSerial softserial(4, 5);  // RX, TX
//#endif
// network info variables
byte mac[6];
IPAddress ip;

char serveraddress[] = "10.10.10.2";  // web & database server address

char ssid[] = "smartenergy";   // your network SSID (name)
char pass[] = "20222023lesi";  // your network password

// Initialize the Ethernet client object
WiFiEspClient client;

int status = WL_IDLE_STATUS;
int reqCount = 0;  // number of requests received

#define LED 6         // pino de output dos LEDs, porta PWM
#define LDR 0         // pino de input do sensor de luz
#define PIR 3         // pino de input do sensor de movimento
#define LEDWIFION 10  // wireless conetado e a funcionar
#define LEDWIFIOFF 11 // wireless nao conetado
#define MAXLED 24     // LED maximum value during tests
#define LDRmax 1000   // LDR maximum input
#define LDRmin 40     // LDR minimum input
#define LDRmed 200    // 600 para efeitos de testes dentro de casa
#define TIMEmax 15    // tempo maximo LEDs ligados
#define valLEDmin 2   // valor dos LEDs quando ligados mas sem movimentom, em standby 
#define valINCREMENT 4 // valor de incremento / decremento na suavizacao de alteracao do valor da iluminacao

int valLED = 0;       // valor inicial
int stateLED = LOW;   // valor inicial do estado dos LEDs desligados
int valLDR = 0;       // valor inicial
long valLDRnew = 0;   // valor incicial
int valPIR = 0;       // valor inicial
int statePIR = LOW;   // sem deteção de movimento
uint32_t timer = 0;   // temporizador para o tempo dos LEDs ligados 
uint32_t timer2 = 0;

WiFiEspServer server(80);

void info() {
  // informacao inicial no arranque do sistema
  Serial.println("\n\n\n\n");
  Serial.println("Smart Energy Campus version 0.2 @ IPCA 2022/2023\n");
  Serial.println(" 2727 Nuno Mendes");
  Serial.println("21138 Rosario Silva");
  Serial.println("21153 Tiago Azevedo");
  Serial.println("21156 Francisco Pereira");
  delay(1000);
}

void test() {
  Serial.println("\n[Testing]");
  delay(1000);

  Serial.print("\n- Ilumination...");
  // aumentar o brilho
  Serial.print("\n Bright up ");
  for(int i=0; i<=255; i++) {
    if ((i % 2) == 0) Serial.print("+");
    ++i;
    analogWrite(LED, i);
    delay(10);
  }
  // reduzir o brilho
  Serial.print("\n Bright down ");
  for(int i=255; i>=0; i--){
    if ((i % 2) == 0) Serial.print("-");
    --i;
    analogWrite(LED, i);
    delay(10);
  }
  analogWrite(LED, 0);    // desliga os LEDs

  Serial.print("\n\n- Light Sensor LDR... "); 
  for(int i=0; i<=127; i++) {
    if ((i % 30) == 0) Serial.print("\n");
    valLDR = analogRead(LDR);
    Serial.print(" ");
    Serial.print(valLDR);
    delay(10);
  }
  valLDR = 0;


  Serial.print("\n\n- Motion Sensor PIR... "); 
  for(int i=0; i<=127; i++) {
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
  analogWrite(LED, 0);    // Desliga os LEDs
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
  valLDR = analogRead(LDR);             // leitura do valor do sensor LDR
  valPIR = digitalRead(PIR);            // leitura do valor do sensor de movimento PIR
  if (valPIR == HIGH) statePIR = HIGH;  // estado de detecao de movimento passa a TRUE
}

void outputs() {
  // LDRmax - pouca iluminacao, sem sol, escuro
  // LDRmin - muita iluminacao, muito sol
  if (valLDR <= LDRmin ) valLDR=LDRmin;
  if (valLDR >= LDRmax) valLDR=LDRmax;
  valLDRnew = (long) (valLDR * 100 / LDRmax );     // converter para percentagem 0% a 100%
  int valLEDnew =  (int) (255  * valLDRnew / 100); // atribui ao LED o valor de iluminacao ideal de acordo com o sensor de input LDR

  if (valLDR >= LDRmed) {
    
    if (statePIR==HIGH) {   // caso volte a detetar movimento reinicia o timer
      timer = TIMEmax;      // o tempo de LEDs ligados volta ao maximo
      stateLED = HIGH;      // liga os LEDs
      sendDataToServer();
      statePIR = LOW;       // estado detecao de movimento passa a FALSO
    } 
    
    if (timer > TIMEmax) timer = TIMEmax;
    if (timer > 0) {
      timer = timer - (millis() - timer2);  // atualiza o tempo restante guardado na variavel timer
      // Ajusta o valor da iluminacao conforme a intensidade de luz "solar", o novo valor que esta guardado em valLEDnew
      if (valLED < valLEDnew) valLED=valLED + valINCREMENT;
      if (valLED > valLEDnew) valLED=valLED - valINCREMENT;
    } else {                      // reduz o valor da iluminacao dos LEDs ao valor mínimo, iluminacao de presenca
      timer = 0;
      stateLED = LOW; 
      if (valLED > valLEDmin) {   // reduz a iluminacao até ser igual ao valor de iluminacao de presenca valLEDmin
        valLED = valLED - valINCREMENT;
      } else {
        valLED = valLEDmin;
      }
    }

    analogWrite(LED, valLED);     // atribui a iluminacao atual aos LEDs
  } else {                        // desliga os LEDs
    valLED = 0;                   // atribui a iluminacao a zero...
    analogWrite(LED, valLED);     // ...e desliga os LEDs
    timer = 0;
    sendDataToServer();
  }

  // envia para a consola os dados atuais de input e output
  Serial.print("\nLight actual value: "); Serial.print(valLED);
  Serial.print("| Light next value: "); Serial.print(valLEDnew);
  Serial.print("| Light state: "); Serial.print(stateLED);
  Serial.print("| LDR value: "); Serial.print(valLDR);
  Serial.print("| LDR %: "); Serial.print(valLDRnew);
  Serial.print("| PIR value: "); Serial.print(valPIR);
  Serial.print("| PIR state: "); Serial.print(statePIR);
  Serial.print("| Timer: "); Serial.print(timer);
  delay(100);

  timer2 = millis();    // regista o tempo atual
}

void loop() {
  // funcao para fazer a leitura de todos os inputs (sensores)
  inputs();   // leitura de sensores
  outputs();  // comandos para os atuadores

/*
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
          client.print("Light value: ");  client.print(valLED); client.print("<br>\r\n");
          client.print("Light state: ");  client.print(stateLED); client.print("<br>\r\n");
          client.print("LDR value: ");    client.print(valLDR); client.print("<br>\r\n");
          client.print("LDR %: ");        client.print(valLDRnew); client.print("<br>\r\n");
          client.print("PIR value: ");    client.print(valPIR); client.print("<br>\r\n");
          client.print("PIR state: ");    client.print(statePIR); client.print("<br>\r\n");
          client.print("Timer: ");        client.print(timer); client.print("<br>\r\n");
          client.print("<br>\r\n");
          client.print("Requests received: "); client.print(++reqCount);
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
  } */
}


void printWifiStatus() {
  // print the SSID of the network you're attached to
  Serial.print("SSID: ");
  Serial.println(WiFi.SSID());

  // print your WiFi shield's IP address
  ip = WiFi.localIP();
  Serial.print("IP Address: "); Serial.println(ip);
  WiFi.macAddress(mac);
  Serial.print("MAC: ");
  Serial.print(mac[5],HEX);  Serial.print(":");
  Serial.print(mac[4],HEX);  Serial.print(":");  
  Serial.print(mac[3],HEX);  Serial.print(":");  
  Serial.print(mac[2],HEX);  Serial.print(":");  
  Serial.print(mac[1],HEX);  Serial.print(":");  
  Serial.println(mac[0],HEX);

  // print where to go in the browser
  Serial.println();
  Serial.print("To see this page in action, open a browser to http://");
  Serial.println(ip);
  Serial.println();
}

void sendDataToServer() {

  Serial.println("\n\nSending data to server\n");  // close any connection before send a new request
  // this will free the socket on the WiFi shield
  client.stop();

  // if there's a successful connection
  if (client.connect(serveraddress, 80)) {
    String s1 = "GET /webservices.php?macaddress=";
    s1 += String(mac[5],HEX); s1 += ":";
    s1 += String(mac[4],HEX); s1 += ":";
    s1 += String(mac[3],HEX); s1 += ":";
    s1 += String(mac[2],HEX); s1 += ":";
    s1 += String(mac[1],HEX); s1 += ":";
    s1 += String(mac[0],HEX);
    //s1 += "&ipaddress=";       s1 += ip;
    String s2 = "&valled=";     s2 += valLED;
    s2 += "&stateled=";   s2 += stateLED;
    s2 += "&valldr=";     s2 += valLDR;
    s2 += "&valldrnew=";  s2 += valLDRnew;
    s2 += "&valpir=";     s2 += valPIR;
    s2 += "&statepir=";   s2 += statePIR;
    s2 += " HTTP/1.1";
    s1 += s2;
    Serial.println((s1));
    client.println((s1));
    client.println(F("Host: 10.10.10.2"));
    client.println("Connection: close");
    client.println();
    // note the time that the connection was made
  }
  else {
    // if you couldn't make a connection
    Serial.println(F("Connection failed"));
  }
}
