import Tkinter as tk
from Tkinter import Label, Frame
import datetime
import requests
import time
import sys

args = sys.argv
bedroom_ip = args[1]
livingroom_ip = args[2]
port = args[3]
COMMANDS = {}
COMMANDS['OFF'] = 'off'
COMMANDS['ON'] = 'on'

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

    def light_handler(self, ip, command):
        try:
            requests.get('http://{}:{}/lights-{}'.format(ip, port, command))
        except Exception as e:
            self.handle_errors(e)

    def bedroom_lights_on(self):
        self.light_handler(bedroom_ip, COMMANDS['ON'])

    def bedroom_lights_off(self):
        self.light_handler(bedroom_ip, COMMANDS['OFF'])

    def livingroom_lights_on(self):    
        self.light_handler(livingroom_ip, COMMANDS['ON'])

    def livingroom_lights_off(self):
        self.light_handler(livingroom_ip, COMMANDS['OFF'])

            #TODO Reimplement this when PIRs back in place
 #    def start_motion(self):
    # try:
    #     print("starting motion sensor in 30 seconds")
    #     time.sleep(30)
    #     print("starting")
    #     requests.get('http://{}:5000/start_motion_sensor'.format(IP_ADDR))
    # except Exception as e:
    #     self.handle_errors(e)

 #    def stop_motion(self):
    # try:
    #     print("Stopping motion sensors")
    #     requests.get('http://{}:5000/stop_motion_sensor'.format(IP_ADDR))
    # except Exception as e:
    #     self.handle_errors(e)


    def create_widgets(self):
        self.bedroom_lights_off_button = tk.Button(self, padx='50', pady='25')
        self.bedroom_lights_on_button = tk.Button(self, padx='50', pady='25')
        self.livingroom_lights_off_button = tk.Button(self, padx='50', pady='25')
        self.livingroom_lights_on_button = tk.Button(self, padx='50', pady='25')
        # self.motion_off_button = tk.Button(self, padx='50', pady='25')
        # self.motion_on_button = tk.Button(self, padx='50', pady='25')

        self.bedroom_lights_on_button["text"] = "Bedroom ON"
        self.bedroom_lights_on_button["command"] = self.bedroom_lights_on

        self.bedroom_lights_off_button["text"] = "Bedroom OFF"
        self.bedroom_lights_off_button["command"] = self.bedroom_lights_off

        self.livingroom_lights_on_button["text"] = "Living room ON"
        self.livingroom_lights_on_button["command"] = self.livingroom_lights_on

        self.livingroom_lights_off_button["command"] = self.livingroom_lights_off
        self.livingroom_lights_off_button["text"] = "Living room OFF"


    # self.motion_on_button["text"] = "Motion On"
    # self.motion_on_button["command"] = self.start_motion


    # self.motion_off_button["text"] = "Motion Off"
    # self.motion_off_button["command"] = self.stop_motion


        self.livingroom_lights_off_button.pack(side="top")
        self.livingroom_lights_on_button.pack(side="top")
        self.bedroom_lights_off_button.pack(side="top")
        self.bedroom_lights_on_button.pack(side="top")
        # self.motion_off_button.pack(side="top")
        # self.motion_on_button.pack(side="top")

        self.quit = tk.Button(self, text="QUIT", fg="red", command=self.master.destroy, padx='50', pady='50')
        
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

