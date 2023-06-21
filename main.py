import serial
import serial.tools.list_ports
import datetime
import time


# 42.654 N 83.233 W is the coordinates for CTC which is 282 meters above sea level
NEW_LATITUDE = 42.654
NEW_LONGITUDE = -83.233
NEW_ALTITUDE = 282  # meters

GPS_DEVICE_NAME = "Silicon Labs CP210x USB to UART Bridge"
GPS_DEVICE_BAUD = 115200
GPS_DEVICE_PORT = None  # if None then it will be automatically detected with GPS_DEVICE_NAME


def get_serial_port_by_device_name(device_name):
    for port in serial.tools.list_ports.comports():
        if port.description.startswith(device_name):
            return port.name


def send_commands_to_gps_from_file(filename):
    with (
        open(filename, 'r') as file,
        serial.Serial(port=GPS_DEVICE_PORT, baudrate=GPS_DEVICE_BAUD) as comport
    ):
        time.sleep(1)
        for line in file.readline():
            line = line.strip()
            line += "\r"
            comport.write(data=line.encode("UTF-8"))
            time.sleep(1)


def set_gps_starting_location_and_current_time():
    """
    This function sets the default time, date, and location for CLAW Simulator GPS
    """
    global GPS_DEVICE_PORT
    if GPS_DEVICE_PORT is None:
        GPS_DEVICE_PORT = get_serial_port_by_device_name(GPS_DEVICE_NAME)

    now = datetime.datetime.now()

    manual_mode_string = "SIM:MODE MANUAL"
    time_setting_string = f"SIMulation:TIME:START:TIME {now.hour},{now.minute},{now.second}"
    date_setting_string = f"SIMulation:TIME:START:DATE {now.year},{now.month},{now.day}"
    position_setting_string = f"SIMulation:POSition:LLH {NEW_LATITUDE},{NEW_LONGITUDE},{NEW_ALTITUDE}"

    commands = [manual_mode_string, time_setting_string, date_setting_string, position_setting_string]

    # opens a serial communication to the GPS device and sends the list of commands
    with serial.Serial(port=GPS_DEVICE_PORT, baudrate=GPS_DEVICE_BAUD) as comport:
        time.sleep(1)
        for command in commands:
            command += "\r"
            comport.write(data=command.encode("UTF-8"))
            time.sleep(1)


if __name__ == '__main__':
    set_gps_starting_location_and_current_time()
