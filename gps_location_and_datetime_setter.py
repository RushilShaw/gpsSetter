import json
import sys
import pathlib
import serial
import serial.tools.list_ports
from datetime import datetime, timezone
import time

DEFAULT_FILEPATH = pathlib.Path("config.json")

GPS_DEVICE_NAME = "Silicon Labs CP210x USB to UART Bridge"
GPS_DEVICE_BAUD = 115200
GPS_DEVICE_PORT = None  # if None then it will be automatically detected with GPS_DEVICE_NAME


def get_serial_port_by_device_name(device_name: str):
    for port in serial.tools.list_ports.comports():
        if port.description.startswith(device_name):
            return port.name


def set_gps_location_and_time(gps_device_port: str, gps_baudrate: int,
                              new_location: list[float, float, float], new_datetime: datetime) -> None:
    return
    longitude, latitude, altitude = new_location

    gps_commands = [
        "SIM:POS:MODE FIXED",
        "SIM:MODE SIM",
        "SIM:COM START",
        f"SIMulation:TIME:START:TIME {new_datetime.hour},{new_datetime.minute},{new_datetime.second}",
        f"SIMulation:TIME:START:DATE {new_datetime.year},{new_datetime.month},{new_datetime.day}",
        f"SIMulation:POSition:LLH {longitude},{latitude},{altitude}",
    ]

    # opens a serial communication to the GPS device and sends the list of commands
    with serial.Serial(port=gps_device_port, baudrate=gps_baudrate) as comport:
        time.sleep(1)
        for command in gps_commands:
            command += "\r"
            comport.write(data=command.encode("UTF-8"))
            time.sleep(1)


def main():
    global DEFAULT_FILEPATH, GPS_DEVICE_PORT, GPS_DEVICE_BAUD, GPS_DEVICE_NAME

    filepath = DEFAULT_FILEPATH
    if len(sys.argv) >= 2:
        filename = sys.argv[1]
        if not filename.endswith(".json"):
            raise ValueError("Specified path must be a .json")
        filepath = pathlib.Path(filename)

    if not filepath.is_file():
        raise FileNotFoundError(f"{filepath.absolute()} is not a file.")

    with open(filepath, 'r') as file:
        data = json.load(file)

    if GPS_DEVICE_PORT is None:
        GPS_DEVICE_PORT = get_serial_port_by_device_name(GPS_DEVICE_NAME)

    new_location = [data["LATITUDE"], data["LONGITUDE"], data["ALTITUDE_METERS"]]
    new_datetime_from_json = data.get("DATETIME")

    if not new_datetime_from_json:
        new_datetime = datetime.now(timezone.utc)
    else:
        new_datetime = datetime.fromisoformat(new_datetime_from_json)

    set_gps_location_and_time(gps_device_port=GPS_DEVICE_PORT, gps_baudrate=GPS_DEVICE_BAUD,
                              new_location=new_location, new_datetime=new_datetime)

    print(new_datetime)
    print(filepath)
    print(GPS_DEVICE_PORT)

if __name__ == '__main__':
    main()
