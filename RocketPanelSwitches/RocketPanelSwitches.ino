/*Rocket Panel Version 0.43
  This version switches back to using the keyboard setup because
    the Unity Engine doesn't support more than 1 joystick and 20 buttons.
    Ugh.
*/

//JoyState_t joySt; //Joystick is disabled, but the code is left in place in the event you want to switch between keyboard/joystick modes

// Define the Variables and Hardware
  int buttonArmStatus = 0;  //Variable for the status of the Arming key
  const int ledArduino =  13; //Built in LED
  const int keySwitchMain = A0; // The only switch with a key on the board will dis/en-able everything
//Setup the Arming Key Buttons, then the Arming LEDs
  const int buttonArm = A4; //Set as the Red Covered Toggle switch
  const int buttonYellowPower = A1; //Joystick Button 0
  const int buttonRedPower = A2; //Joystick Button 1
  const int ledStageActive =  4;
  const int ledAbortActive =  8;
  const int ledArmGreen =  23;    
  const int ledStagingbuttons =  7; 

//Setup the system control switches
  const int buttonGear = 13;       //Joystick Button 4
  const int buttonLights = 31;
  const int buttonBrakes = A5;     //Joystick Button 2 - Not yet conencted to anything physical
  const int buttonSAStoggle = A3;  //Joystick Button 3
  const int buttonSAS = 33;
  const int buttonRCS = 34;
  const int ledBlueToggle = 5;
  const int ledRedToggle = 6;
  const int ledYellowToggle = 9;
  const int ledGreenToggle = 10;
  
/* //Setup Analog Meters
  int analogGaugeGFORCE = 2;
  int analogGaugeElectricCharge = 3;
  int analogGaugeMonoproppelent = 4;
  int analogGaugeAtmoDensity = 5;
  int analogGaugeLiquidFuel = 6;
  int analogGaugeOxidizer = 7;
*/

//Setup button debouncing using the Bounce library
#include <Bounce.h>
// Instantiate a Bounce object with a 50 millisecond debounce time
Bounce bounceButtonRedPower = Bounce( buttonRedPower,50 ); 
Bounce bounceButtonYellowPower = Bounce( buttonYellowPower,50 ); 



//Setup variables to use ledArduino as a keep-alive indicator (it blinks slowly)
int stateLedArduino = LOW;             // stateLedArduino used to set the status of ledArduino
long previousLedArduinoMillis = 0;        // will store last time LED was updated
long intervalLedArduino = 1000;  // interval at which to blink ledArduino (in milliseconds)



//Initialize Input/Output//////////////////////
void setup() {
  // Initialize LEDs as Output:
  pinMode(ledAbortActive, OUTPUT);
  pinMode(ledStageActive, OUTPUT); 
  pinMode(ledStagingbuttons, OUTPUT);
  pinMode(ledArmGreen, OUTPUT);
  pinMode(ledArduino, OUTPUT);
  pinMode(ledBlueToggle, OUTPUT);
  pinMode(ledRedToggle, OUTPUT);
  pinMode(ledYellowToggle, OUTPUT);
  pinMode(ledGreenToggle, OUTPUT);
  
  // Initialize Buttons as Input
  pinMode(buttonRedPower, INPUT);
  pinMode(buttonYellowPower, INPUT); 
  pinMode(buttonArm, INPUT);
  pinMode(buttonBrakes, INPUT);
  pinMode(buttonSAStoggle, INPUT);
  pinMode(buttonGear, INPUT);
  /* // Initialize Analog Meters as PWM Output
  pinMode(analogGaugeGFORCE, OUTPUT);
  pinMode(analogGaugeElectricCharge, OUTPUT);
  pinMode(analogGaugeMonoproppelent, OUTPUT);
  pinMode(analogGaugeAtmoDensity, OUTPUT);
  pinMode(analogGaugeLiquidFuel, OUTPUT);
  pinMode(analogGaugeOxidizer, OUTPUT);
  */
  
 /*
        joySt.xAxis = 128;
	joySt.yAxis = 128;
	joySt.zAxis = 128;
	joySt.xRotAxis = 128;
	joySt.yRotAxis = 128;
	joySt.zRotAxis = 128;
	joySt.throttle = 128;
	joySt.rudder = 128;
	joySt.hatSw1 = 128;
	joySt.hatSw2 = 128;
	joySt.buttons = 0;
*/
  digitalWrite(ledRedToggle, HIGH);
  digitalWrite(ledBlueToggle, HIGH);
}

