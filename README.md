# GPS Location and Time Setter

This script is used to set the GPS location and time on a GPS device using a serial connection.
It reads the configuration from a JSON file and sends the necessary commands to the GPS device to set the new location and time.

## Prerequisites

- Python 3.x
- `pyserial` library (install using `pip install pyserial`)

## Usage

1. Ensure that the GPS device is connected to the computer via a serial port.
2. Create a JSON configuration file with the desired GPS location and time. The file should have the following structure:

```json
{
  "LATITUDE_DEGREES": <latitude>,
  "LONGITUDE_DEGREES": <longitude>,
  "ALTITUDE_METERS": <altitude>,
  "DATETIME_ISO_8601": "<YYYY-MM-DD HH:MM:SS>"
}
```

- `LATITUDE_DEGREES`: The new latitude value in decimal degrees.
- `LONGITUDE_DEGREES`: The new longitude value in decimal degrees.
- `ALTITUDE_METERS`: The new altitude value in meters.
- `DATETIME_ISO_8601`: (Optional) The new date and time in UTC to set on the GPS device. If not provided, the current date and time will be used.

3. Run the script by executing the following command in the terminal:

```bash
python gps_location_and_datetime_setter.py <config_file.json>
```

- Replace `<config_file.json>` with the path to your JSON configuration file.

## Configuration

The script provides some configurable parameters at the beginning of the code:

- `DEFAULT_FILEPATH`: The default path to the JSON configuration file if not provided as a command-line argument.
- `GPS_DEVICE_NAME`: The name of the GPS device. Modify this value if your GPS device has a different name.
- `GPS_DEVICE_BAUD`: The baud rate for the GPS device. Modify this value if your GPS device requires a different baud rate.
- `GPS_DEVICE_PORT`: The serial port of the GPS device. If set to `None`, the script will automatically detect the port based on the device name.
