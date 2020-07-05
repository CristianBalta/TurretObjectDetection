#include <Stepper.h>

String serData;

volatile long temp, counter = 0; //This variable will increase or decrease depending on the rotation of encoder
int error = 0;
int steps = 800; // change this to fit the number of steps per revolution


// initialize the stepper library on pins 8 through :
Stepper myStepper(steps, 51, 50);
Stepper myStepper2(steps, 12, 13);




void setup(){
  myStepper.setSpeed(60);
  myStepper2.setSpeed(120);


Serial.begin (115200);
  pinMode(2, INPUT_PULLUP); // internal pullup input pin 2 
  
  pinMode(3, INPUT_PULLUP); // internal pullup input pin 3
   //Setting up interrupt
  //A rising pulse from encodenren activated ai0(). AttachInterrupt 0 is DigitalPin nr 2 on moust Arduino.
  attachInterrupt(0, ai0, RISING);
   
  //B rising pulse from encodenren activated ai1(). AttachInterrupt 1 is DigitalPin nr 3 on moust Arduino.
  attachInterrupt(1, ai1, RISING);
}

void loop() {  
  
  deplasare(800);

  delay(5000);

  deplasare(-800);
  delay(500000);
  

}

void deplasare(int pozitia_finala){
  
  // step one revolution  in one direction:
  myStepper.step(pozitia_finala);
  delay(500);

  Serial.println("The stepper was told: ");
  Serial.println(pozitia_finala);

  Serial.println("The encoder measured: ");
  Serial.println(4*counter);
  
  verificare(pozitia_finala, 4*counter);
  
  counter = 0;

  delay(500);
 
}

void verificare(int pozitia_finala, int encoder_counter){
  
  if (abs(pozitia_finala) - encoder_counter != 0)
  {
  
  error = abs(pozitia_finala) - encoder_counter;
  
  Serial.println("The error is: ");
  Serial.println(error);
  
  pozitia_finala = error;
  error = 0;
  encoder_counter = 0;
  counter = 0;

  deplasare(pozitia_finala);
  

  }

}

void ai0() {
  // ai0 is activated if DigitalPin nr 2 is going from LOW to HIGH
  // Check pin 3 to determine the direction
  if(digitalRead(3)==LOW) {
  counter++;
  }else{
  counter--;
  }
  }
   
  void ai1() {
  // ai0 is activated if DigitalPin nr 3 is going from LOW to HIGH
  // Check with pin 2 to determine the direction
  if(digitalRead(2)==LOW) {
  counter--;
  }else{
  counter++;
  }
  }
