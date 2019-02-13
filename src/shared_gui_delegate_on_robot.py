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
        self.stop_program= False

    def go(self, left_wheel_speed, right_wheel_speed):
        left = int(left_wheel_speed)
        right = int(right_wheel_speed)
        self.robot.drive_system.go(left, right)

    def stop(self):
        self.robot.drive_system.stop()

    def raise_arm(self):
        self.robot.arm_and_claw.raise_arm()

    def calibrate_arm(self):
        self.robot.arm_and_claw.calibrate_arm()

    def lower_arm(self):
        self.robot.arm_and_claw.lower_arm()

    def move_arm_to_position(self, arm_position_entry):
        self.robot.arm_and_claw.move_arm_to_position(arm_position_entry)

    def quit(self):
        self.stop_program = True
        # self.stop()
        # self.robot.arm_and_claw.motor.turn_off()


    def exit(self):
        self.quit()
        self.robot.exit()

    def straight_for_seconds(self, time_entry, speed_entry):
        self.robot.drive_system.go_straight_for_seconds(time_entry, speed_entry)

    def straight_for_inches_using_time(self, distance_entry, speed_entry):
        self.robot.drive_system.go_straight_for_inches_using_time(distance_entry, speed_entry)

    def straight_for_inches_using_encoder(self, distance_entry, speed_entry):
        self.robot.drive_system.go_straight_for_inches_using_encoder(distance_entry, speed_entry)

    def beep_for_a_given_of_times(self,given_times):
        for k in range(int(given_times)):
            self.robot.sound_system.beeper.beep().wait()

    def play_a_tone_at_a_given_of_times(self,frequency, duration, given_times):
        for i in range(given_times):
            self.robot.sound_system.tone_maker.play_tone(frequency,duration)

    def speak_a_given_phrase(self,phrase):
        self.robot.sound_system.speech_maker.speak(phrase)

    def tone_up_with_inches(self,frequency_entry,safe_inches_entry,speed_entry,k_entry):
        seconds_per_inch_at_100 = 10.0  # 1 sec = 10 inches at 100 speed
        import time
        duration = 200
        distance_per_sec = (speed_entry/100)*10
        duration_distance = duration *  distance_per_sec # duration 0.2s * f/x *x/s
        self.robot.drive_system.left_motor.turn_on(speed_entry)
        self.robot.drive_system.right_motor.turn_on(speed_entry)
        while True:
            self.robot.sound_system.tone_maker.play_tone(frequency_entry,duration)
            frequency_entry = frequency_entry + k_entry *duration_distance/1000
            time.sleep(duration)
            print(frequency_entry,duration,self.robot.sensor_system.ir_proximity_sensor.get_distance_in_inches()-safe_inches_entry
            if self.robot.sensor_system.ir_proximity_sensor.get_distance_in_inches() <= safe_inches_entry:
                self.stop()
                break

