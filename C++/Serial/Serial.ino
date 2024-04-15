String x;
// PIN_4 = Rasp pi 4gb RAM
int PIN_4 = 2;
// PIN_8 = Rasp pi 8gb RAM
int PIN_8 = 4;



void setup() {
  Serial.begin(115200);
  Serial.setTimeout(1);
  pinMode(PIN_4, OUTPUT);
  pinMode(PIN_8, OUTPUT);
}
void loop() {
  while (!Serial.available())
    ;
  x = Serial.readString();
  if (x.equals("Ligar4")) {
    digitalWrite(PIN_4, HIGH);
    Serial.print("4ON|");
  } else if (x.equals("Desligar4")) {
    digitalWrite(PIN_4, LOW);
    Serial.print("4OFF|");
  } else if (x.equals("Ligar8")) {
    digitalWrite(PIN_8, HIGH);
    Serial.print("8ON|");
  } else if (x.equals("Desligar8")) {
    digitalWrite(PIN_8, LOW);
    Serial.print("8OFF|");
  }
}