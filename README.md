# Description
All the code was written for an **Arduino UNO rev3**.

## C++ source code file `main.cpp`
Reads the A0 pin and writes data to the serial. (PlatformIO was used to compile and upload)

## Python script `readSerial.py`
Reads the serial and saves the measurements into a JSON file (also plots all measurements)

## Python script `plotOutput.py`
Plots measurements from a JSON file.  
Either plots all measurements or a specific one.
