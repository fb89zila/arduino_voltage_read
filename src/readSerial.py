from os import mkdir
from pathlib import Path
from time import sleep
import plotOutput as plt_out
import serial as ser
import json
import argparse

DEFAULT_SERIAL_PORT = '/dev/ttyACM0'
SERIAL_INIT_TIMEOUT = 4 # timeout before the first read in seconds
BYTE_LINES_TO_REMOVE = 0 # remove lines from the front of read bytes (in case of bad data)

def readSerial(serial_port : str) -> list:
    """Reads from given serial port.

    Args:
        serial_port (str, optional): Port of serial. Defaults to `DEFAULT_SERIAL_PORT`.

    Returns:
        list: List of strings. (format: `'start_time,end_time,volt1,volt2,...\\r\\n'`)
    """
    
    # create serial (!!! resets Board !!!)
    serial = ser.Serial(port=serial_port)
    
    # timeout for initialization (Board resets -> Serial contains bad data)
    sleep(SERIAL_INIT_TIMEOUT)
    
    byte_lines = []
    string_lines = []
    
    loop_num = 0
    read_num = 1
    
    try: # read from serial
        while True:
            if loop_num <= BYTE_LINES_TO_REMOVE:
                print("!WILL BE REMOVED!")
                loop_num += 1
            else:
                print("READ {}".format(read_num))
                read_num += 1

            serial_in = serial.readline()
            print(serial_in)
            byte_lines.append(serial_in)
    except KeyboardInterrupt: # press CTRL+C to decode the bytes
        byte_lines = byte_lines[BYTE_LINES_TO_REMOVE:]
        for byte_line in byte_lines:
            string_lines.append(byte_line.decode('utf-8'))
    
    return string_lines

def createDict(measurements : list) -> dict:
    """Create dict from measurements.

    Args:
        measurements (list): List of measurement strings. (format: `'start_time,end_time,volt1,volt2,...\\r\\n'`)

    Returns:
        dict: Dict of measurement dicts. (structure: `'measurement i' : {'start time', 'end_time', 'voltages'}`)
    """
    
    # remove newlines and split line into time and voltage
    measurements = [measurement.replace('\r', '').replace('\n', '').split(',') for measurement in measurements]
    
    # write data as json
    measurements_dict = {}
    measurement_number = 1
    for measurement in measurements:
        measurement_dict = {
            'start time' : int(measurement[0]),
            'end_time': int(measurement[1]),
            'voltages' : [float(volt) for volt in measurement[2:]]
        }
        
        measurements_dict["measurement {}".format(measurement_number)] = measurement_dict
        measurement_number += 1
        
    return measurement_dict

def saveJsonFile(measurements_dict : dict, file_path : Path):
    """Save measurements dict to a JSON file in given path.

    Args:
        measurements_dict (dict): Dict to write into the output file.
        file_path (Path): Where to save the output file.
    """
    
    # write dict to string
    json_data = json.dumps(measurements_dict)
    
    file_path.mkdir(parents=True, exist_ok=True)
    
    # write to file
    with open(file_path, "w") as file:
        file.write(json_data)

def plotMeasurements(measurements_dict : dict):
    """Plot all measurements from a dict.

    Args:
        measurements_dict (dict): Dict with measurements to plot. (structure: `'measurement i' : {'start time', 'end_time', 'voltages'}`)
    """
    
    measurement_list = []
    for measurement in measurements_dict.values():
        measurement_list.append(measurement)
    
    plt_out.plotMeasurements(measurement_list)

def main(args):
    """Start of the program.

    Args:
        args (argparse.Namespace): Namespace with arguments passed from the command-line.
    """
        
    # reading serial and creating dict from it
    measurements = readSerial(args.serial_port)
    measurements_dict = createDict(measurements)
    
    # save and plot measurements
    saveJsonFile(measurements_dict, args.output_path)
    plotMeasurements(measurements_dict)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter,
                                     description='Reads the serial and saves the measurements into a JSON file (also plots all measurements)'
                                     )
    parser.add_argument('-o', '--output', dest='output_path',
                        metavar='PATH',
                        help='Path where the output file should be saved. [default: "output-files/output.json"]',
                        type=Path,
                        default='output-files/output.json')
    parser.add_argument('-p', '--port', dest='serial_port',
                        metavar='PORT',
                        help='Port of serial. [default: "DEFAULT_SERIAL_PORT" constant in script]\n(eg. WIN: "COM3", Linux: "/dev/ttyACM0", macOS: "/dev/cu.usbmodem14101")',
                        type=str,
                        default=DEFAULT_SERIAL_PORT)
    args = parser.parse_args()
    
    main()
