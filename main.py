import serial
import serial.tools.list_ports
import datetime
import time


STARTING_LATITUDE = 42.654  # 42.654 is the starting LAT for CTC
STARTING_LONGITUDE = -83.233  # 83.233 is the starting LON for CTC
STARTING_ALTITUDE = 282  # (in meters) 282 is the starting ALT for CTC

PORT = ""
BAUD = 115200
NAME = "Silicon Labs CP210x USB to UART Bridge"


def get_serial_port_location_by_name(device_name):
    for port in serial.tools.list_ports.comports():
        if port.description.startswith(device_name):
            return port.name


def run_locations(filename):
    with (
        open(filename, 'r') as file,
        serial.Serial(port=PORT, baudrate=BAUD) as ser
    ):
        for line in file.readline():
            line = line.strip()
            line += "\r"
            ser.write(data=line.encode("UTF-8"))
            time.sleep(0.5)
            bytes_to_read = ser.inWaiting()
            response = ser.read(bytes_to_read)
            print(response.decode())
            time.sleep(0.5)
            ser.write(data=line.encode("UTF-8"))


def main():
    """
    This function sets the default time, date, and location for CLAW Simulator GPS
    """
    global PORT
    if PORT is None:
        PORT = get_serial_port_location_by_name(NAME)

    now = datetime.datetime.now()

    manual_setting_string = "SIM:MODE MANUAL"
    time_setting_string = f"SIMulation:TIME:START:TIME {now.hour},{now.minute},{now.second}"
    date_setting_string = f"SIMulation:TIME:START:DATE {now.year},{now.month},{now.day}"
    position_setting_string = f"SIMulation:POSition:LLH {STARTING_LATITUDE},{STARTING_LONGITUDE},{STARTING_ALTITUDE}"

    commands = [manual_setting_string, time_setting_string, date_setting_string, position_setting_string]

    with serial.Serial(port=PORT, baudrate=BAUD) as ser:
        time.sleep(0.5)
        for command in commands:
            command += "\r"
            ser.write(data=command.encode("UTF-8"))
            time.sleep(0.5)
            bytes_to_read = ser.inWaiting()
            response = ser.read(bytes_to_read)
            print(response.decode())
            time.sleep(0.5)


if __name__ == '__main__':
    main()
