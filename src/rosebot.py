"""
  Capstone Project.  Code to run on the EV3 robot (NOT on a laptop).

  This code is SHARED by all team members.  It contains both:
    -- High-level, general-purpose methods for a Snatch3r EV3 robot.
    -- Lower-level code to interact with the EV3 robot library.

  Author:  Your professors (for the framework and lower-level code)
    and Rishav Khosla and Shengjun Guan.
  Winter term, 2018-2019.
"""

import ev3dev.ev3 as ev3
import time
import math


###############################################################################
#    RoseBot class.
#
# NOTE TO STUDENTS:
#   You should construct a RoseBot for the Snatch3r robot.
#   Do ** NOT ** construct any instances of any other classes in this module,
#   since a RoseBot constructs instances of all the sub-systems that provide
#   ALL of the functionality available to a Snatch3r robot.
#
#   Use those sub-systems (and their instance variables)
#   to make the RoseBot (and its associated Snatch3r robot) do things.
###############################################################################
class RoseBot(object):
    def __init__(self):
        # Use these instance variables
        self.sensor_system = SensorSystem()
        self.drive_system = DriveSystem(self.sensor_system)
        self.arm_and_claw = ArmAndClaw(self.sensor_system.touch_sensor)


###############################################################################
#    DriveSystem
###############################################################################
class DriveSystem(object):
    """
    Controls the robot's motion via GO and STOP methods,
        along with various methods that GO/STOP under control of a sensor.
    """
    # -------------------------------------------------------------------------
    # NOTE:
    #   Throughout, when going straight:
    #     -- Positive speeds should make the robot move forward.
    #     -- Negative speeds should make the robot move backward.
    #   Throughout, when spinning:
    #     -- Positive speeds should make the robot spin in place clockwise
    #          (i.e., left motor goes at speed S, right motor at speed -S).
    #     -- Negative speeds should make the robot spin in place
    #          counter-clockwise
    #          (i.e., left motor goes at speed -S, right motor at speed S).
    # -------------------------------------------------------------------------

    def __init__(self, sensor_system):
        """
        Stores the given SensorSystem object.
        Constructs two Motors (for the left and right wheels).
          :type sensor_system:  SensorSystem
        """
        self.sensor_system = sensor_system
        self.left_motor = Motor('B')
        self.right_motor = Motor('C')

        self.wheel_circumference = 1.3 * math.pi

    # -------------------------------------------------------------------------
    # Methods for driving with no external sensor (just the built-in encoders).
    # -------------------------------------------------------------------------

    def go(self, left_wheel_speed, right_wheel_speed):
        """ Makes the left and right wheel motors spin at the given speeds. """

    def stop(self):
        """ Stops the left and right wheel motors. """

    def go_straight_for_seconds(self, seconds, speed):
        """
        Makes the robot go straight (forward if speed > 0, else backward)
        at the given speed for the given number of seconds.
        """

    def go_straight_for_inches_using_time(self, inches, speed):
        """
        Makes the robot go straight at the given speed
        for the given number of inches, using the approximate
        conversion factor of 10.0 inches per second at 100 (full) speed.
        """

    def go_straight_for_inches_using_encoder(self, inches, speed):
        """
        Makes the robot go straight (forward if speed > 0, else backward)
        at the given speed for the given number of inches,
        using the encoder (degrees traveled sensor) built into the motors.
        """

    # -------------------------------------------------------------------------
    # Methods for driving that use the color sensor.
    # -------------------------------------------------------------------------

    def go_straight_until_intensity_is_less_than(self, intensity, speed):
        """
        Goes straight at the given speed until the intensity returned
        by the color_sensor is less than the given intensity.
        """

    def go_straight_until_intensity_is_greater_than(self, intensity, speed):
        """
        Goes straight at the given speed until the intensity returned
        by the color_sensor is greater than the given intensity.
        """

    def go_straight_until_color_is(self, color, speed):
        """
        Goes straight at the given speed until the color returned
        by the color_sensor is equal to the given color.
        """

    def go_straight_until_color_is_not(self, color, speed):
        """
        Goes straight at the given speed until the color returned
        by the color_sensor is NOT equal to the given color.
        """

    # -------------------------------------------------------------------------
    # Methods for driving that use the infrared proximity sensor.
    # -------------------------------------------------------------------------
    def go_forward_until_distance_is_less_than(self, inches, speed):
        """
        Goes forward at the given speed until the robot is less than
        the given number of inches from the nearest object that it senses.
        """

    def go_backward_until_distance_is_greater_than(self, inches, speed):
        """
        Goes straight at the given speed until the robot is greater than
        the given number of inches from the nearest object that it senses.
        Assumes that it senses an object when it starts.
        """

    def go_until_distance_is_within(self, delta_inches, speed):
        """
        Goes forward or backward, repeated as necessary, until the robot is
        within the given delta-inches from the nearest object that it senses.
        """

    # -------------------------------------------------------------------------
    # Methods for driving that use the infrared beacon sensor.
    # -------------------------------------------------------------------------

    def spin_clockwise_until_beacon_heading_is_nonnegative(self, speed):
        pass

    def spin_counterclockwise_until_beacon_heading_is_nonpositive(self, speed):
        pass

    def go_straight_to_the_beacon(self, speed):
        """ Assumes that the Beacon is straight ahead. """
        pass

    # -------------------------------------------------------------------------
    # Methods for driving that use the camera.
    # -------------------------------------------------------------------------


