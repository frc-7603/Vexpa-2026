#region VEXcode Generated Robot Configuration
from vex import *
import urandom
import math

# Brain should be defined by default
brain=Brain()

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

# Create the motors
left_motor  = Motor(Ports.PORT10, GearSetting.RATIO_18_1, False)
right_motor = Motor(Ports.PORT2, GearSetting.RATIO_18_1, True)

# Create the drivetrain (wheelTravel, trackWidth, wheelBase in mm, gear ratio)
drivetrain = DriveTrain(left_motor, right_motor,
                        319.19,   # wheel circumference (4" wheels) [web:11]
                        295,      # track width (distance between left and right wheels) [web:11]
                        40,       # wheelbase (front‑back distance) [web:11]
                        MM,       # Distance Units (MM)
                        1         # external gear ratio [web:11]
)

# Create the controller
controller = Controller(PRIMARY)

# Dynamically Adjust the speed
left_speed = controller.axis3.position() + controller.axis1.position()

def when_started():
    # drive forward 10 inches
    #drivetrain.drive_for(FORWARD, 10, INCHES)    # [web:11]
    
    left_motor.set_velocity(20, RPM)
    
    brain.screen.print("VEXcode")

    #drivetrain.set_drive_velocity(0.1, PERCENT);
    #drivetrain.drive_for(LEFT, 10, INCHES)
    # turn right 90 degrees (approx by time or distance, or use SmartDrive if you have inertial) [web:15]

when_started()

while True:

    if controller.buttonR1.pressing():
        
        left_motor.set_velocity(controller.axis3.position() + controller.axis1.position(), PERCENT)
        left_motor.spin(FORWARD)
        
    else:
        left_motor.stop()