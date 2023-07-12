import serial
import serial.tools.list_ports
import datetime
import time


# 42.654 N 83.233 W is the coordinates for CTC which is 282 meters above sea level
NEW_LATITUDE = 42.654
NEW_LONGITUDE = -83.233
NEW_ALTITUDE_METERS = 282.0

# if None then the current computer time will be used. To insert a custom time use a datetime.datetime() object in UTC
NEW_TIME = None

GPS_DEVICE_NAME = "Silicon Labs CP210x USB to UART Bridge"
GPS_DEVICE_BAUD = 115200
GPS_DEVICE_PORT = None  # if None then it will be automatically detected with GPS_DEVICE_NAME


def get_serial_port_by_device_name(device_name: str):
    for port in serial.tools.list_ports.comports():
        if port.description.startswith(device_name):
            return port.name


def send_commands_to_gps_from_file(filename: str):
    with (
        open(filename, 'r') as file,
        serial.Serial(port=GPS_DEVICE_PORT, baudrate=GPS_DEVICE_BAUD) as comport
    ):
        time.sleep(1)
        for line in file.readline():
            comport.write(data=line.encode("UTF-8"))
            time.sleep(1)


def set_gps_location_and_time(gps_device_port: str, gps_baudrate: int,
                              new_location: list[float, float, float], new_datetime: datetime.datetime) -> None:

    longitude, latitude, altitude = new_location

    gps_commands = [
        "SIM:COM START",
        "SIM:POS:MODE FIXED",
        f"SIMulation:TIME:START:TIME {new_datetime.hour},{new_datetime.minute},{new_datetime.second}",
        f"SIMulation:TIME:START:DATE {new_datetime.year},{new_datetime.month},{new_datetime.day}",
        f"SIMulation:POSition:LLH {longitude},{latitude},{altitude}",
        "SIM:COM STOP"
    ]

    # opens a serial communication to the GPS device and sends the list of commands
    with serial.Serial(port=gps_device_port, baudrate=gps_baudrate) as comport:
        time.sleep(1)
        for command in gps_commands:
            command += "\r"
            comport.write(data=command.encode("UTF-8"))
            time.sleep(1)


if __name__ == '__main__':
    if GPS_DEVICE_PORT is None:
        GPS_DEVICE_PORT = get_serial_port_by_device_name(GPS_DEVICE_NAME)

    NEW_LOCATION = [NEW_LONGITUDE, NEW_LATITUDE, NEW_ALTITUDE_METERS]

    if NEW_TIME is None:
        NEW_TIME = datetime.datetime.now(datetime.timezone.utc)

    set_gps_location_and_time(gps_device_port=GPS_DEVICE_PORT, gps_baudrate=GPS_DEVICE_BAUD,
                              new_location=NEW_LOCATION, new_datetime=NEW_TIME)
