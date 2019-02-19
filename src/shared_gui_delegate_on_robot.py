"""
  Capstone Project.  Code to run on the EV3 robot (NOT on a laptop).
  This code is the delegate for handling messages from the shared GUI.

  Author:  Your professors (for the framework)
    and Rishav Khosla and Shengjun Guan.
  Winter term, 2018-2019.
"""
import rosebot
import math as ma


class ResponderToGUIMessages(object):
    def __init__(self, robot):
        """
            :type robot: rosebot.RoseBot
        """
        self.robot = robot
        self.stop_program = False
        self.t_for_inches = 12/3.35 # to get this value do experience: ()inches/()s
        self.k_for_degrees = 2*ma.pi*20 / 109# (rad)/s

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

    def beep_for_a_given_of_times(self, given_times):
        for k in range(int(given_times)):
            self.robot.sound_system.beeper.beep().wait()

    def play_a_tone_at_a_given_of_times(self, frequency, duration, given_times):
        for i in range(given_times):
            self.robot.sound_system.tone_maker.play_tone(frequency, duration)

    def speak_a_given_phrase(self, phrase):
        self.robot.sound_system.speech_maker.speak(phrase)

    def tone_up_with_inches(self, frequency_entry, safe_inches_entry, speed_entry, k_entry):
        seconds_per_inch_at_100 = 10.0  # 1 sec = 10 inches at 100 speed
        import time
        duration = 200
        distance_per_sec = (speed_entry / 100) * 10
        duration_distance = duration * distance_per_sec  # duration 0.2s * f/x *x/s
        self.robot.drive_system.left_motor.turn_on(speed_entry)
        self.robot.drive_system.right_motor.turn_on(speed_entry)
        while True:
            self.robot.sound_system.tone_maker.play_tone(frequency_entry, duration)
            frequency_entry = frequency_entry + k_entry * (duration_distance / 1000)
            print(frequency_entry, duration,
                  self.robot.sensor_system.ir_proximity_sensor.get_distance_in_inches() - safe_inches_entry)
            if self.robot.sensor_system.ir_proximity_sensor.get_distance_in_inches() <= safe_inches_entry:
                self.stop()
                break
            time.sleep(duration / 1000)

    def beep_faster(self, initial_duration_entry, safe_inches_entry, speed_entry, k_entry):
        import time
        self.robot.drive_system.left_motor.turn_on(speed_entry)
        self.robot.drive_system.right_motor.turn_on(speed_entry)
        duration = initial_duration_entry / 1000
        duratin_increasing_pace = -1 * k_entry / 1000
        while True:
            self.robot.sound_system.beeper.beep()
            if duration + duratin_increasing_pace * duration > 0:
                duration = duration + duratin_increasing_pace * duration
            print(self.robot.sensor_system.ir_proximity_sensor.get_distance_in_inches() - safe_inches_entry,
                  duration)
            if self.robot.sensor_system.ir_proximity_sensor.get_distance_in_inches() <= safe_inches_entry:
                self.stop()
                break
            time.sleep(duration)

    def led_faster(self, initial_duration_entry, safe_inches_entry, speed_entry, k_entry):
        import time
        duration = initial_duration_entry
        duration_dec = -1 * k_entry
        # self.robot.led_system.left_led = self.robot.led_system.LED("left")
        # self.robot.led_system.right_led = self.robot.led_system.LED("Right")
        self.robot.drive_system.left_motor.turn_on(speed_entry)
        self.robot.drive_system.right_motor.turn_on(speed_entry)
        while True:
            self.robot.led_system.left_led.set_color_by_name(self.robot.led_system.left_led.GREEN)
            time.sleep(duration)
            self.robot.led_system.left_led.set_color_by_name(self.robot.led_system.left_led.BLACK)
            time.sleep(duration)
            self.robot.led_system.right_led.set_color_by_name(self.robot.led_system.right_led.GREEN)
            time.sleep(duration)
            self.robot.led_system.right_led.set_color_by_name(self.robot.led_system.right_led.BLACK)
            time.sleep(duration)
            self.robot.led_system.left_led.set_color_by_name(self.robot.led_system.left_led.GREEN)
            self.robot.led_system.right_led.set_color_by_name(self.robot.led_system.right_led.GREEN)
            time.sleep(duration)
            self.robot.led_system.right_led.set_color_by_name(self.robot.led_system.right_led.BLACK)
            self.robot.led_system.left_led.set_color_by_name(self.robot.led_system.left_led.BLACK)
            time.sleep(duration)
            if duration + duration_dec * 6 * duration > 0:
                duration = duration + duration_dec * 6 * duration
            if self.robot.sensor_system.ir_proximity_sensor.get_distance_in_inches() <= safe_inches_entry:
                self.stop()
                break

    def turn_clockwise_until_sees_object(self, speed):
        self.robot.drive_system.spin_clockwise_until_sees_object(speed, 10000)
        self.robot.drive_system.display_camera_data()

    def turn_counterclockwise_until_sees_object(self, speed):
        self.robot.drive_system.spin_counterclockwise_until_sees_object(speed, 10000)

    def note(self,clockwise, degree, distance, frequency):
    # spin first
        self.robot.drive_system.spin_an_angle(degree,clockwise,self.k_for_degrees)
    # move_forward
        time = distance / self.t_for_inches # inches / (inches/s)
        self.robot.drive_system.go_straight_for_seconds(time, 50)
    # spin back
        try:
            self.robot.drive_system.spin_an_angle(degree,-1*clockwise,self.k_for_degrees)
        except:
            pass
    # play a phrase
    # #play a tone
        self.robot.sound_system.tone_maker.play_tone(frequency,1000)

    def generate(self,inches):
        z = self.t_for_inches
        self.first_box(inches,z)
        print("first box is ready")
        # self.second_box(inches,z)
        # print("second box is ready")


    def second_box(self, inches,z):
        #take the second box and then move and put down the box
        self.take_box()
        inches_height = (inches / 48) * 33
        duration_1 = inches_height/ z # time for taking box and move to the position
        self.robot.drive_system.spin_an_angle(ma.pi,1,self.k_for_degrees)
        self.robot.drive_system.go_straight_for_seconds(duration_1,50)
        self.drop_box()
        self.robot.drive_system.go_straight_for_seconds(1, -50)
        self.robot.drive_system.spin_an_angle(ma.pi, -1,self.k_for_degrees)
        self.robot.drive_system.go_straight_for_seconds(1, -50)
        self.robot.drive_system.go_straight_for_seconds(duration_1,50)



    def take_box(self):
        import time
        self.robot.sound_system.beeper.beep()
        while True:
            time.sleep(0.5)
            if self.robot.sensor_system.ir_proximity_sensor.get_distance_in_inches() <= 1:
                self.robot.sound_system.beeper.beep()
                time.sleep(0.5)
                self.move_arm_to_position(1750)
                break


    def drop_box(self):
        import time
        self.robot.sound_system.beeper.beep()
        time.sleep(0.5)
        self.move_arm_to_position(0)

    def first_box(self,inches,z):
        #take the first box and then move and put down the box
        self.take_box()
        duration_1 = ((inches*5)/6)/ z # time for taking box and move to the position
        self.robot.drive_system.spin_an_angle(ma.pi/2,1,self.k_for_degrees)
        self.robot.drive_system.go_straight_for_seconds(duration_1,50)
        self.robot.drive_system.spin_an_angle(ma.pi/2,-1,self.k_for_degrees)
        self.drop_box()
        self.robot.drive_system.go_straight_for_seconds(1, -50)
        self.robot.drive_system.spin_an_angle(ma.pi/2, -1,self.k_for_degrees)
        self.robot.drive_system.go_straight_for_seconds(duration_1,50)
        self.robot.drive_system.spin_an_angle(ma.pi/2, 1,self.k_for_degrees)
        self.robot.drive_system.go_straight_for_seconds(1, 50)






# move



# ----------------------------final_project------------------------------------------------------------------------------------------------
class frobot(object):
    def __init__(self):
        self.button_name = None
        self.last_button = None
        self.distance = None
        self.k = None
        self.inches = None
        self.frequency =None



#     put_boxes(frobot, robot)




