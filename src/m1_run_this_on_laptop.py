"""
  Capstone Project.  Code to run on a LAPTOP (NOT the robot).
  Displays the Graphical User Interface (GUI) and communicates with the robot.

  Authors:  Your professors (for the framework)
    and Shengjun Guan.
  Winter term, 2018-2019.
"""

import mqtt_remote_method_calls as com
import tkinter
from tkinter import ttk
import shared_gui


def main():
    """
    This code, which must run on a LAPTOP:
      1. Constructs a GUI for my part of the Capstone Project.
      2. Communicates via MQTT with the code that runs on the EV3 robot.
    """
    # -------------------------------------------------------------------------
    # Construct and connect the MQTT Client:
    # -------------------------------------------------------------------------
    mqtt_sender = com.MqttClient()
    mqtt_sender.connect_to_ev3()

    # -------------------------------------------------------------------------
    # The root TK object for the GUI:
    # -------------------------------------------------------------------------
    root = tkinter.Tk()
    root.title("Evil3")


    # -------------------------------------------------------------------------
    # The main frame, upon which the other frames are placed.
    # -------------------------------------------------------------------------

    main_frame = ttk.Frame(root, padding = 10, borderwidth = 5, relief = "groove")
    main_frame.grid()

    # -------------------------------------------------------------------------
    # Sub-frames for the shared GUI that the team developed:
    # -------------------------------------------------------------------------
    teleop_frame, arm_frame, control_frame, get_drive_systems_frame, get_sound_system_frame= get_shared_frames(main_frame, mqtt_sender)


    # -------------------------------------------------------------------------
    # Frames that are particular to my individual contributions to the project.
    # -------------------------------------------------------------------------
    # TODO: Implement and call get_my_frames(...)
    #individual frame code
    individual_frame_1_go_straight_with_time = ttk.Frame(main_frame, padding=10, borderwidth=5, relief="ridge")
    individual_frame_1_go_straight_with_time.grid()

    # Construct the widgets on the frame:
    frame_label = ttk.Label(individual_frame_1_go_straight_with_time, text="Go Straight with time")
    time_entry = ttk.Entry(individual_frame_1_go_straight_with_time, width=8)
    go = ttk.Button(individual_frame_1_go_straight_with_time, text="go with time")
    speed_entry = ttk.Entry(individual_frame_1_go_straight_with_time, width=8)
    speed_entry.insert(0, "100")

    # Grid the widgets:
    frame_label.grid(row=0, column=1)
    time_entry.grid(row=1, column=0)
    speed_entry.grid(row=1, column=1)
    go.grid(row=1, column=2)

    # Set the Button callbacks:
    go["command"] = lambda: handle_go_with_times(time_entry.get(), speed_entry.get(), mqtt_sender )



    # -------------------------------------------------------------------------
    # Grid the frames.
    # -------------------------------------------------------------------------
    grid_frames(teleop_frame,arm_frame,control_frame,individual_frame_1_go_straight_with_time, get_drive_systems_frame, get_sound_system_frame)

    # -------------------------------------------------------------------------
    # The event loop:
    # -------------------------------------------------------------------------
    root.mainloop()



def get_shared_frames(main_frame, mqtt_sender):
    teleop_frame = shared_gui.get_teleoperation_frame(main_frame,mqtt_sender)
    arm_frame = shared_gui.get_arm_frame(main_frame,mqtt_sender)
    control_frame = shared_gui.get_control_frame(main_frame,mqtt_sender)
    get_drive_systems_frame = shared_gui.get_drive_systems_frame(main_frame,mqtt_sender)
    get_sound_system_frame = shared_gui.get_sound_system_frame(main_frame,mqtt_sender)

    return teleop_frame, arm_frame, control_frame, get_drive_systems_frame, get_sound_system_frame


def grid_frames(teleop_frame, arm_frame, control_frame,individual_frame_1_go_straight_with_time,get_drive_systems_frame, get_sound_system_frame):
    teleop_frame.grid(row=0, column = 0)
    arm_frame.grid(row=1,column = 0)
    control_frame.grid(row=2,column = 0)
    individual_frame_1_go_straight_with_time.grid(row=3,column = 0)
    get_drive_systems_frame.grid(row=4, column =0)
    get_sound_system_frame.grid(row=5, column =0)


def handle_go_with_times(time_entry, speed_entry, mqtt_sender):
    print("go_straight_for_seconds", time_entry, speed_entry)
    mqtt_sender.send_message("run_with_time", [time_entry, speed_entry])

# -----------------------------------------------------------------------------
# Calls  main  to start the ball rolling.
# -----------------------------------------------------------------------------
main()