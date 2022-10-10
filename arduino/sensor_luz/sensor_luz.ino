// Projeto 2 : Sensor de Luz

// pino da ligação do led
int ledPin = 6;
// pino de ligação do LDR
int ldrPin = 0;
// valor lido do LDR;
int lightVal = 0;

void setup() {
  Serial.begin(9600);
  // definir os pinos como de saída
  pinMode(ledPin, OUTPUT);
}

void loop() {
  // ler o valor do LDR
  lightVal = analogRead(ldrPin);
  
  Serial.print("\nLeitura entrada analogica: ");
  Serial.print(lightVal);  

  // acende o led Verde
  digitalWrite(ledPin, HIGH);

  // Atraso com valor do lightVal
  delay(lightVal);

  // desliga o led Verde
  digitalWrite(ledPin, LOW);
 
  // Atraso com valor do lightVal
  delay(lightVal);

}
