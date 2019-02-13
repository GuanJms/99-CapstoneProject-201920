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


def main():
    """
    This code, which must run on the EV3 ROBOT:
      1. Makes the EV3 robot to various things.
      2. Communicates via MQTT with the GUI code that runs on the LAPTOP.
    """
    # run_test_arm()
    real_thing()
    # ir_test()

#
# def run_test_arm():
#     robot = rosebot.RoseBot()
#     robot.arm_and_claw.calibrate_arm()
#     robot.arm_and_claw.raise_arm()
#     robot.arm_and_claw.lower_arm()
#     robot.arm_and_claw.raise_arm()
#     robot.arm_and_claw.move_arm_to_position(0)


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
        print(d,type(d))
        time.sleep(0.5)


# -----------------------------------------------------------------------------
# Calls  main  to start the ball rolling.
# -----------------------------------------------------------------------------
main()