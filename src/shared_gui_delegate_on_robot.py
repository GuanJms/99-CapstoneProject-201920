"""
  Capstone Project.  Code to run on the EV3 robot (NOT on a laptop).
  This code is the delegate for handling messages from the shared GUI.

  Author:  Your professors (for the framework)
    and Rishav Khosla and Shengjun Guan.
  Winter term, 2018-2019.
"""
import rosebot

class ResponderToGUIMessages(object):
    def __init__(self, robot):
        """
            :type robot: rosebot.RoseBot
        """
        self.robot = robot

    def go(self, left_wheel_speed, right_wheel_speed):
        left = int(left_wheel_speed)
        right = int(right_wheel_speed)
        self.robot.drive_system.go(left, right)
