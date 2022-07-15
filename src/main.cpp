#include <Arduino.h>

#define MAX_READS 100 // max. 306 - use 100/200 to be safe
#define ANALOG_READ_DELAY_MICRO_SECONDS 980

unsigned long time_start = 0;
unsigned long time_end = 0;

unsigned short output_AC_DC[MAX_READS] = {0}; // MAX_READS * 2 bytes
float voltages[MAX_READS] = {0}; // MAX_READS * 4 bytes

void setup()
{
  Serial.begin(9600); // Initialize Serial with 9600 baud rate
  pinMode(A0, INPUT); // read mode on analog_pin
}

void loop()
{
  time_start = micros(); // start time in micro seconds

  for (int i = 0; i < MAX_READS; i++)
  {
    output_AC_DC[i] = (unsigned short) analogRead(A0); // ~100 micro sec for read
    delayMicroseconds(ANALOG_READ_DELAY_MICRO_SECONDS); // delay for better sine curve
  }

  time_end = micros(); // end time in micro seconds

  for (int j = 0; j < MAX_READS; j++)
    voltages[j] = (output_AC_DC[j] * 5) / 1023.0; // voltage (>0) in V (5V UNO operating voltage, 1024 resolution)
  
  // print everything into the serial
  Serial.print(time_start);
  Serial.print(",");
  Serial.print(time_end);
  Serial.print(",");
  for (int k = 0; k < MAX_READS; k++)
  {
    Serial.print(voltages[k]);
    if (k != MAX_READS-1)
      Serial.print(",");
  }
  Serial.println();
}