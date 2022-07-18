# Description
All the code was written for an **Arduino UNO rev3 (ATmega328P microcontroller)**.

## C++ source code file `main.cpp`
Reads the `A0` pin and writes data to the serial. (PlatformIO was used to compile and upload)  
For more information about the Analog-to-Digital converter and other details about the definitions and functions in the code can be found [here](https://github.com/fb89zila/arduino_voltage_read/wiki/EN).

## Python script `readSerial.py`
Reads the serial and saves the measurements into a JSON file (also plots all measurements)

### Command line arguments (optional):
|argument|description|
|:-|:-:|
|`-h, --help`|show help message|
|`-o, --output PATH`|Path where the output file should be saved.</br> [default: `output-files/output.json`]|
|`-p, --port PORT`|Port of serial.</br>(WIN: `COM3`, Linux: `/dev/ttyACM0`, macOS: `/dev/cu.usbmodem14101`)</br>[default: `DEFAULT_SERIAL_PORT` constant in script]|

## Python script `plotOutput.py`
Plots measurements from a JSON file. Either plots all measurements or a specific one.

### Command line arguments (optional):
|argument|description|
|:-|:-:|
|`-h, --help`|show help message|
|`-i, --input PATH`|Path to input file.</br>[default: `output-files/output.json`]|
|`-o, --offset OFFSET`|Offset of the measured voltage.</br>[default: `0.0`]|
|`-m, --measurement M_NUM`|Measurement to be plotted.</br>(`M_NUM < 1`: all measurements are plotted.)</br>[default: `0`]|
