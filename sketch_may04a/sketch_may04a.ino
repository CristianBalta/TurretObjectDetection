int ledPin = 13;


void setup() {
  // put your setup code here, to run once:
  pinMode(ledPin, OUTPUT);
  Serial.begin(115200);

}

void loop() {
  // put your main code here, to run repeatedly:
  if(Serial.available()){
    blink(Serial.read()- '0');
  }
  delay(500);

  Serial.println("Hello from Arduino!");
  delay(1000);

}

void blink(int numberOfTimes){
  for(int i = 0; i < numberOfTimes; i++){
    digitalWrite(ledPin, HIGH);
    delay(100);
    digitalWrite(ledPin, LOW);
    delay(100);
  }
}
