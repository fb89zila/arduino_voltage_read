from pathlib import Path
import matplotlib.pyplot as plt
import json
import numpy as np
import argparse

def readFile(file_path = Path) -> dict:
    """Read given JSON-file.

    Args:
        file_path (pathlib.Path, optional): File path to JSON-file.

    Returns:
        dict: JSON-formated dict
    """

    with open(file_path, 'r') as file:
        json_data = json.load(file)

    return json_data

def plotSingleMeasurement(start_time : int, end_time : int, voltages : list):
    """Plot one measurement.

    Args:
        start_time (int): Time of first voltage value.
        end_time (int): Time of last voltage value.
        voltages (list): List of voltage values.
    """

    time = np.linspace(start_time / 1000, end_time / 1000, len(voltages))

    plt.plot(time, voltages)

def plotMeasurements(measurement_list : list, voltage_offset : float, list_pos: int = -1):
    """Defines plot figure and plots all or one specific measurement.

    Args:
        measurement_list (list[dict]): List of measurement dicts. (keys: `'start time', 'end_time', 'voltages'`)
        voltage_offset (int, optional): Offset to substract from voltage values.
        list_pos (int, optional): Index of specific `measurement` in `measurement_list`. Defaults to `-1`.
    """

    plt.gcf().canvas.set_window_title('Voltage-Time Curve')

    # label for axes
    plt.xlabel('Time in $ms$')
    plt.ylabel('Voltage in $V$')
    
    # show grid in light grey
    plt.grid(True, color='#BBBBBB', linestyle=':')
    
    # plot the measurement given in with the '-m' measurement or all if it is below 1
    if list_pos < 0:
        first_start_time = measurement_list[0]['start time']
        for measurement in measurement_list:
            plotSingleMeasurement(measurement['start time']-first_start_time,
                                  measurement['end_time']-first_start_time,
                                  [volt - voltage_offset for volt in measurement['voltages']])
    else:
        plotSingleMeasurement(0,
                              measurement_list[list_pos]['end_time'] - measurement_list[list_pos]['start time'],
                              [volt - voltage_offset for volt in measurement_list[list_pos]['voltages']])

    plt.show()

def main(args : argparse.Namespace):
    """Start of the program.

    Args:
        args (argparse.Namespace): Namespace with arguments passed from the command-line.
    """
    
    json_data = readFile(args.input_path)
    
    # map all measurements into a list
    measurement_list = []
    for measurement_i in json_data.values():
        measurement_list.append(measurement_i)

    list_pos = args.m_num - 1

    # error message if '-m' argument is larger than the number of measurements
    if (args.m_num > len(measurement_list)):
        print('Measurement {} not found: measurement {} is the last entry in {}'.format(args.m_num, len(measurement_list), str(args.input_path)))
    else:
        plotMeasurements(measurement_list, args.u_offset, list_pos)
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter,
                                     description='Plots measurements from a JSON file.\nEither plots all measurements or a specific one.'
                                     )
    parser.add_argument('-i', '--input', dest='input_path',
                        help='Path to input file. [default: output-files/output.json]',
                        type=Path,
                        default='output-files/output.json')
    parser.add_argument('-o', '--offset', dest='u_offset',
                        help='Offset of the voltage. [default: 0.0]',
                        type=float,
                        default=0.0)
    parser.add_argument('-m', '--measurement', dest='m_num',
                        help='Measurement to be plotted. [default: 0]\n(If <1 all measurements are plotted.)',
                        type=int,
                        default=0)
    args = parser.parse_args()
    
    main(args)
