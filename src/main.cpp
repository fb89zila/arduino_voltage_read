#include <Arduino.h>
#include <stdint.h>

#define MAX_READS 100
#define ANALOG_READ_DELAY_MICRO_SECONDS 980

unsigned long time_start = 0; // 8 byte
unsigned long time_end = 0; // 8 byte

uint16_t output_AC_DC[MAX_READS] = {0}; // MAX_READS * 2 bytes
float voltages[MAX_READS] = {0}; // MAX_READS * 4 bytes

const uint8_t analog_pin = A0; // 1 byte

void setup()
{
  Serial.begin(9600); // Initialize Serial with 9600 baud rate
  pinMode(analog_pin, INPUT); // read mode on analog_pin
}

void loop()
{
  time_start = micros(); // start time in micro seconds

  for (int i = 0; i < MAX_READS; i++)
  {
    output_AC_DC[i] = (uint16_t) analogRead(analog_pin); // ~100 micro sec for read
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