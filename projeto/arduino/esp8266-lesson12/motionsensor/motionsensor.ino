/*  ___   ___  ___  _   _  ___   ___   ____ ___  ____  
 * / _ \ /___)/ _ \| | | |/ _ \ / _ \ / ___) _ \|    \ 
 *| |_| |___ | |_| | |_| | |_| | |_| ( (__| |_| | | | |
 * \___/(___/ \___/ \__  |\___/ \___(_)____)___/|_|_|_|
 *                  (____/ 
 * Osoyoo W5100 web server lesson 12
 * send motionsensor data through internet UDP protocol
 * tutorial url: https://osoyoo.com/?p=10000
 */

 

int inputPin = 3;               // choose the input pin D3(for PIR sensor)
int pirState = LOW;             // we start, assuming no motion detected
int val = 0;                    // variable for reading the pin status
 

#include "WiFiEsp.h"
#include <WiFiEspUdp.h>
#include "SoftwareSerial.h"
SoftwareSerial softserial(4, 5); // A9 to ESP_TX, A8 to ESP_RX by default
char ssid[] = "***";            // your network SSID (name)
char pass[] = "***";        // your network password
int status = WL_IDLE_STATUS;     // the Wifi radio's status
WiFiEspUDP Udp;
unsigned int localPort = 8888;              // local port to listen on
char packetBuffer[5];      
int connectionId;
char  ReplyBuffer[] = "acknowledged";       // a string to send back
unsigned int buzzerPort = 8888;        // buzzer port to listen for UDP packets
 

void setup() {
  pinMode(pirState, INPUT);

  Serial.begin(9600);   // initialize serial for debugging
    softserial.begin(115200);
  softserial.write("AT+CIOBAUD=9600\r\n");
  softserial.write("AT+RST\r\n");
  softserial.begin(9600);    // initialize serial for ESP module
  WiFi.init(&softserial);    // initialize ESP module

  // check for the presence of the shield:
  if (WiFi.status() == WL_NO_SHIELD) {
    Serial.println("WiFi shield not present");
    // don't continue:
    while (true);
  }

  // attempt to connect to WiFi network
  while ( status != WL_CONNECTED) {
    Serial.print("Attempting to connect to WPA SSID: ");
    Serial.println(ssid);
    // Connect to WPA/WPA2 network
    status = WiFi.begin(ssid, pass);
  }
  
  Serial.println("Connected to wifi");
  printWifiStatus();

  Serial.println("\nStarting connection to server...");
  // if you get a connection, report back via serial:
  Udp.begin(localPort);
  
  Serial.print("Listening on port ");
  Serial.println(localPort);
 
}
 
void loop() {
  byte remoteIp[] = { 10,0,0,15 }; // Replace this IP with the IP in buzzer.ino serial monitor
  Udp.beginPacket(remoteIp,buzzerPort);
  val = digitalRead(inputPin);  // read input value
  if (val == HIGH) {            // check if the input is HIGH
 
    if (pirState == LOW) {
      // we have just turned on
      Serial.println("Motion detected!");
      Udp.write("A");
      Udp.endPacket();
      delay(10);
      // We only want to print on the output change, not state
      pirState = HIGH;
    }
  } else {
 
    if (pirState == HIGH){
      // we have just turned of
      Serial.println("Motion ended!");
      Udp.write("C");
      Udp.endPacket();
      delay(100);
      // We only want to print on the output change, not state
      pirState = LOW;
    }
  }
}
void printWifiStatus()
{
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
