import Tkinter as tk
from Tkinter import Label, Frame
import datetime
import requests
import time
import sys
from decouple import config
from PIL import ImageTk, Image

COMMANDS = {}
COMMANDS['OFF'] = 'off'
COMMANDS['ON'] = 'on'
bedroom_ip = str(config('BEDROOMIP'))
livingroom_ip = str(config('LIVINGROOMIP'))
on_img_path = str(config('ONIMGPATH'))
off_img_path = str(config('OFFIMGPATH'))
port = str(config('PORT'))
REFRESH_DELAY=1500
room_state = 'on'
imgs = [None, None]

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
            print('Trying')
            requests.get('http://{}:{}/lights-{}'.format(ip, port, command))
        except Exception as e:
            self.handle_errors(e)

    def bedroom_lights_on(self):
        self.light_handler(bedroom_ip, COMMANDS['ON'])
        self.get_refreshed_image('on', 'bed')

    def bedroom_lights_off(self):
        self.light_handler(bedroom_ip, COMMANDS['OFF'])
        self.get_refreshed_image('off', 'bed')

    def livingroom_lights_on(self):    
        self.light_handler(livingroom_ip, COMMANDS['ON'])
        self.get_refreshed_image('on', 'living')

    def livingroom_lights_off(self):
        self.light_handler(livingroom_ip, COMMANDS['OFF'])
        self.get_refreshed_image('off', 'living')
 
    def load_on_indicator(self):
        self.bedroom_on_img = ImageTk.PhotoImage(Image.open(on_img_path))
        panel = tk.Label(root, image=self.bedroom_on_img)
        panel.pack(side='bottom', fill='both', expand='yes')
        imgs[1] = panel

    def load_off_indicator(self):
        self.bedroom_off_img = ImageTk.PhotoImage(Image.open(off_img_path))
        panel = tk.Label(root, image=self.bedroom_off_img)
        panel.pack(side='bottom', fill='both', expand='yes')
        imgs[0] = panel

    def get_refreshed_image(self, state, room):
        ROOMS = {'living': 0, 'bed': 1}
        r = ROOMS[room]
        if state is 'on':
            imgs[r].config(image=self.bedroom_on_img)
        else:
            imgs[r].config(image=self.bedroom_off_img)

    # TODO: refactor this to be a handler for both rooms, call functions above to load depending on room state
    def load_light_indicators(self):
        if room_state is 'on':
            self.load_on_indicator()
        else:
            self.load_off_indicator()



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

        # TODO: cut this image in half, create logic to store state of each light and render appropriate (on or off) image. Will likely need to move buttons to facilitate this visually. 

        self.bedroom_lights_on_button["text"] = "Bedroom ON"
        self.bedroom_lights_on_button["command"] = self.bedroom_lights_on

        self.bedroom_lights_off_button["text"] = "Bedroom OFF"
        self.bedroom_lights_off_button["command"] = self.bedroom_lights_off

        self.livingroom_lights_on_button["text"] = "Living room ON"
        self.livingroom_lights_on_button["command"] = self.livingroom_lights_on

        self.livingroom_lights_off_button["command"] = self.livingroom_lights_off
        self.livingroom_lights_off_button["text"] = "Living room OFF"
        self.load_on_indicator()
        self.load_off_indicator()


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
# app.loop_refresh()
app.mainloop()

