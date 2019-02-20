"""
  Capstone Project.  Code to run on a LAPTOP (NOT the robot).
  Displays the Graphical User Interface (GUI) and communicates with the robot.

  Authors:  Your professors (for the framework)
    and Rishav Khosla.
  Winter term, 2018-2019.
"""

import mqtt_remote_method_calls as com
import tkinter
from tkinter import ttk
import shared_gui
import time
import rosebot


def main():
    mqtt_sender = com.MqttClient()
    mqtt_sender.connect_to_ev3()

    root = tkinter.Tk()
    root.title('Rishav Khosla Final Project')

    main_frame = ttk.Frame(root, padding=10, borderwidth=5, relief='groove')
    main_frame.grid()

    agv_label = ttk.Label(main_frame, text=' Prototype AGV Beta Testing')
    empty_label = ttk.Label(main_frame)
    empty_label_2 = ttk.Label(main_frame)
    start_button = ttk.Button(main_frame, text='Start Moving Boxes')
    quit_button = ttk.Button(main_frame, text='Exit Program')
    calibrate_button = ttk.Button(main_frame, text='Calibrate Arm')

    agv_label.grid(row=0, column=1)
    empty_label.grid(row=1, column=1)
    empty_label_2.grid(row=3, column=1)
    start_button.grid(row=2, column=1)
    quit_button.grid(row=4, column=2)
    calibrate_button.grid(row=4, column=0)

    start_button['command'] = lambda: handle_agv(mqtt_sender)
    quit_button['command'] = lambda: handle_quit(mqtt_sender)
    calibrate_button['command'] = lambda: handle_calibrate(mqtt_sender)

    root.mainloop()


def handle_agv(mqtt_sender):
    mqtt_sender.send_message("agv")


def handle_quit(mqtt_sender):
    mqtt_sender.send_message('quit')


def handle_calibrate(mqtt_sender):
    mqtt_sender.send_message('calibrate_arm')


main()

