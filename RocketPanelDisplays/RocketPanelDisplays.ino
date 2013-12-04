//This program sets an analog meter to various levels.
// wire 11 goes to right dual gauge
// wire 12 goes to left dual gauge
// wire 10 goes to vertical gauge

int gaugeDualLeft = 12;
int gaugeDualRight = 11;
int gaugeVertical = 10;


int met = 0; //Mission Elapsed Time
int valueDualLeft = 0;
int valueDualRight = 0;
int valueVertical = 0;

void setup (){
 pinMode(gaugeDualLeft, OUTPUT);
 pinMode(gaugeDualRight, OUTPUT);
 pinMode(gaugeVertical, OUTPUT);
 
 Serial.begin(9600); 

}

void loop (){
  if (Serial.available()) {
  //met = Serial.parseInt();
  valueDualLeft = Serial.parseInt(); //Looks for the next valid integer in the serial stream
  valueDualRight = Serial.parseInt();
  valueVertical = Serial.parseInt();
  }  
      // look for the newline
    if (Serial.read() == '\n') {
      // constrain the values to 0 - 255
      valueDualLeft = constrain(valueDualLeft, 0, 255);
      valueDualRight = constrain(valueDualRight, 0, 255);
      valueVertical = constrain(valueVertical, 0, 255);
      
      
      //Configure LiquidFuel for the Weird Gauge I have
      valueDualLeft = valueDualLeft*8/255;      
      //Configure Oxidizer for the Weird Gauge I have
      valueDualRight = valueDualRight*8/255;
      
      //Configure Rate of Climb for the Vertical Gauge I have
      valueVertical = valueVertical * 48/255 + 12;
      
      
      // Write the values to the display 
      analogWrite(gaugeDualLeft, valueDualLeft);
      analogWrite(gaugeDualRight, valueDualRight);
      analogWrite(gaugeVertical, valueVertical);
      
      // print the three numbers in one string as hexadecimal:
      Serial.print("Gauges updated");
  
  
    }
delay(20);
}


