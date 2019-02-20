"""
  Capstone Project.  Code to run on the EV3 robot (NOT on a laptop).
  Author:  Your professors (for the framework)
    and Shengjun Guan.
  Winter term, 2018-2019.
"""

import rosebot
import mqtt_remote_method_calls as com
import time
import shared_gui_delegate_on_robot
import math


def main():
    """
    This code, which must run on the EV3 ROBOT:
      1. Makes the EV3 robot to various things.
      2. Communicates via MQTT with the GUI code that runs on the LAPTOP.
    """
    # spin()
    # run_test_arm()
    real_thing()
    # ir_test()
    # go()
    # color_rec()
    # color()


def color():
    robot = rosebot.RoseBot()
    while True:
        print(robot.sensor_system.color_sensor.get_color())
        if robot.sensor_system.color_sensor.get_color() == 4:
            break

    # get_color(self):
    # """
    # Returns the color detected by the sensor, as best the sensor can judge
    # from shining red, then green, then blue light and measuring the
    # intensities returned.  The returned value is an integer between
    # 0 and 7, where the meanings of the integers are:
    #   - 0: No color
    #           (that is, cannot classify the color as one of the following)
    #   - 1: Black
    #   - 2: Blue
    #   - 3: Green
    #   - 4: Yellow
    #   - 5: Red
    #   - 6: White
    #   - 7: Brown


#
# def run_test_arm():
#     robot = rosebot.RoseBot()
#     robot.arm_and_claw.calibrate_arm()
#     robot.arm_and_claw.raise_arm()
#     robot.arm_and_claw.lower_arm()
#     robot.arm_and_claw.raise_arm()
#     robot.arm_and_claw.move_arm_to_position(0)

# def color_rec():
#     robot = rosebot.RoseBot()
#
#     while True:
#         if robot.sensor_system.camera.low_level_camera.mode.title() != 'Sig1' :
#             print(' yes')
#         else:
#             print('Nope')
#             print(robot.sensor_system.camera.low_level_camera.mode.)
#         time.sleep(0.5)

def go():
    robot = rosebot.RoseBot()
    robot.drive_system.go_straight_for_seconds(3.4, 50)


def spin():
    robot = rosebot.RoseBot()
    robot.drive_system.spin_an_angle(math.pi / 2, 1, 2 * math.pi * 20 / 110)
    robot.drive_system.go_straight_for_seconds(12,50)
    time.sleep(0.5)
    robot.drive_system.go_straight_for_seconds(12,-50)



def real_thing():
    robot = rosebot.RoseBot()
    delegate = shared_gui_delegate_on_robot.ResponderToGUIMessages(robot)
    mqtt_reveiver = com.MqttClient(delegate)
    mqtt_reveiver.connect_to_pc()
    while True:
        if delegate.stop_program:
            break
        time.sleep(0.01)


def ir_test():
    robot = rosebot.RoseBot()
    while True:
        d = robot.sensor_system.ir_proximity_sensor.get_distance_in_inches()
        print(d, type(d))
        time.sleep(0.5)


# -----------------------------------------------------------------------------
# Calls  main  to start the ball rolling.
# -----------------------------------------------------------------------------
main()
