import serial
import datetime
import sys
import glob


STARTING_LATITUDE = 42.654361
STARTING_LONGITUDE = -83.23361
STARTING_ALTITUDE = 282  # meters

PORT = ""
BAUDRATE = 115200
NAME = ""


def get_serial_port_location_by_serial_number(serial_number):
    for port in serial.tools.list_ports.comports():
        if port.serial_number == serial_number:
            return port.location


def get_serial_port_location_by_name(device_name):
    for port in serial.tools.list_ports.comports():
        if device_name in port.name:
            return port.location



def serial_ports():
    """ Lists serial port names

        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
    """
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result


def run_locations(filename):
    with (
        open(filename, 'r') as file,
        serial.Serial(port=PORT, baudrate=BAUDRATE) as ser
    ):
        line = file.readline()
        ser.write(data=line.encode("UTF-8"))


def main():
    """
    This function sets the default time, date, and location for CLAW Simulator GPS
    """
    now = datetime.datetime.now()
    time_setting_string = f"SIMulation:TIME:START:TIME {now.hour},{now.minute},{now.second}"
    date_setting_string = f"SIMulation:TIME:START:DATE {now.year},{now.month},{now.day}"  # TODO Does this need z-fill
    position_setting_string = f"SIMulation:POSition:LLH {STARTING_LATITUDE},{STARTING_LONGITUDE},{STARTING_ALTITUDE}"

    # the GPS requires 8-N-1 which is default the baud rate required is 115200
    # https://en.wikipedia.org/wiki/8-N-1
    with serial.Serial(port=PORT, baudrate=BAUDRATE) as ser:
        for string in [time_setting_string, date_setting_string, position_setting_string]:
            ser.write(data=string.encode("UTF-8"))


if __name__ == '__main__':
    main()
