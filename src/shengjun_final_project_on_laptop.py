"""
1. generate a guitar platform
2. construct a tone data base
3. interactive GUI
4. Tab playing
    a. pattern
"""
import mqtt_remote_method_calls as com
import tkinter
from tkinter import ttk
import shared_gui

def main():
    mqtt_sender = com.MqttClient()
    mqtt_sender.connect_to_ev3()

    root = tkinter.Tk()
    root.title("Evil3")