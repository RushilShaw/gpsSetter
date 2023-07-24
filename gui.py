import tkinter
from tkcalendar import Calendar
import gps_location_and_datetime_setter


GPS_DEVICE_NAME = gps_location_and_datetime_setter.GPS_DEVICE_NAME
GPS_DEVICE_BAUD = gps_location_and_datetime_setter.GPS_DEVICE_BAUD
GPS_DEVICE_PORT = gps_location_and_datetime_setter.GPS_DEVICE_PORT


class MyWindow:
    def __init__(self, win, title):
        self.window = win
        self.title = title
        boxes = [
            "LATITUDE_DEGREES",
            "LONGITUDE_DEGREES",
            "ALTITUDE_METERS",
        ]

        self.label_entry_dict = {}
        index = 0
        for index, name in enumerate(boxes):
            tkinter.Label(self.window, text=f'{name}: ').place(x=10, y=10 + 25 * index)
            entry_box = tkinter.Entry(self.window, show="")
            entry_box.place(x=150, y=10 + 25 * index)
            self.label_entry_dict[name] = entry_box

        cal = Calendar(self.window, selectmode='day',
                       year=2020, month=5,
                       day=22)

        cal.pack(pady=20)

        tkinter.Button(self.window, text='Run', fg='black', bg='white',
                       command=self.run, height=1, width=7).place(x=150, y=10 + 25 * (index + 1))

    def run(self):
        print(True)

    def start(self, geometry):
        self.window.geometry(geometry)
        self.window.mainloop()


if __name__ == '__main__':
    gps_port = GPS_DEVICE_PORT
    if gps_port is None:
        gps_port = gps_location_and_datetime_setter.get_serial_port_by_device_name(GPS_DEVICE_NAME)

    window = tkinter.Tk()
    my_win = MyWindow(window, 'Hello Python')
    window.configure(bg="white")
    my_win.start("400x300+10+10")
