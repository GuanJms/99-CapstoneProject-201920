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
import shared_gui_delegate_on_robot
import rosebot


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

    fre_pics = {
        "E3": 164.81,
        "F3": 174.61,
        "G3": 196.00,
        "A3": 220.00,
        "B3": 246.94,
        "C4": 261.63,
        "D4": 293.66,
        "E4": 329.63,
        "F4": 349.23,
        "G4": 392.00,
        "A4": 440.00,
        "B4": 493.88,
        "C5": 523.25,
        "D5": 587.33,
        "E5": 659.23,
        "F5": 698.46,
        "G5": 783.99
    }

    mqtt_sender = com.MqttClient()
    mqtt_sender.connect_to_ev3()
    frobot = shared_gui_delegate_on_robot.frobot()
    t = shared_gui_delegate_on_robot.ResponderToGUIMessages(rosebot)
    root = tkinter.Tk()
    root.title("Shengjun's CSSE 120 Final Project")
    main_frame = ttk.Frame(root, padding=10, borderwidth=5, relief="groove")
    main_frame.grid()
    canvas = tkinter.Canvas(main_frame, width=480, height=520, bg='white')
    main_label = ttk.Label(main_frame, text='Robot Running on Guitar Platform')
    guitar_width_input_frame = guitar_width(main_frame, mqtt_sender,frobot)
    last_button = None
    note_frame = music_buttons(canvas,main_frame, mqtt_sender,frobot,note_pics,fre_pics,t)

    # canvas part
    guitar_canvas(canvas)
    # grid part
    main_label.grid(row=0, column=0)
    guitar_width_input_frame.grid(row=1, column=0)
    canvas.grid(row=2, column=1)
    note_frame.grid(row=2, column=0)
    root.mainloop()


def guitar_width(main_frame, mqtt_sender,frobot):
    guitar_width_input_frame = ttk.Frame(main_frame, padding=10, borderwidth=5, relief="groove")
    gitar_label = ttk.Label(guitar_width_input_frame, text="Guitar width(inches):")
    gitar_entry = ttk.Entry(guitar_width_input_frame, width=8)
    start_generate = ttk.Button(guitar_width_input_frame, text='Generate')
    # grid
    gitar_label.grid(row=0, column=0)
    gitar_entry.grid(row=0, column=1)
    start_generate.grid(row=0, column=2)
    # todo: Generate botton method
    start_generate["command"] = lambda: handle_start_generate(float(gitar_entry.get()) / 480, float(gitar_entry.get()),
                                                              mqtt_sender,frobot)
    return guitar_width_input_frame


def guitar_canvas(canvas):
    # Drawing guitar lines
    y = 110
    print(y)
    for i in range(5):
        canvas.create_line(0, i * y + 40, 520, i * y + 40)
    x = 80
    for i in range(1, 6):
        canvas.create_line(i * x, 40, i * x, 480)

    # crossing the first fret
    canvas.create_line(0, 40, 480, 150)
    canvas.create_line(0, 150, 480, 40)


def music_buttons(canvas, main_frame, mqtt_sender,frobot,note_pics,fre_pics,t):
    music_button_frame = ttk.Frame(main_frame, padding=10, borderwidth=5, relief="groove")
    lista = ['C', 'D', 'E', 'F', 'G', 'A', 'B']
    for i in range(3, 6, 1):
        for j in range(len(lista)):
            button_name = lista[j] + str(i)
            if button_name != 'C3' and button_name != 'D3' and button_name != 'A5' and button_name != 'B5':
                position_x = i - 3
                position_y = j
                button_construct(canvas,position_x, position_y, music_button_frame, mqtt_sender, button_name,frobot,note_pics,fre_pics,t)
    return music_button_frame


def button_construct(canvas,position_x, position_y, music_button_frame, mqtt_sender, button_name, frobot,note_pics,fre_pics,t):
    button = ttk.Button(music_button_frame, text=button_name)
    button.grid(row=position_y, column=position_x)
    button["command"] = lambda: handle_note(canvas,button_name, mqtt_sender, frobot,note_pics,fre_pics,t)
    button.grid(row=position_y, column=position_x)


