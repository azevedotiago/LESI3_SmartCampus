// Projeto 1: Semaforos

int ledDelay = 10000;
int redPin = 10;
int yellowPin = 9;
int greenPin = 8;

void setup() {
  // put your setup code here, to run once:
  pinMode(redPin, OUTPUT);
  pinMode(yellowPin,OUTPUT);
  pinMode(greenPin,OUTPUT);
}

void loop() {
  //Acender vermelho
  digitalWrite(redPin,HIGH);
  delay(ledDelay);
  digitalWrite(redPin,LOW);

  // acender verde
  digitalWrite(greenPin,HIGH);
  delay(ledDelay);
  digitalWrite(greenPin,LOW);

  // acender amarelo
  digitalWrite(yellowPin,HIGH);
  delay(2000);
  digitalWrite(yellowPin,LOW);
}


