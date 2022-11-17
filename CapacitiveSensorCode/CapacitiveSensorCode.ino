// Import libraries for MPR121 and I2C:
#include <Wire.h>
#include "Adafruit_MPR121.h"

// Initialize sensor object:
Adafruit_MPR121 cap = Adafruit_MPR121();

// Initialize timestamp variable
long msec;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  Serial.setTimeout(1);

  // Default address is 0x5A, if tied to 3.3V its 0x5B
  // If tied to SDA its 0x5C and if SCL then 0x5D
  if (!cap.begin(0x5A)) {
    Serial.println("MPR121 not found, check wiring?");
    while (1);
  }

  Serial.println("Time(ms),Cap0,Cap1,Cap2,Cap3,Cap4,Cap5,Cap6,Cap7,Cap8,Cap9,Cap10,Cap11"); // Header for .csv
}

void loop() {
  // put your main code here, to run repeatedly:
  msec = millis();
  Serial.print(msec);
  Serial.print(',');

  for (uint8_t i = 0; i < 12; i++) {
    Serial.print(cap.filteredData(i));
    Serial.print(',');
  }

  Serial.println();
  delay(10); 

}
