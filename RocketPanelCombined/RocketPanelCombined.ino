//This program sets an analog meter to various levels.

#include "LedControl.h"
unsigned long st = 0; //set up the cycle time record
unsigned long dt = 0; //Loop end time
unsigned long sleep_marker = 0;


// wire 08 goes to vertical gauge
// wire 09 goes to left dual gauge
// wire 10 goes to right dual gauge
// wire 11 goes to 7brown CLK
// wire 12 goes to 7green Data IN
// wire 13 goes to 7blue LOAD
#define gaugeVertical 8
#define gaugeDualLeft 9
#define gaugeDualRight 10
// the 7 segment displays are handled differently
// (DataIN, Clock, LOAD, number of displays)
LedControl lc=LedControl(12,11,13,5);

# define bPwrRed 34 //Correct
# define bPwrYlw 32 //Correct
# define bAnglGrn 30 //correct
# define bAnglYlw 22 //Correct
# define bAnglRed 28 //Correct
# define bAnglWht 24 //Correct
# define bAnglBlu 26 //Correct
# define sKey 36 //Correct
# define lPwrRed 23
# define lPwrYlw 25

//Declare global variables
// MET(seconds), ASL, Apoapsis, Periapsis, Vertical Speed, Horizontal Speed
byte memA[]  = {0, 0, 0, 0, 0, 0, 0, 48, 0, 0, 0, 0, 0, 0, 0, 48, 0, 0,
  0, 0, 0, 0, 0, 48, 0, 0, 0, 0, 0, 0, 0, 48, 0, 0, 0, 0, 0, 0, 0, 48,
  128, 0, 0, 0, 0, 0, 0, 48, 0, 0};
  
//Memory for button presses
boolean memB[11]; 

void setup (){
 Serial.begin(9600);
 
 pinMode(gaugeVertical, OUTPUT);
 pinMode(gaugeDualLeft, OUTPUT);
 pinMode(gaugeDualRight, OUTPUT);
 pinMode(bPwrRed, INPUT);
 pinMode(bPwrYlw, INPUT);
 pinMode(bAnglGrn, INPUT);
 pinMode(bAnglYlw, INPUT);
 pinMode(bAnglRed, INPUT);
 pinMode(bAnglWht, INPUT);
 pinMode(bAnglBlu, INPUT);
 pinMode(sKey, INPUT);
 pinMode(lPwrRed, OUTPUT);
 pinMode(lPwrYlw, OUTPUT);
 
 digitalWrite(bPwrRed, HIGH);
 digitalWrite(bPwrYlw, HIGH);
 digitalWrite(bAnglGrn, HIGH);
 digitalWrite(bAnglYlw, HIGH);
 digitalWrite(bAnglRed, HIGH);
 digitalWrite(bAnglWht, HIGH);
 digitalWrite(bAnglBlu, HIGH);
 digitalWrite(sKey, HIGH);
 


// disable sleep mode for the 7segment displays
  lc.shutdown(0,false);
  lc.shutdown(1,false);
  lc.shutdown(2,false);
  lc.shutdown(3,false);
  lc.shutdown(4,false);
// set the 7seg brightness to between 0 and 15 */
  int sevbright = 5; 
    // Set brightness for all 7 segment displays. 
    // 5 is nice for direct viewing
    // 15 can be read through a sheet of paper
  lc.setIntensity(0,sevbright);
  lc.setIntensity(1,sevbright);
  lc.setIntensity(2,sevbright);
  lc.setIntensity(3,sevbright);
  lc.setIntensity(4,sevbright);
// clear the 7seg displays
  lc.clearDisplay(0);
  lc.clearDisplay(1);
  lc.clearDisplay(2);
  lc.clearDisplay(3);
  lc.clearDisplay(4);
 
  /*for(int n=0; n<10; n++) {
    Serial.println(memA[n]); 
  } */
}


void updateSerial (){
   int count = 0;
   byte buffer;
   if (Serial.available() > 47){
   while (Serial.available() > 0) {
    buffer = Serial.read();
    if (buffer == byte(13)) { 
      buffer = 0;
      break;
      }
    else if (count > 48) {
      buffer = 0;
      break;
      }
    else {
      memA[count] = buffer;
    }
    count++;
    }
   }

}


