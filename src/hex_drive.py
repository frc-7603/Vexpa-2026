#region VEXcode Generated Robot Configuration
from vex import *
import urandom
import math

# Brain should be defined by default
brain=Brain()

# Robot configuration code
controller_1 = Controller(PRIMARY)


# wait for rotation sensor to fully initialize
wait(30, MSEC)


# Make random actually random
def initializeRandomSeed():
    wait(100, MSEC)
    random = brain.battery.voltage(MV) + brain.battery.current(CurrentUnits.AMP) * 100 + brain.timer.system_high_res()
    urandom.seed(int(random))
      
# Set random seed 
initializeRandomSeed()


def play_vexcode_sound(sound_name):
    # Helper to make playing sounds from the V5 in VEXcode easier and
    # keeps the code cleaner by making it clear what is happening.
    print("VEXPlaySound:" + sound_name)
    wait(5, MSEC)

# add a small delay to make sure we don't print in the middle of the REPL header
wait(200, MSEC)
# clear the console to make sure we don't have the REPL in the console
print("\033[2J")

#endregion VEXcode Generated Robot Configuration

# ------------------------------------------
# 
# 	Project:      VEXcode Project
#	Author:       VEX
#	Created:
#	Description:  VEXcode V5 Python Project
# 
# ------------------------------------------

# Library imports
from vex import *

# Begin project code

brain = Brain()
controller_1 = Controller(PRIMARY)
motor_right_front = Motor(Ports.PORT1, GearSetting.RATIO_18_1, False)
motor_left_front = Motor(Ports.PORT2, GearSetting.RATIO_18_1, False)
motor_right_back = Motor(Ports.PORT3, GearSetting.RATIO_18_1, False)
motor_left_back = Motor(Ports.PORT4, GearSetting.RATIO_18_1, False)

motor_right_front.set_position(0, DEGREES)
motor_left_front.set_position(0, DEGREES)
motor_right_back.set_position(0, DEGREES)
motor_left_back.set_position(0, DEGREES)

degrees_spun = 0

def strafe(mag_x, mag_y):

    lf_y = mag_y
    rf_y = -mag_y
    lb_y = lf_y
    rb_y = rf_y

    rf_x = mag_x
    rb_x = -mag_x
    lf_x = rf_x
    lb_x = rb_x

    mag_rf = (rf_x + rf_y) / 2
    mag_lf = (lf_x + lf_y) / 2
    mag_rb = (rb_x + rb_y) / 2
    mag_lb = (lb_x + lb_y) / 2

    return mag_rf, mag_lf, mag_rb, mag_lb

def reset_spin():
    global degrees_spun

    if degrees_spun > 1800:

        spin_amount = 3600 - degrees_spun
        motor_right_front.spin_for(FORWARD, spin_amount, DEGREES)
        motor_left_front.spin_for(FORWARD, spin_amount, DEGREES)
        motor_right_back.spin_for(FORWARD, spin_amount, DEGREES)
        motor_left_back.spin_for(FORWARD, spin_amount, DEGREES)

    else: 

        spin_amount = degrees_spun
        motor_right_front.spin_for(REVERSE, spin_amount, DEGREES)
        motor_left_front.spin_for(REVERSE, spin_amount, DEGREES)
        motor_right_back.spin_for(REVERSE, spin_amount, DEGREES)
        motor_left_back.spin_for(REVERSE, spin_amount, DEGREES)

    return

while (True):
    pos_axis3 = controller_1.axis3.position()
    pos_axis4 = controller_1.axis4.position()
    pos_axis1 = controller_1.axis1.position()

    controller_1.buttonB.pressed(reset_spin) # spin the robot to it's start position when button B is pressed

    if abs(pos_axis3) > abs(pos_axis1) or abs(pos_axis4) > abs(pos_axis1):

        voltages = [((x/100) * 12) for x in strafe(pos_axis4, pos_axis3)]

        motor_right_front.spin(FORWARD, voltages[0], VOLT)
        motor_left_front.spin(REVERSE, voltages[1], VOLT)
        motor_right_back.spin(FORWARD, voltages[2], VOLT)
        motor_left_back.spin(REVERSE, voltages[3], VOLT)

    elif abs(pos_axis1) > abs(pos_axis3):

        # degrees_spun wraps around at 3600
        # the ratio of wheel radius to robot radius is about 10:1 
        # so 10 revolutions of the wheels = 1 revolution of the robot approx.abs

        degrees_spun = degrees_spun % 3600
        spin_amount = (90 * abs(pos_axis1) / 100) / 10

        if pos_axis1 > 0:

            motor_right_front.spin_for(FORWARD, spin_amount, DEGREES)
            motor_left_front.spin_for(FORWARD, spin_amount, DEGREES)
            motor_right_back.spin_for(FORWARD, spin_amount, DEGREES)
            motor_left_back.spin_for(FORWARD, spin_amount, DEGREES)
            degrees_spun += spin_amount
            
        else: 

            motor_right_front.spin_for(REVERSE, spin_amount, DEGREES)
            motor_left_front.spin_for(REVERSE, spin_amount, DEGREES)
            motor_right_back.spin_for(REVERSE, spin_amount, DEGREES)
            motor_left_back.spin_for(REVERSE, spin_amount, DEGREES)
            degrees_spun -= spin_amount

    else:
        motor_right_front.stop(HOLD)
        motor_left_front.stop(HOLD)
        motor_right_back.stop(HOLD)
        motor_left_back.stop(HOLD)
    

    