def handle_note(canvas, button_name, mqtt_sender, frobot, note_pics,fre_pics, t):
    last_button = frobot.last_button
    frobot.button_name = button_name
    frobot.frequency = fre_pics[button_name]
    try:
        clockwise, degree, distance = move(frobot.last_button,frobot.button_name,note_pics, frobot.k,frobot)
    except:
        clockwise, degree, distance = None, None, None
    print(frobot.frequency, frobot.last_button)
    mqtt_sender.send_message("note", [clockwise, degree, distance, frobot.frequency])

    rotate_t0 =  degree / t.k_for_degrees
    distance_t = distance / t.t_for_inches
    changing_canvas(canvas, last_button, button_name, rotate_t0, distance_t,note_pics)

def changing_canvas(canvas, last_button, button_name, rotate_t0, distance_t,note_pics):
    import time
    time.sleep(rotate_t0)
    try:
        canvas.delete('bluecar')
    except:
        pass
    updates_times = distance_t * 50
    numebers = 0
    while True:
        numebers = numebers + 1
        if numebers >= updates_times:
            break
    #DONE """Make the last_button and button_name linked to the x0, calculate
    #         each update the x using the angle. Then extend one point into four points and
    #         make the area as a car"""
    #DONE """Make the animation last for a while rather than delet need testing"""
    x0, y0 = note_pics[last_button]
    xf, yf = note_pics[button_name]
    x = [x0]
    y = [y0]
    z0 = x0 + 80
    w0 = y0 + 110
    z = [z0]
    w = [w0]

    vx = (xf - x0) / numebers  # x velocity
    vy = (yf - y0) / numebers  # y velocity
    # ^ ^ ^ something
    # with angle and time for 0.05

    for t in range(1, numebers):

        new_x = x[t-1] + vx
        new_y = y[t-1] + vy
        new_z = z[t-1] + vx
        new_w = w[t-1] + vy

        x.append(new_x)
        y.append(new_y)
        z.append(new_z)
        w.append(new_w)

    for i in range(1, numebers):
        # canvas.create_oval(x[i], fill="", tag='blueball')
        canvas.create_rectangle(x[i],y[i],z[i],w[i], fill="black", tag='bluecar')
        canvas.update()

        # Pause for 0.05 seconds, then delete the image
        time.sleep(0.015)
        canvas.delete('bluecar')
    time.sleep(rotate_t0)
    canvas.create_rectangle(x[numebers-1],y[numebers-1],z[numebers-1],w[numebers-1], fill="blue", tag='bluecar')



def handle_start_generate(k, inches, mqtt_sender, frobot): # here make k into the calss
    print('Start generate guitar')
    print('Send rate to robot')
    frobot.k = k
    frobot.last_button = "E3"
    frobot.inches = inches
    mqtt_sender.send_message("generate", [inches])

def move(last_button, button_name, note_pics, k,frobot):
    clockwise = None
    degree = None
    distance = None
    if last_button != button_name:
        (x1, y1) = note_pics[last_button]
        (x2, y2) = note_pics[button_name]
        if x2 - x1 > 0:
            clockwise = 1
            if y2 - y1 > 0:
                degree = ma.pi - abs(ma.atan((x2 - x1) / (y2 - y1)))
                distance = k * ma.sqrt((y2 - y1) * (y2 - y1) + (x2 - x1) * (x2 - x1))
            if y2 - y1< 0:
                degree = abs(ma.atan((x2 - x1) / (y2 - y1)))
                distance = k * ma.sqrt((y2 - y1) * (y2 - y1) + (x2 - x1) * (x2 - x1))

            if y2 - y1 == 0:
                degree = ma.pi/2
                distance = k * abs(x2 - x1)

        if x2 - x1 < 0:
            clockwise = -1
            if y2 - y1 > 0:
                degree = ma.pi - abs(ma.atan((x2 - x1) / (y2 - y1)))
                distance = k * ma.sqrt((y2 - y1) * (y2 - y1) + (x2 - x1) * (x2 - x1))
            if y2 - y1 < 0:
                degree = abs(ma.atan((x2 - x1) / (y2 - y1)))
                distance = k * ma.sqrt((y2 - y1) * (y2 - y1) + (x2 - x1) * (x2 - x1))

            if y2 - y1 == 0:
                degree = ma.pi/2
                distance = k * abs(x2 - x1)
        if x2 - x1 == 0:
            clockwise = 0
            if y2 - y1 > 0:
                degree = ma.pi
            if y2 - y1 < 0:
                degree = 0
            distance = k * abs(y2 - y1)
        frobot.last_button = button_name

    return clockwise, degree, distance

    # after this method, its gonna give clockwise and counter-clockwise, degree, inches
    # clockwise 1 = clockwise yes
    # 0 = couter-clockwise
    # 3 = 180 degree to the opposite direction
main()

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