###############################################################################
#    ArmAndClaw
###############################################################################
class ArmAndClaw(object):
    """ Controls the robot's arm and claw (which operate together). """
    # -------------------------------------------------------------------------
    # NOTE:
    #   A POSITIVE speed for the ArmAndClaw's motor moves the arm UP.
    #   A NEGATIVE speed for the ArmAndClaw's motor moves the arm DOWN.
    #   It takes   14.2 revolutions    of the ArmAndClaw's motor
    #     to go from all the way UP to all the way DOWN.
    # -------------------------------------------------------------------------

    def __init__(self, touch_sensor):
        """
        Stores the given touch sensor for stopping the Arm in its UP position.
        Constructs the Arm's motor.
          :type  touch_sensor:  TouchSensor
        """
        self.touch_sensor = touch_sensor
        self.motor = Motor('A', motor_type='medium')

    def raise_arm(self):
        """ Raises the Arm until its touch sensor is pressed. """
        self.motor.turn_on(100)
        while True:
            if self.touch_sensor.is_pressed():
                self.motor.turn_off()
                break

    def calibrate_arm(self):
        """
        Calibrates its Arm, that is:
          1. Raises its Arm until it is all the way UP
               (i.e., its touch sensor is pressed)
          2. Lowers its Arm until it is all the way down
               (i.e., 14.2 motor revolutions),
          3. Resets the motor's position to 0.
        """

    def move_arm_to_position(self, desired_arm_position):
        """
        Move its Arm to the given position, where 0 means all the way DOWN.
        The robot must have previously calibrated its Arm.
        """
        self.motor.turn_on(100)
        while True:
            if self.motor.get_position() == desired_arm_position:
                self.motor.turn_off()
                break

    def lower_arm(self):
        """
        Lowers the Arm until it is all the way down, i.e., position 0.
        The robot must have previously calibrated its Arm.
        """
        self.motor.turn_on(100)
        while True:
            if self.motor.get_position() == 0:
                self.motor.turn_off()
                break


###############################################################################
#    SensorSystem
###############################################################################
class SensorSystem(object):
    """
    Has all the sensor objects available to the Snatch3r robot, including
    the Button objects that form part of the BeaconSystem and DisplaySystem.
    Use this object to get   ** any **   sensor reading.
    """
    def __init__(self, touch_sensor, color_sensor, ir_proximity_sensor,
                 ir_beacon_sensor, camera, beacon_system, display_system):
        self.touch_sensor = TouchSensor(1)
        # self.color_sensor = color_sensor
        # self.ir_proximity_sensor = ir_proximity_sensor
        # self.ir_beacon_sensor = ir_beacon_sensor
        # self.camera = camera
        # self.beacon_system = beacon_system
        # self.display_system = display_system


###############################################################################
#    SoundSystem
###############################################################################
class SoundSystem(object):
    """
    Has all the kinds of "noise makers" available to the Snatch3r robot.
    Use this object to make   ** any **   sounds.
    """
    def __init__(self, beeper, tone_maker, speech_maker, song_maker):
        self.beeper = beeper
        self.tone_maker = tone_maker
        self.speech_maker = speech_maker
        self.song_maker = song_maker

    def tones_until_touch_sensor_is_pressed(self):
        """
        Plays an increasing sequence of short tones,
        stopping when the touch sensor is pressed.
        """


