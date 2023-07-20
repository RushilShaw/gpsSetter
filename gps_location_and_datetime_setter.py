import sys
import time
import json
import serial
import pathlib
import serial.tools.list_ports
from datetime import datetime, timezone


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
    longitude_degrees, latitude_degrees, altitude_meters = new_location

    gps_commands = [
        "SIM:POS:MODE FIXED",
        "SIM:TIME:MODE ASSIGN",
        "SIM:MODE SIM",
        "SIM:COM START",
        f"SIMulation:TIME:START:TIME {new_datetime.hour},{new_datetime.minute},{new_datetime.second}",
        f"SIMulation:TIME:START:DATE {new_datetime.year},{new_datetime.month},{new_datetime.day}",
        f"SIMulation:POSition:LLH {longitude_degrees},{latitude_degrees},{altitude_meters}",
    ]

    # opens a serial communication to the GPS device and sends the list of commands
    with serial.Serial(port=gps_device_port, baudrate=gps_baudrate) as comport:
        time.sleep(1)
        for command in gps_commands:
            command += "\r"
            comport.write(data=command.encode("UTF-8"))
            time.sleep(1)


def main():
    gps_port = GPS_DEVICE_PORT
    if gps_port is None:
        gps_port = get_serial_port_by_device_name(GPS_DEVICE_NAME)

    config_filepath: pathlib.Path
    # if an argument was specified, use the argument for config_filepath instead of the default filepath
    if len(sys.argv) >= 2:
        filepath = sys.argv[1]
        if not filepath.endswith(".json"):
            raise ValueError("Specified path must be a .json")
        config_filepath = pathlib.Path(filepath)
    else:
        config_filepath = DEFAULT_FILEPATH

    if not config_filepath.is_file():
        raise FileNotFoundError(f"{config_filepath.absolute()} is not a file.")

    with open(config_filepath, 'r') as file:
        config = json.load(file)

    new_location = [config["LATITUDE_DEGREES"], config["LONGITUDE_DEGREES"], config["ALTITUDE_METERS"]]
    new_datetime_from_json = config.get("DATETIME_ISO_8601")

    if not new_datetime_from_json:
        new_datetime = datetime.now(timezone.utc)
    else:
        new_datetime = datetime.fromisoformat(new_datetime_from_json)

    set_gps_location_and_time(gps_device_port=gps_port, gps_baudrate=GPS_DEVICE_BAUD,
                              new_location=new_location, new_datetime=new_datetime)


if __name__ == '__main__':
    main()