void writeAnalog(){
  //Configure Rate of Climb for the Vertical Gauge I have
  byte gVByte = (memA[40] * (182/255))  + 140;  
  //Configure LiquidFuel for the Weird Gauge I have
  byte gDLByte = memA[41]*10/255;      
  //Configure Oxidizer for the Weird Gauge I have
  byte gDRByte = memA[42]*10/255;
        
      // Write the values to the display 
      analogWrite(gaugeVertical, gVByte);
    /* Using a 180 ohm resistor to set 2.5v to around neutral 
      50=bottom, 140=mid, 232=top; range=182steps
      
      Using the resistor helps, but there is still too much
      voltage sag (and change) as the various displays and
      LEDs turn on and off, causing the refV to fluctuate
      and the gauges to loose accuracy. This is a hardware problem.
    */
      analogWrite(gaugeDualLeft, gDLByte);
      analogWrite(gaugeDualRight, gDRByte);
}


void write7seg(){
  /* Move the stuff in memA to the appropriate
  location based on the first byte, if it makes sense.
  I don't yet know how to modify strings as arguments
  so for the mean time I'm using if/else
  */
  int n = 39;
  int led7 = 0;
  int digit7 = 0;
  boolean decPoint;
  while (n >= 0) {
   digit7 = 0 - (n % 8) + 7;
   
   if (n < 8) {
     led7 = 0; }
   else if (n > 7 && n < 16) {
     led7 = 1; }
   else if (n > 15 && n < 24) {
     led7 = 2; }
   else if (n > 23 && n < 32) {
     led7 = 3; }
   else if (n > 31 && n < 40) {
     led7 = 4; }
   else {
   }
      
   if (memA[n] >= 48 && memA[n] < 58) {
     //handle decimal points
     if (memA[(n / 8 * 8)] == ((n % 8) + 97) ||
           memA[(n / 8 * 8)] == ((n % 8) + 105)) {
       decPoint = true; }
     else {
       decPoint = false;}
     lc.setDigit(led7,digit7,(memA[n]-48),decPoint);
   }
   
   //handle minus signs
   else if (memA[n] == (45)) {
     lc.setChar(led7, digit7, '-', false);
   }
   
   else if (memA[n] == (97)) { //Display zero w/ decimal point
     lc.setDigit(led7,digit7,0,true);
   }
   
   else if (memA[n] == (105)) { //Display '-' w/ decimal point
     lc.setChar(led7, digit7, '-', true);
   }
   
   else if (memA[n] >= 106 && memA[n] <= 112)  {
     lc.setChar(led7, digit7, '-', false);
   }
   else { //Set the all segments of the digit blank
     lc.setLed(led7, digit7, 0, false);
     lc.setLed(led7, digit7, 1, false);
     lc.setLed(led7, digit7, 2, false);
     lc.setLed(led7, digit7, 3, false);
     lc.setLed(led7, digit7, 4, false);
     lc.setLed(led7, digit7, 5, false);
     lc.setLed(led7, digit7, 6, false);
     lc.setLed(led7, digit7, 7, false);
   }
   
   n--;
  }
}
void chk_buttons() {
  memB[0] = digitalRead(bPwrRed);
  memB[1] = digitalRead(bPwrYlw);
  memB[2] = digitalRead(bAnglGrn);
  memB[3] = digitalRead(bAnglYlw);
  memB[4] = digitalRead(bAnglRed);
  memB[5] = digitalRead(bAnglWht);
  memB[6] = digitalRead(bAnglBlu);
  memB[7] = 1 - digitalRead(sKey);
}


void buttonLEDs() {
  if (memB[7] == 1) {
    digitalWrite(lPwrRed, HIGH);
    digitalWrite(lPwrYlw, HIGH);
  }
  else {
    digitalWrite(lPwrRed, LOW);
    digitalWrite(lPwrYlw, LOW);
  }
}


void sendMemB() {
  Serial.print("[");
  for(int n=0; n<12; n++) {
    Serial.print((memB[n]));     
  }
  Serial.print("]");
}



//////////////////////////////////////////////////////////////////////////////////
void loop (){
st = millis();
 updateSerial();
 chk_buttons();
 buttonLEDs();
 sendMemB();

if (sleep_marker > 200) {
  write7seg();
  writeAnalog();
  sleep_marker = 0;
  //Serial.println( (char*)(memA)); //For debugging, print current buffer
  }


//Serial.println(dt);
//delay(100);
dt = st - millis();

/*if (sleep_marker > 150) {
  Serial.print(round((int)dt));
  Serial.write("\n");
  sleep_marker = 0;
 } */
 
sleep_marker += dt;
}


