import Tkinter as tk
from Tkinter import Label, Frame
import datetime
import requests
import time
IP_ADDR ="192.168.1.74"
class Application(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.master = master
        self.pack()
        self.create_widgets()

    def write_to_log(self, data):
        with open('/home/pi/log.txt', 'a') as file:
            file.write('written {}\n{}\n'.format(datetime.datetime.now(), data))

    def handle_errors(self, e):
        print('Exception: {}'.format(e))
        self.write_to_log(e)

    def lights_off(self):
        try:
            requests.get('http://{}:8080/lights-off'.format(IP_ADDR))
        except Exception as e:
            self.handle_errors(e)

    def lights_on(self):
        try:
            requests.get('http://{}:8080/lights-on'.format(IP_ADDR))
        except Exception as e:
            self.handle_errors(e)
    def start_motion(self):
	try:
	    print("starting motion sensor in 30 seconds")
	    time.sleep(30)
	    print("starting")
	    requests.get('http://{}:5000/start_motion_sensor'.format(IP_ADDR))
	except Exception as e:
	    self.handle_errors(e)

    def stop_motion(self):
	try:
	    print("Stopping motion sensors")
	    requests.get('http://{}:5000/stop_motion_sensor'.format(IP_ADDR))
	except Exception as e:
	    self.handle_errors(e)


    def create_widgets(self):
        self.lights_off_button = tk.Button(self, padx='50', pady='25')
        self.lights_on_button = tk.Button(self, padx='50', pady='25')

        self.motion_off_button = tk.Button(self, padx='50', pady='25')
        self.motion_on_button = tk.Button(self, padx='50', pady='25')

	self.motion_on_button["text"] = "Motion On"
	self.motion_on_button["command"] = self.start_motion


	self.motion_off_button["text"] = "Motion Off"
	self.motion_off_button["command"] = self.stop_motion


	self.lights_off_button["text"] = "Lights Off"
        self.lights_off_button["command"] = self.lights_off

	self.lights_on_button["text"] = "Lights On"
        self.lights_on_button["command"] = self.lights_on

	self.lights_on_button.pack(side="top")
        self.lights_off_button.pack(side="top")
        self.motion_off_button.pack(side="top")
        self.motion_on_button.pack(side="top")

	self.quit = tk.Button(self, text="QUIT", fg="red",
                                  command=self.master.destroy,
                                  padx='50', pady='50')
        self.quit.pack(side="bottom")

root = tk.Tk()
root.title('Light Controls')

root.resizable(0,0)

Label(text="Light Controls").pack()

separator = Frame(bd=1, background='black', relief='sunken')
separator.pack(fill='both', padx=5, pady=5)
liner = Frame(bd=1)
liner.pack(fill='both', side="bottom", pady=5)

app = Application(master=root)
app.mainloop()