void loop(){
  //joySt.buttons = 0x0; // Reset all joystick buttons to off
  // Button values follow pattern of
  // 0x1, 0x2, 0x4, 0x8, 0x10, 0x20, 0x40, 0x80, 0x100, 0x200, 0x400, 0x800, 0x1000, 0x2000, 0x4000, 0x8000
  
  bounceButtonRedPower.update ( );
  bounceButtonYellowPower.update ( );
if (digitalRead(keySwitchMain) == HIGH){ 
 
  
////////////Arming System///////////////////
  buttonArmStatus = digitalRead(buttonArm);
  if (buttonArmStatus == HIGH){   
     // Arm Staging System:   
     digitalWrite(ledStagingbuttons, HIGH); 
     digitalWrite(ledRedToggle, HIGH);
     digitalWrite(ledArmGreen, LOW);
     intervalLedArduino = 100;
     //Monitor Red Power Button//
     if (bounceButtonRedPower.read() == HIGH) {digitalWrite(ledAbortActive, LOW);}
     else {digitalWrite(ledAbortActive, HIGH);
          //joySt.buttons += 0x1; // Set joystick button 1 to pressed for this cycle
          Keyboard.write(0xB2);
         
      }
      
     //Monitor Yellow Power Button//
     
     if (bounceButtonYellowPower.read() == HIGH)
          {digitalWrite(ledStageActive, LOW);}
     else {digitalWrite(ledStageActive, HIGH);
           //joySt.buttons += 0x2; //Set joystick button 2 to pressed for this cycle
           Keyboard.write(0x20);
          }
  }
 
  else
  {
    // Disable Staging System
    digitalWrite(ledStagingbuttons, LOW); 
    digitalWrite(ledRedToggle, LOW);
    digitalWrite(ledAbortActive, LOW);
    digitalWrite(ledStageActive, LOW);
    digitalWrite(ledArmGreen, HIGH);
    intervalLedArduino = 500;
  } //End of Arming System
  
  
// digitalWrite(analogGaugeGFORCE, 128); //Sets a demo gauge to 50%
 
 //Check the covered toggle switches and set their joystick buttons / LEDs
 if (digitalRead(buttonSAStoggle) == HIGH){
    //joySt.buttons += 0x4;
    Keyboard.write(0x46);
     digitalWrite(ledBlueToggle, LOW);}
   else {digitalWrite(ledBlueToggle, HIGH);}
   
  if (digitalRead(buttonGear) == HIGH){
    //joySt.buttons += 0x8;
    Keyboard.write(0x47);
     digitalWrite(ledGreenToggle, LOW);}
   else {digitalWrite(ledGreenToggle, HIGH);}
   
    if (digitalRead(buttonBrakes) == HIGH){
    //joySt.buttons += 0x10;
    Keyboard.write(0x42);
     digitalWrite(ledYellowToggle, LOW);}
   else {digitalWrite(ledYellowToggle, HIGH);}
 
 /*  /////// Write this cycle's joystick status to Joystick.move
	Joystick.setState(&joySt);
    digitalWrite(ledRedToggle, HIGH);
*/

  }
 else {
   intervalLedArduino = 1000;
  digitalWrite(ledRedToggle, HIGH);
  digitalWrite(ledBlueToggle, HIGH);
  digitalWrite(ledYellowToggle, HIGH);
  digitalWrite(ledGreenToggle, HIGH);
  digitalWrite(ledStagingbuttons, LOW); 
  digitalWrite(ledAbortActive, LOW);
  digitalWrite(ledStageActive, LOW);
  digitalWrite(ledArmGreen, HIGH);
 }

/////////Update ledArduino as a "system working" indicator/////////
 unsigned long currentLedArduinoMillis = millis();
 
  if(currentLedArduinoMillis - previousLedArduinoMillis > intervalLedArduino) {
    // save the last time you blinked the LED
    previousLedArduinoMillis = currentLedArduinoMillis;  

    // if the LED is off turn it on and vice-versa:
    if (stateLedArduino == LOW)
      stateLedArduino = HIGH;
    else
      stateLedArduino = LOW;

    // set the LED with the stateLedArduino of the variable:
    digitalWrite(ledArduino, stateLedArduino);
  }
 


}//End Program
