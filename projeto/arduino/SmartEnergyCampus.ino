/*
  Project: Smart Energy Campus
  Year: 2022 / 2023
        LESI @ IPCA
  Authors: 2727 Nuno Mendes
           21138 Rosario Silva
           21153 Tiago Azevedo
           21156 Francisco Pereira
*/

#include <WiFiEsp.h>
#include <WiFiEspClient.h>
//#include <WiFiEspServer.h>
#include "SoftwareSerial.h"
#include "TimerOne.h"

SoftwareSerial softserial(4, 5);  // RX, TX
byte mac[6];
IPAddress ip;

//char serveraddress[] = "10.10.10.2";  // endereco do servidor web e base de dados
char ssid[] = "smartenergy";          // nome de rede sem fios (SSID)
char pass[] = "20222023lesi";         // senha da rede sem fios

// Inicializa o cliente de rede
WiFiEspClient client;
int status = WL_IDLE_STATUS;
int reqCount = 0;      // Em modo servidor web: numero de pedidos recebidos

#define LED 6          // pino de output dos LEDs, porta PWM
#define LDR 0          // pino de input do sensor de luz
#define PIR 3          // pino de input do sensor de movimento
#define LEDWIFION 9    // wireless conetado e a funcionar
#define LEDWIFIOFF 11  // wireless nao conetado
#define MAXLED 24      // LED maximum value during tests
#define LDRmax 1000    // LDR maximum input
#define LDRmin 40      // LDR minimum input
#define LDRmed 600     // 600 para efeitos de testes dentro de casa, 400 no IPCA
#define TIMEmax 15     // tempo maximo LEDs ligados
#define valLEDmin 2    // valor dos LEDs quando ligados mas sem movimentom, em standby 
#define valINCREMENT 4 // valor de incremento / decremento na suavizacao de alteracao do valor da iluminacao

int counter = 0;
int periodo = 20;     // tempo em segundo em que sao enviados periodicamente dados para o servidor
int valLED = 0;        // valor inicial
int stateLED = LOW;    // valor inicial do estado dos LEDs desligados
int valLDR = 0;        // valor inicial
long valLDRnew = 0;    // valor incicial
int valPIR = 0;        // valor inicial
int statePIR = LOW;    // sem deteção de movimento
uint32_t timer = 0;    // temporizador para o tempo dos LEDs ligados 
uint32_t timer2 = 0;
int sendData = 0;      // estado do envio de dados para o servidor

//WiFiEspServer server(80);

void info() {
  // informacao inicial no arranque do sistema
  Serial.println("\n\n\n\n");
  Serial.println("Smart Energy Campus version 0.4 @ IPCA 2022/2023\n");
  Serial.println(" 2727 Nuno Mendes");
  Serial.println("21138 Rosario Silva");
  Serial.println("21153 Tiago Azevedo");
  Serial.println("21156 Francisco Pereira");
  //delay(750);
}

void test() {
  Serial.println("\n[Testing]");
  delay(1000);

  Serial.print("\n- Ilumination...");
  // aumentar o brilho
  Serial.print("\n Bright up ");
  for(int i=0; i<=255; i++) {
    //if ((i % 2) == 0) Serial.print("+");
    ++i;
    analogWrite(LED, i);
    delay(10);
  }
  // reduzir o brilho
  Serial.print("\n Bright down ");
  for(int i=255; i>=0; i--){
    //if ((i % 2) == 0) Serial.print("-");
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

  // inicializacao do Interrupt atraves de um Timer
  Timer1.initialize(500000);
  Timer1.setPeriod(1000000);            // definido para periodos de 1 segundo
  Timer1.attachInterrupt(periodic);     // funcao que invoca quando e' atingido o periodo

  // inicializa a consola serie para depuracao (debug)
  Serial.begin(9600);

  // Info do projeto
  info();

  // Testando os componentes externos
  //test();

  // incializacao serie para o modulo ESP
  analogWrite(LEDWIFIOFF, MAXLED);
  Serial.println("\n[Network connection]");
  softserial.begin(115200);
  softserial.write("AT+CIOBAUD=9600\r\n");
  softserial.write("AT+RST\r\n");
  softserial.begin(9600);
  // inicializa o modulo ESP
  WiFi.init(&softserial);

  // verifica a presença do shield WiFi
  if (WiFi.status() == WL_NO_SHIELD) {
    Serial.println("WiFi shield not present");
    // nao continua
    while (true)
      ;
  }

  // tentiva de conetar a rede sem fios
  while (status != WL_CONNECTED) {
    analogWrite(LED, 255);
    analogWrite(LEDWIFION, MAXLED);
    analogWrite(LEDWIFIOFF, 0);
    delay(75);
    analogWrite(LED, 64);
    analogWrite(LEDWIFION, 0);
    analogWrite(LEDWIFIOFF, MAXLED);
    delay(75);
    analogWrite(LED, 255);
    analogWrite(LEDWIFION, MAXLED);
    analogWrite(LEDWIFIOFF, 0);
    delay(75);
    analogWrite(LED, 64);
    analogWrite(LEDWIFION, 0);
    analogWrite(LEDWIFIOFF, MAXLED);
    delay(75);

    Serial.print("Tentando conetar a rede com SSID: ");
    Serial.println(ssid);
    // Conetar a rede sem fios com WPA/WPA2
    status = WiFi.begin(ssid, pass);
    analogWrite(LED, 0);
  }

  Serial.println("Esta ligado a rede sem fios");
  printWifiStatus();
  analogWrite(LEDWIFION, MAXLED);
  analogWrite(LEDWIFIOFF, 0);

  // start the web server on port 80
  //server.begin();
}

void inputs() {
  valLDR = analogRead(LDR);     // leitura do valor do sensor LDR
  valPIR = digitalRead(PIR);    // leitura do valor do sensor de movimento PIR
  if (valPIR == HIGH) {
    statePIR = HIGH;            // estado de detecao de movimento passa a TRUE
    sendDataToServer();
  }
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
      stateLED = HIGH; 
      if (valLED > valLEDmin) {   // reduz a iluminacao até ser igual ao valor de iluminacao de presenca valLEDmin
        valLED = valLED - valINCREMENT;
      } else {
        valLED = valLEDmin;
      }
    }

    analogWrite(LED, valLED);     // atribui a iluminacao atual aos LEDs
  } else {                        // desliga os LEDs
    stateLED = LOW; 
    valLED = 0;                   // atribui a iluminacao a zero...
    analogWrite(LED, valLED);     // ...e desliga os LEDs
    timer = 0;
    //sendDataToServer();
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
  Serial.print("| Counter: "); Serial.print(counter);
  delay(75);

  timer2 = millis();    // regista o tempo atual
  if (statePIR == HIGH && stateLED == LOW) {
    statePIR = LOW;
  }
}

