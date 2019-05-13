import Tkinter as tk
from Tkinter import Label, Frame
import datetime
import requests

class Application(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.master = master
        self.pack()
        self.create_widgets()

    def write_to_log(self, data):
        with open('/home/pi/sandbox/log.txt', 'a') as file:
            file.write('written {}\n{}\n'.format(datetime.datetime.now(), data))

    def handle_errors(self, e):
        print('Exception: {}'.format(e))
        self.write_to_log(e)

    def lights_off(self):
        try:
            requests.get('http://10.0.0.237:4321/lights-off')
        except Exception as e:
            self.handle_errors(e)

    def lights_on(self):
        try:
            requests.get('http://10.0.0.237:4321/lights-on')
        except Exception as e:
            self.handle_errors(e)

    def create_widgets(self):
        self.lights_off_button = tk.Button(self, relief='raised')
        self.lights_on_button = tk.Button(self)
        self.lights_off_button["text"] = "Lights Off"
        self.lights_off_button["command"] = self.lights_off
        self.lights_on_button["text"] = "Lights On"
        self.lights_on_button["command"] = self.lights_on
        self.lights_on_button.pack(side="top")
        self.lights_off_button.pack(side="top")
        self.quit = tk.Button(self, text="QUIT", fg="red",
                                  command=self.master.destroy,
                                  padx='13')
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