###############################################################################
#    LEDSystem
###############################################################################
class LEDSystem(object):
    """
    Has the left and right LEDs on the Brick.
    """
    def __init__(self):
        """ Constructs and stores the left and right LED objects. """
        self.left_led = LED()
        self.right_led = LED()

    def turn_both_leds_off(self):
        """ Turns the left and right LEDs off. """

    def only_left_on(self):
        """ Turns the left LED on and the right LED off """

###############################################################################
#    BeaconSystem
###############################################################################

###############################################################################
#    DisplaySystem
###############################################################################


###############################################################################
###############################################################################
# Classes built directly upon the underlying EV3 robot modules.
# USE them, and AUGMENT them if you wish, but do NOT modify them.
#
# Sensors in the SensorSystem:
#   -- TouchSensor (also used in the ArmAndClaw)
#   -- ColorSensor
#   -- InfraredProximitySensor
#   -- InfraredBeaconSensor
#   -- Camera
#
# In the DriveSystem:
#   -- Motor
#
# In the SoundSystem:
#   -- Beeper
#   -- ToneMaker
#   -- SpeechMaker
#   -- SongPlayer
#
###############################################################################
###############################################################################
class Motor(object):

    def __init__(self, port, motor_type='large'):
        # port must be 'A', 'B', 'C', or 'D'.  Use 'arm' as motor_type for Arm.
        if motor_type == 'large':
            self._motor = ev3.LargeMotor('out' + port)
        elif motor_type == 'medium':
            self._motor = ev3.MediumMotor('out' + port)

    def turn_on(self, speed):  # speed must be -100 to 100
        self._motor.run_direct(duty_cycle_sp=speed)

    def turn_off(self):
        self._motor.stop(stop_action="brake")

    def get_position(self):  # Units are degrees (that the motor has rotated).
        return self._motor.position

    def reset_position(self):
        self._motor.position = 0


class TouchSensor(object):
    def __init__(self, port):  # port must be 1, 2, 3 or 4
        self._touch_sensor = ev3.TouchSensor('in' + str(port))

    def is_pressed(self):
        """ Returns True if this TouchSensor is pressed, else returns False """
        return self._touch_sensor.is_pressed


class ColorSensor(object):
    def __init__(self, port):  # port must be 1, 2, 3 or 4
        self._color_sensor = ev3.ColorSensor('in' + str(port))

    def get_reflected_light_intensity(self):
        """
        Shines red light and returns the intensity of the reflected light.
        The returned value is from 0 to 100,
        but in practice more like 3 to 90+ in our classroom lighting
        with our downward-facing 0.25-inches-from-the-ground sensor placement.
        """
        return self._color_sensor.reflected_light_intensity


class InfraredProximitySensor(object):

    def __init__(self, port):  # port must be 1, 2, 3 or 4
        self._ir_sensor = ev3.InfraredSensor('in' + str(port))

    def get_distance(self):
        """
        Returns the distance to the nearest object sensed by this IR sensor.
        Units are: XXX.
        """
        # DCM: Fix above units XXX and add info re width of range.
        return self._ir_sensor.proximity


class InfraredBeaconSensor(object):
    def __init__(self, port):   # port must be 1, 2, 3 or 4
        self._ir_sensor = ev3.InfraredSensor('in' + str(port))

    def get_distance(self):
        """
        Returns the distance to the Beacon when the Beacon is turned on.
        Units are: XXX.
        """
        # DCM: Fix above units XXX and add info re width of range.
        return self._ir_sensor.proximity

    def get_heading(self):
        """
        Returns the heading (direction) to the Beacon when the Beacon
        is turned on.  Units are degrees (positive for clockwise, XXX).
        """
        # DCM: Fix above units XXX and add info re width of range.
        return self._ir_sensor.proximity


class Beeper(object):
    def __init__(self):
        self._beeper = ev3.Sound

    def beep(self):
        # DCM: Indicate that this is NON-blocking.
        # DCM: Indicate that returns a subprocess.Popen, which has a WAIT method
        return self._beeper.beep()


class ToneMaker(object):
    def __init__(self):
        self._tone_maker = ev3.Sound

    def tone(self, frequency, duration):
        # DCM: Indicate that this is NON-blocking.
        # DCM: Indicate that returns a subprocess.Popen, which has a WAIT method
        return self._tone_maker.tone(frequency, duration)  # MHz, msec  DCM XXX CTO


class SpeechMaker(object):
    pass


class SongMaker(object):
    pass


class LED(object):
    pass


class BeaconButton(object):
    pass


class BrickButton(object):
    pass
