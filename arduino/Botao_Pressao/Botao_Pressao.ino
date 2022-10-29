// Exemplo: Acender LED ao pressionar o botão
#define LED 11   // pino do LED, porta PWM
#define BUTTON 7 // pino de input do botão

int val = 0;     // val é usado para guardar o estado do pino de input
unsigned long old_time;
unsigned long new_time;

void setup() {
  pinMode(LED, OUTPUT);
  pinMode(BUTTON, INPUT);
  Serial.begin(9600);
}

void loop() {

  val = digitalRead(BUTTON); // Lê o valor de input e guarda-o
  Serial.print("\nEstado do botao de pressao: ");
  Serial.print(val); 

  // verifica se o botão está HIGH (pressionado)
  if (val == HIGH) {
    for(int i=0; i<2; i++) {
      new_time = millis();
      Serial.print("\nTempo passado desde o inicio: ");
      Serial.print((new_time-old_time)/ 1000);
      Serial.print(" segundos");
      old_time = new_time;
    
      // aumentar o brilho
      for(int i=0; i<255; i++) {
        analogWrite(LED, i);
        delay(2);
      }
      // reduzir o brilho
      for(int i=255; i>0; i--){
        analogWrite(LED, i);
        delay(2);
      }
      delay(500);
    }
  } else {
    analogWrite(LED, 0);
  }
}
