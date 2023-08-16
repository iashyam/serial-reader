from tkinter import *
from tkinter.filedialog import asksaveasfile
import serial.tools.list_ports
from tkinter import messagebox
import serial
port_list = serial.tools.list_ports.comports()
import time
from xlwt import Workbook
import pandas as pd
import matplotlib.pyplot as plt


class window:
    def __init__(self):

        self.count = 1

        #making a window
        self.window = Tk()
        self.window.title("Serial Port Data Collector")
        self.window.geometry("450x400")
        self.window.resizable(False, False)
        #creating a workbook
        self.wb = Workbook()
        #addng a sheet
        self.sheet = self.wb.add_sheet('sheet1')

        #putting the headers to collect the data 
        self.sheet.write(0,0,"time")
        self.sheet.write(0, 1, "mass(g)")
        
        self.t0= time.time()

        #A check if start button is pressed
        self.isStarted = False

        # <-- creating a dropdown menu to select port from --> 

        #getting all the ports
        all_ports = []
        for port in port_list:
            all_ports.append(str(port))

        #creating a menu
        self.menu = StringVar()
        self.menu.set("Select the port")

        #creating a dropdown option
        drop = OptionMenu(self.window, self.menu, *all_ports)
        drop.grid(row=0, column=1)

        #<--- creating an input to ask for bod rate --->
        label = Label(self.window, text = "Enter the bod rate: ")
        label.grid(row=2, column=1)
        self.bod_entry = Entry(self.window, width=40)
        self.bod_entry.grid(row=3, column=1, padx=20)
        self.set_button = Button(self.window, text="set", command=self.set)
        self.set_button.grid(row=3, column=2)

        # #<--- to create a file to store data --->
        # label = Label(self.window, text="Select the file to save data")
        # label.grid(row=4, column=1)
        # button = Button(self.window, text="Select", command=self.save_file)
        # button.grid(row=4, column=2)

        #<--- A label to display whcih port is selected --->
        label = Label(self.window, text="Current Port: ")
        label.grid(row=6, column=0)
        self.port_label = Label(self.window, text="text will appear here")
        self.port_label.grid(row=6, column=1)

        #<--- A label to display the current value of mass --->
        label = Label(self.window, text='Current Mass: ')
        label.grid(row=7, column=0)
        self.mass_label = Label(self.window, text=str("Text will appear here"))
        self.mass_label.grid(row=7, column=1)

        #<--- A label to display the current time --->
        label = Label(self.window, text="Current Time: ")
        label.grid(row=8, column=0)
        self.time_label = Label(self.window, text="Text will appear here")
        self.time_label.grid(row=8, column=1)
    
        #<--- A start Button --->
        self.start_button = Button(self.window, text="Record Data",state='disabled', command=self.get_data)
        self.start_button.grid(row=5, column=1, pady=10)

        #<--- A button to end the process and save the data  --->
        self.end_button = Button(self.window, text="End", state="disabled", command=self.end)
        self.end_button.grid(row=9, column=1, pady=10)

        #<--- A button to plot the results --->
        self.plot_button = Button(self.window, text="Plot", state='disabled', command=self.plot)
        self.plot_button.grid(row=10, column=1, pady=10)

        self.name_label = Label(self.window, text="Software by Shyam Sunder, PH22C047")
        self.name_label.grid(row=11, column=1, pady=30)

        self.window.mainloop()


    def get_data(self):
        
        #main task collecting the data
        data = ""
        for _ in range(14):
            if self.obj.in_waiting:
                thing = self.obj.read()
                thing = str(thing.decode('utf'))
                data += thing

        #extracting the actual mass from the strange string this sends
        mass = data[5:11]

        #time since they are started
        t = round(time.time() - self.t0, 4)

        #show the latest data on the gui
        self.mass_label.config(text=str(mass))
        self.time_label.config(text=str(t))
        self.port_label.config(text=str(self.port))

        #write the data in excel sheet 
        self.sheet.write(self.count, 0, t)
        self.sheet.write(self.count, 1, mass)
        self.count += 1
    
    
    def end(self):
        self.isStarted = False 
        try:
            self.file_name = self.save_file()
            self.wb.save(self.file_name) 
            self.plot_button.config(state='active')
        except AttributeError:
            messagebox.showerror("Error", "Please select valid file name!")
            


    def plot(self):
        data = pd.read_excel(self.file_name)

        times = data['time']
        masses = data['mass(g)']

        plt.style.use('seaborn-v0_8-whitegrid')
        plt.plot(times, masses)
        plt.title("Time vs Mass")
        plt.xlabel('Time')
        plt.ylabel("Mass")
        plt.show()

    def save_file(self):
        f = asksaveasfile("w", initialfile = 'Untitled.xls',defaultextension=".xls")
        return f.name

    def set(self):

        ### BODE RATE AND PORT ARE TO BE SELECTED BY THE USER
        self.port = str(self.menu.get())
        self.port_address = self.port.split('-')[0].strip()
        self.bod_rate = str(self.bod_entry.get())

        #connecting with the serial port to communicate
        self.obj = serial.Serial(self.port_address, self.bod_rate, xonxoff=True)

        #sending the command to activate continous sending of the data
        #the command is D03
        self.obj.write(b'D03\r\n')

        self.set_button.config(state='disabled')
        self.start_button.config(state='active')
        self.end_button.config(state='active')
        self.bod_entry.config(state='disabled')
        
    def start(self):
        self.isStarted = True
        print("Mera naam mery hai")
        
if __name__ == "__main__":
    window()