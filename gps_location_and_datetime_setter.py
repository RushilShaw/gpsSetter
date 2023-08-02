import sys
import json
import pathlib
import GpsUtils
from datetime import datetime, timezone


def get_config(**kwargs) -> tuple[list[float, float, float], str]:
    """
    get_config func: if the kwargs argument is empty then the first command line argument (argv)
    will be used the filepath a json file of the configuration variables necessary
    """
    if not kwargs:
        filepath = sys.argv[1]
        if not filepath.endswith(".json"):
            raise ValueError("Specified path must be a .json")
        config_file = pathlib.Path(filepath)

        if not config_file.is_file():
            raise FileNotFoundError(f"{config_file.absolute()} is not a file.")

        with open(config_file, 'r') as file:
            config = json.load(file)

    else:
        config = kwargs

    new_location = [config["LATITUDE_DEGREES"], config["LONGITUDE_DEGREES"], config["ALTITUDE_METERS"]]
    new_datetime_iso_8601 = config.get("DATETIME_ISO_8601")

    return new_location, new_datetime_iso_8601


def generate_commands(new_location: list[float, float, float], new_datetime_iso_8601: str) -> list[str]:
    """
    generate_commands func: creates a list of the commands needed to set the new location and datetime on the
    CLAW simulation GPS
    """
    longitude_degrees, latitude_degrees, altitude_meters = new_location

    if not new_datetime_iso_8601:
        new_datetime = datetime.now(timezone.utc)
    else:
        new_datetime = datetime.fromisoformat(new_datetime_iso_8601)

    gps_commands = [
        "SIM:MODE MANUAL",
        "SIM:POS:MODE FIXED",
        "SIM:TIME:MODE ASSIGN",
        "SIM:COM START",
        "OUT:POW -110",
        f"SIMulation:TIME:START:TIME {new_datetime.hour},{new_datetime.minute},{new_datetime.second}",
        f"SIMulation:TIME:START:DATE {new_datetime.year},{new_datetime.month},{new_datetime.day}",
        f"SIMulation:POSition:LLH {longitude_degrees},{latitude_degrees},{altitude_meters}",
    ]
    return gps_commands


def main(**kwargs):
    gps = GpsUtils.ClawGPSSimulator()
    new_location, new_datetime_iso_8601 = get_config(**kwargs)
    commands = generate_commands(new_location, new_datetime_iso_8601)
    gps.stream_list_of_commands(commands)


if __name__ == '__main__':
    main()
