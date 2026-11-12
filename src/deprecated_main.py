#region VEXcode Generated Robot Configuration
from vex import *
import urandom
import math

# Brain should be defined by default
brain=Brain()

# Robot configuration code
claw_motor = Motor(Ports.PORT3, GearSetting.RATIO_18_1, False)
arm_motor = Motor(Ports.PORT8, GearSetting.RATIO_18_1, False)
controller_1 = Controller(PRIMARY)
left_motor = Motor(Ports.PORT1, GearSetting.RATIO_18_1, False)
right_motor = Motor(Ports.PORT10, GearSetting.RATIO_18_1, True)


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

# ----------------------------------------------------------------------------
#                                                                            
# 	Project:        Left Arcade Control
#	Description:    This example will use the left X/Y Controller
#                   axis to control the Clawbot.
#   Configuration:  V5 Clawbot (Individual Motors)
#                   Controller
#                   Claw Motor in Port 3
#                   Arm Motor in Port 8
#                   Left Motor in Port 1
#                   Right Motor in Port 10    
#                                                                            
# ----------------------------------------------------------------------------
 
# Library imports
from vex import *

# Begin project code

# Montanari-Bot: Radio (Port1), Left_Motor (Port2), Right_Motor (Port3), Chain (Port5), Wheel (Port4)
# 

LOOP_WAIT = (5, MSEC)
ONE_SECOND = (1000, MSEC)

controller_1 = Controller(PRIMARY)

left_motor = Motor(Ports.PORT2, GearSetting.RATIO_18_1, False)
right_motor = Motor(Ports.PORT3, GearSetting.RATIO_18_1, True)

chain_load_motor = Motor(Ports.PORT5, GearSetting.RATIO_18_1, False)
wheel_load_motor = Motor(Ports.PORT4, GearSetting.RATIO_18_1, True)

velocity = 0

# control variables
 
speed_offset = 1

creeps_per_loop = 1 # But ima creeeeep
creep_amount = 100 # Creep % per SECOND, cant be too creepy
creep_wait_time = (LOOP_WAIT[0]/ONE_SECOND[0])/creeps_per_loop

status_action = "Idle"
status_velocity = 0
status_target = 0
status_axes = (0, 0)

def controller_status(action=None, velocity=None, target=None, axes=None):
    pass

    """
    global status_action, status_velocity, status_target, status_axes

    # Update only if NOT None, because 0 is "false" 
    if action is not None:
        status_action = action

    if velocity is not None:
        status_velocity = velocity

    if target is not None:
        status_target = target

    if axes is not None:
        status_axes = axes

    axis1, axis2 = status_axes

    controller_1.screen.clear_screen()

    controller_1.screen.set_cursor(1, 9)
    controller_1.screen.print(f"Action: {status_action}")

    controller_1.screen.set_cursor(2, 1)
    controller_1.screen.print(f"Vel: {status_velocity:.1f}% | Tgt: {status_target:.1f}%")

    controller_1.screen.set_cursor(3, 1)
    controller_1.screen.print(f"Axes: {axis1:.2f}, {axis2:.2f}")
    """


def get_sign_from_target(currentv, target):
    
    if currentv < target:
        return 1
    
    elif currentv > target:
        return -1
    
    return 0

# We have to make it lurk and creep so that it doesnt jerk and leap
def lurk_cycle(left_target, right_target):

    global left_motor, right_motor

    current_left = left_motor.velocity(PERCENT)
    current_right = right_motor.velocity(PERCENT)

    sign_left = get_sign_from_target(current_left, left_target)
    sign_right = get_sign_from_target(current_right, right_target)

    step = creep_amount * creep_wait_time

    new_left = current_left + sign_left * step
    new_right = current_right + sign_right * step

    # im clamping it
    # CLAMP BY TWICE/????
    if abs(left_target - new_left) < step:
        new_left = left_target

    if abs(right_target - new_right) < step:
        new_right = right_target

    left_motor.set_velocity(left_target, PERCENT)
    right_motor.set_velocity(right_target, PERCENT)

    #controller_status(
    #    velocity=current_right,
    #    target=right_target
    #)
    

def get_speed():

    forward = controller_1.axis3.position() / speed_offset
    turn = controller_1.axis4.position() / speed_offset

    left = forward + turn
    right = forward - turn

    return left, right


def loading_cycle(): # toggling cube motors based on button input
    
    global wheel_load_motor, chain_load_motor
    global velocity

    if controller_1.buttonUp.pressing(): # loading cubes via toggling motors

        controller_status(action="Intaking")

        wheel_load_motor.set_velocity(100,PERCENT)
        chain_load_motor.set_velocity(80, PERCENT)
        velocity = 100
    
    elif controller_1.buttonDown.pressing(): # de-loading cubes via reversing motors

        controller_status(action="Ejecting")

        wheel_load_motor.set_velocity(-100,PERCENT)
        chain_load_motor.set_velocity(-80, PERCENT)
        velocity = -100
    
    else: # stop motors otherwise

        controller_status(action="Idle")

        wheel_load_motor.set_velocity(0,PERCENT)
        chain_load_motor.set_velocity(0, PERCENT)
        velocity = 0


controller_1.screen.set_cursor(1, 1)
controller_1.screen.print("Action: Idle")

controller_1.screen.set_cursor(2, 1)
controller_1.screen.print(f"Vel: {velocity:.1f}% | Tgt: 0%")

controller_1.screen.set_cursor(3, 1)
controller_1.screen.print("Axes: 0, 0")

while True: # drive loop

    """
    controller_status(
        axes=(
            controller_1.axis3.position() / speed_offset, 
            controller_1.axis4.position() / speed_offset
        )
    )
    """

    loading_cycle()
    lurk_cycle(*get_speed()) # i'm on my megagrind

    left_motor.spin(FORWARD)
    right_motor.spin(FORWARD)
    
    wheel_load_motor.spin(FORWARD)
    chain_load_motor.spin(FORWARD)
    
    wait(*LOOP_WAIT)