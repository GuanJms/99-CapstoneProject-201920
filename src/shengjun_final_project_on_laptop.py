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
import math as ma

import shared_gui

def main():
    note_pics = {
        "E3": (0, 40),
        "F3": (0, 150),
        "G3": (0, 370),
        "A3": (80, 40),
        "B3": (80, 260),
        "C4": (80, 370),
        "D4": (160, 40),
        "E4": (160, 260),
        "F4": (160, 370),
        "G4": (240, 40),
        "A4": (240, 260),
        "B4": (320, 40),
        "C5": (320, 150),
        "D5": (320, 370),
        "E5": (400, 40),
        "F5": (400, 150),
        "G5": (400, 370)
    }
    mqtt_sender = com.MqttClient()
    mqtt_sender.connect_to_ev3()

    root = tkinter.Tk()
    root.title("Shengjun's CSSE 120 Final Project")

    main_frame = ttk.Frame(root, padding=10, borderwidth=5, relief="groove")
    main_frame.grid()
    main_label = ttk.Label(main_frame, text='Robot Running on Guitar Platform')

    guitar_width_input_frame, actual_width = guitar_width(main_frame,mqtt_sender)
    k = actual_width/480 #pic in data calculated for inches in actual
    last_button = None
    note_frame = music_buttons(main_frame,mqtt_sender)

# canvas part
    canvas = tkinter.Canvas(main_frame, width=480, height=520, bg='white')
    guitar_canvas(canvas)
# grid part
    main_label.grid(row=0,column= 0)
    guitar_width_input_frame.grid(row=1,column=0)
    canvas.grid(row=2, column=1)
    note_frame.grid(row=2,column=0)
    root.mainloop()


def guitar_width(main_frame,mqtt_sender):
    guitar_width_input_frame = ttk.Frame(main_frame, padding=10, borderwidth=5, relief="groove")
    gitar_label = ttk.Label(guitar_width_input_frame,text="Guitar width(inches):")
    gitar_entry = ttk.Entry(guitar_width_input_frame,width=8)
    start_generate = ttk.Button(guitar_width_input_frame, text='Generate')
    # grid
    gitar_label.grid(row=0,column=0)
    gitar_entry.grid(row=0,column=1)
    start_generate.grid(row=0,column=2)
    # todo: Generate botton method


    return guitar_width_input_frame, gitar_entry.get()

def guitar_canvas(canvas):
    # Drawing guitar lines
    y = 110
    print(y)
    for i in range(5):
        canvas.create_line(0, i * y + 40, 520, i * y + 40)
    x = 80
    for i in range(1, 6):
        canvas.create_line(i * x, 40, i * x, 480)

    #crossing the first fret
    canvas.create_line(0, 40, 480,150)
    canvas.create_line(0,150, 480 , 40)

def music_buttons(main_frame, mqtt_sender):
    music_button_frame =  ttk.Frame(main_frame, padding=10, borderwidth=5, relief="groove")
    lista = ['C','D','E','F','G','A','B']
    for i in range(3,6,1):
        for j in  range(len(lista)):
            button_name = lista[j] + str(i)
            if button_name != 'C3' and button_name != 'D3' and button_name != 'A5' and button_name != 'B5':
                position_x = i - 3
                position_y = j
                button_construct(position_x,position_y,music_button_frame, mqtt_sender,button_name)
    return music_button_frame

def button_construct(position_x,position_y,music_button_frame, mqtt_sender,button_name):
    button = ttk.Button(music_button_frame,text=button_name)
    button.grid(row=position_y, column = position_x)
    button["command"] = lambda: handle_note(button_name, mqtt_sender)
    button.grid(row=position_y, column =position_x)


def handle_note(button_name, mqtt_sender):
    print(button_name)
    mqtt_sender.send_message("note",[button_name])

def move(last_button, button_name, note_pics):
    if last_button == None:
        last_button = 'E3'
    if button_name != button_name:
        (x1, y1) = note_pics[last_button]
        (x2, y2) = note_pics[button_name]
        if x2-x1 > 0:
            clockwise = 1
            if y2-y1 != 0:
                degree  = abs(ma.atan((x2 - x1) / (y2 - y1)))
            if y2-y1 == 0:
                degree = ma.pi/2
        if x2-x1 < 0:
            clockwise = 0
            if y2 - y1 != 0:
                degree = ma.pi - abs(ma.atan((x2 - x1) / (y2 - y1)))
            if y2 - y1 == 0:
                degree = ma.pi/2
        if x2-x1 == 0:
            clockwise = 3

    return clockwise, degree, distance

    # after this method, its gonna give clockwise and counter-clockwise, degree, inches
    # clockwise 1 = clockwise yes
    # 0 = couter-clockwise
    # 3 = 180 degree to the opposite direction





main()
