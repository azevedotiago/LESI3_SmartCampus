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

char ssid[] = "smartenergy";   // your network SSID (name)
char pass[] = "20222023lesi";  // your network password
int status = WL_IDLE_STATUS;
int reqCount = 0;  // number of requests received


#define LED 6 // pino do LED, porta PWM
#define LDR 0 // pino de input do sensor de luz
#define PIR 3 // pino de input do sensor de movimento
int valLDR = 0;
int valPIR = 0; 
int statePIR = LOW; // sem deteção de movimento

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
    if ((i % 30) == 0) Serial.print("\n");
    valPIR = digitalRead(PIR);
    Serial.print(" ");
    Serial.print(valPIR);
    delay(10);
    //if (i == 255) i=0;
  }
  valPIR = LOW;

  Serial.println("\n");
}


void setup() {
  pinMode(LED, OUTPUT);
  pinMode(LDR, INPUT);
  pinMode(PIR, INPUT);
  analogWrite(LED, 0); // Desliga os LEDs


  // initialize serial for debugging
  Serial.begin(9600);

  // Info do projeto
  info();

  // Testando os componentes externos
  test();

  // initialize serial for ESP module
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
    Serial.print("Attempting to connect to WPA SSID: ");
    Serial.println(ssid);
    // Connect to WPA/WPA2 network
    status = WiFi.begin(ssid, pass);
  }

  Serial.println("You're connected to the network");
  printWifiStatus();

  // start the web server on port 80
  server.begin();
}


void loop() {

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
            "Refresh: 20\r\n"        // refresh the page automatically every 20 sec
            "\r\n");
          client.print("<!DOCTYPE HTML>\r\n");
          client.print("<html>\r\n");
          client.print("<h4>ESP8266 Wifi IoT lesson 1</h4>\r\n");
          client.print("<h1>Hello World!</h1>\r\n");
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
  IPAddress ip = WiFi.localIP();
  Serial.print("IP Address: ");
  Serial.println(ip);

  // print where to go in the browser
  Serial.println();
  Serial.print("To see this page in action, open a browser to http://");
  Serial.println(ip);
  Serial.println();
}