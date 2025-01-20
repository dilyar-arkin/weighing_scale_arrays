#include "HX711.h"

// Define pin pairs for 5 load cells
const int LOADCELL1_DOUT_PIN = 2;
const int LOADCELL1_SCK_PIN = 3;

const int LOADCELL2_DOUT_PIN = 4;
const int LOADCELL2_SCK_PIN = 5;

const int LOADCELL3_DOUT_PIN = 6;
const int LOADCELL3_SCK_PIN = 7;

const int LOADCELL4_DOUT_PIN = 8;
const int LOADCELL4_SCK_PIN = 9;

const int LOADCELL5_DOUT_PIN = 10;
const int LOADCELL5_SCK_PIN = 11;

// Create HX711 objects for each load cell
HX711 scale1, scale2, scale3, scale4, scale5;

void setup() {
  Serial.begin(57600);
  
  // Initialize each scale with timeout handling
  if (!initializeScale(scale1, LOADCELL1_DOUT_PIN, LOADCELL1_SCK_PIN, 2000)) {
    Serial.println("HX711 1 initialization failed. Check wiring or hardware.");
    //while (true); // Halt further execution if initialization fails
  }
  if (!initializeScale(scale2, LOADCELL2_DOUT_PIN, LOADCELL2_SCK_PIN, 2000)) {
    Serial.println("HX711 2 initialization failed. Check wiring or hardware.");
    //while (true); // Halt further execution if initialization fails
  }
  if (!initializeScale(scale3, LOADCELL3_DOUT_PIN, LOADCELL3_SCK_PIN, 2000)) {
    Serial.println("HX711 3 initialization failed. Check wiring or hardware.");
    //while (true); // Halt further execution if initialization fails
  }
  if (!initializeScale(scale4, LOADCELL4_DOUT_PIN, LOADCELL4_SCK_PIN, 2000)) {
    Serial.println("HX711 4 initialization failed. Check wiring or hardware.");
    //while (true); // Halt further execution if initialization fails
  }
  if (!initializeScale(scale5, LOADCELL5_DOUT_PIN, LOADCELL5_SCK_PIN, 2000)) {
    Serial.println("HX711 5 initialization failed. Check wiring or hardware.");
    //while (true); // Halt further execution if initialization fails
  }

  Serial.println("All HX711 scales initialized successfully.");
}

void loop() {
  // Try to get a reading with a timeout for each scale
  long reading1 = getSensorReading(scale1, 1000);
  long reading2 = getSensorReading(scale2, 1000);
  long reading3 = getSensorReading(scale3, 1000);
  long reading4 = getSensorReading(scale4, 1000);
  long reading5 = getSensorReading(scale5, 1000);

  // Print all the sensor values at once
  Serial.print("Loadcell 1: ");
  Serial.print(reading1);
  Serial.print(" | Loadcell 2: ");
  Serial.print(reading2);
  Serial.print(" | Loadcell 3: ");
  Serial.print(reading3);
  Serial.print(" | Loadcell 4: ");
  Serial.print(reading4);
  Serial.print(" | Loadcell 5: ");
  Serial.println(reading5);

  delay(1500);  // Delay before the next reading
}

// Function to initialize the HX711 scale with a timeout
bool initializeScale(HX711 &scale, int doutPin, int sckPin, unsigned long timeout) {
  Serial.print("Initializing HX711...");
  scale.begin(doutPin, sckPin);
  
  // Wait for HX711 to be ready with the provided timeout
  if (scale.wait_ready_timeout(timeout)) {
    Serial.println("HX711 ready.");
    Serial.print("read average: \t\t");
    Serial.println(scale.read_average(20));       // print the average of 20 readings from the ADC

    Serial.print("get value: \t\t");
    Serial.println(scale.get_value(5));		// print the average of 5 readings from the ADC minus the tare weight, set with tare()

    Serial.print("get units: \t\t");
    Serial.println(scale.get_units(5), 1);        // print the average of 5 readings from the ADC minus tare weight, divided
                                                  // by the SCALE parameter set with set_scale 
    scale.set_scale(2280.f);    // this value is obtained by calibrating the scale with known weights; see the README for details
    scale.tare();				        // reset the scale to 0           
    
    Serial.print("read: \t\t");
    Serial.println(scale.read());                 // print a raw reading from the ADC

    Serial.print("read average: \t\t");
    Serial.println(scale.read_average(20));       // print the average of 20 readings from the ADC

    Serial.print("get value: \t\t");
    Serial.println(scale.get_value(5));		// print the average of 5 readings from the ADC minus the tare weight, set with tare()

    Serial.print("get units: \t\t");
    Serial.println(scale.get_units(5), 1);        // print the average of 5 readings from the ADC minus tare weight, divided
              // by the SCALE parameter set with set_scale                                   
    return true;  // Successfully initialized
  } else {
    Serial.println("HX711 initialization failed.");
    return false;  // Initialization failed
  }
}

// Function to get a sensor reading with timeout handling
long getSensorReading(HX711 &scale, unsigned long timeout) {
  if (scale.wait_ready_timeout(timeout)) {
    return scale.get_units(10);  // Return the reading if ready
  } else {
    Serial.println("HX711 reading timed out.");
    return 0;  // Return 0 if reading times out
  }
}