void loop() {
  // funcao para fazer a leitura de todos os inputs (sensores)
  inputs();   // leitura de sensores
  outputs();  // comandos para os atuadores

/* inicio: serviço http do proprio poste de iluminacao*/
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
  }  */
  /* fim: serviço http do proprio poste de iluminacao*/
}

void printWifiStatus() {
  // escreve na consola o SSID da rede sem fios a qual esta ligado
  Serial.print("SSID: ");
  Serial.println(WiFi.SSID());

  // escreve na consola o endereco IP do shield WiFi
  ip = WiFi.localIP();
  Serial.print("IP Address : "); Serial.println(ip);
  WiFi.macAddress(mac);
  Serial.print("MAC Address: ");
  Serial.print(mac[5],HEX);  Serial.print(":");
  Serial.print(mac[4],HEX);  Serial.print(":");  
  Serial.print(mac[3],HEX);  Serial.print(":");  
  Serial.print(mac[2],HEX);  Serial.print(":");  
  Serial.print(mac[1],HEX);  Serial.print(":");  
  Serial.println(mac[0],HEX);

  // escreve na consola o link para abrir a partir de um navegador/browser
  Serial.println();
  Serial.print("Para acesso direto ao poste abrir num browser o endereco http://");
  Serial.println(ip);
}

void sendDataToServer() { // funcao que faz o envio dos dados atuais para o servidor
if (sendData == LOW) {    // nao deixa executar o envio de dados mais que uma vez em simultaneo
  sendData=HIGH;

  analogWrite(LEDWIFION, 0);
  analogWrite(LEDWIFIOFF, 0);
  Serial.println("\n\nEnviado dados para o servidor");

  client.stop(); // termina todas as ligacoes e efetua um novo pedido e liberta o socket do shield WiFi

  // verifica se existe conetividade com o servidor
  if (client.connect("10.10.10.2", 80)) {
    // a ligacao com o servidor foi efetuada
    // pisca led VERDE para sinalizar comunicacao com o servidor com sucesso

    String s1 = "GET /webservices.php?macaddress=";
    s1 += String(mac[5],HEX); s1 += ":";
    s1 += String(mac[4],HEX); s1 += ":";
    s1 += String(mac[3],HEX); s1 += ":";
    s1 += String(mac[2],HEX); s1 += ":";
    s1 += String(mac[1],HEX); s1 += ":";
    s1 += String(mac[0],HEX);
    s1 += "&ipaddress=";
    s1 += String(ip[0])+String(".")+String(ip[1]) +String(".")+String(ip[2])+String(".")+String(ip[3]); // endereço IP atual
    String s2 = "&valled="; s2 += valLED;
    s2 += "&stateled=";     s2 += stateLED;
    s2 += "&valldr=";       s2 += valLDR;
    s2 += "&valldrnew=";    s2 += valLDRnew;
    s2 += "&valpir=";       s2 += valPIR;
    s2 += "&statepir=";     s2 += statePIR;
    s2 += " HTTP/1.1";
    s1 += s2;
    Serial.println((s1));
    
    analogWrite(LEDWIFION, MAXLED); delay(100);
    client.println((s1));
    analogWrite(LEDWIFION,0); delay(100);
    client.println(F("Host: 10.10.10.2"));
    analogWrite(LEDWIFION,MAXLED); delay(100);
    client.println("Connection: close");
    analogWrite(LEDWIFION,0); delay(100);
    client.println();
    analogWrite(LEDWIFION,MAXLED); delay(100);
  }
  else {
    // se a ligacao com o servidor nao for efetuada
    // pisca led VERMELHO para sinalizar erro de comunicacao com o servidor
    Serial.println(F("A ligacao falhou!"));
    analogWrite(LEDWIFIOFF, MAXLED); delay(100);
    analogWrite(LEDWIFIOFF, 0); delay(100);
    analogWrite(LEDWIFIOFF, MAXLED); delay(100);
    analogWrite(LEDWIFIOFF, 0); delay(100);
  }

  analogWrite(LEDWIFION,MAXLED);
  analogWrite(LEDWIFIOFF, 0);
  client.stop(); 
  sendData=LOW;
  }
}

void periodic() {
  if (counter >= periodo) {
       sendDataToServer();
       counter = 0;
  } else {
  ++counter;
  }
}