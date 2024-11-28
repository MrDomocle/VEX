#region VEXcode Generated Robot Configuration
from vex import *
import urandom

# Brain should be defined by default
brain=Brain()

# Robot configuration code
RightMid = Motor(Ports.PORT1, GearSetting.RATIO_18_1, True)
RightBot = Motor(Ports.PORT2, GearSetting.RATIO_18_1, False)
LeftMid = Motor(Ports.PORT3, GearSetting.RATIO_18_1, False)
LeftBot = Motor(Ports.PORT4, GearSetting.RATIO_18_1, True)
controller_1 = Controller(PRIMARY)
Intake = Motor(Ports.PORT12, GearSetting.RATIO_18_1, False)
Ramp = Motor(Ports.PORT21, GearSetting.RATIO_18_1, True)
digital_out_a = DigitalOut(brain.three_wire_port.a)
RingDistance = Distance(Ports.PORT20)


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



# define variables used for controlling motors based on controller inputs
controller_1_left_shoulder_control_motors_stopped = True
controller_1_right_shoulder_control_motors_stopped = True

# define a task that will handle monitoring inputs from controller_1
def rc_auto_loop_function_controller_1():
    global controller_1_left_shoulder_control_motors_stopped, controller_1_right_shoulder_control_motors_stopped, remote_control_code_enabled
    # process the controller input every 20 milliseconds
    # update the motors based on the input values
    while True:
        if remote_control_code_enabled:
            # check the buttonL1/buttonL2 status
            # to control Ramp
            if controller_1.buttonL1.pressing():
                Ramp.spin(REVERSE)
                controller_1_left_shoulder_control_motors_stopped = False
            elif controller_1.buttonL2.pressing():
                Ramp.spin(FORWARD)
                controller_1_left_shoulder_control_motors_stopped = False
            elif not controller_1_left_shoulder_control_motors_stopped:
                Ramp.stop()
                # set the toggle so that we don't constantly tell the motor to stop when
                # the buttons are released
                controller_1_left_shoulder_control_motors_stopped = True
            # check the buttonR1/buttonR2 status
            # to control Intake
            if controller_1.buttonR1.pressing():
                Intake.spin(REVERSE)
                controller_1_right_shoulder_control_motors_stopped = False
            elif controller_1.buttonR2.pressing():
                Intake.spin(FORWARD)
                controller_1_right_shoulder_control_motors_stopped = False
            elif not controller_1_right_shoulder_control_motors_stopped:
                Intake.stop()
                # set the toggle so that we don't constantly tell the motor to stop when
                # the buttons are released
                controller_1_right_shoulder_control_motors_stopped = True
        # wait before repeating the process
        wait(20, MSEC)

# define variable for remote controller enable/disable
remote_control_code_enabled = True

rc_auto_loop_thread_controller_1 = Thread(rc_auto_loop_function_controller_1)

#endregion VEXcode Generated Robot Configuration

vexcode_brain_precision = 0
vexcode_console_precision = 0
vexcode_controller_1_precision = 0
myVariable = 0
driveRightVel = 0
driveLeftVel = 0
leftCentimeters = 0
rightCentimeters = 0
rightTurnDist = 0
leftTurnDist = 0
botCircumference = 0
autonVel = 0
autonRamVel = 0
autonRamDistance = 0
finalLeftVel = 0
finalRightVel = 0
shakeLeftVel = 0
shakeRightVel = 0
shakeVel = 0
shakeInterval = 0
Mogomech = False
shake = False
shakeDir = False
straightShake = False

def score_ring_ram_ram(score_ring_ram_ram__ram):
    global myVariable, driveRightVel, driveLeftVel, leftCentimeters, rightCentimeters, rightTurnDist, leftTurnDist, botCircumference, autonVel, autonRamVel, autonRamDistance, finalLeftVel, finalRightVel, shakeLeftVel, shakeRightVel, shakeVel, shakeInterval, Mogomech, shake, shakeDir, straightShake, vexcode_brain_precision, vexcode_console_precision, vexcode_controller_1_precision
    if score_ring_ram_ram__ram:
        # Faster motors for ramming
        RightMid.set_velocity(autonRamVel, PERCENT)
        RightBot.set_velocity(autonRamVel, PERCENT)
        LeftMid.set_velocity(autonRamVel, PERCENT)
        LeftBot.set_velocity(autonRamVel, PERCENT)
        move_straight_centimeters_wait_wait(10, False)
    Intake.spin(FORWARD)
    while not RingDistance.object_distance(MM) < 23:
        wait(5, MSEC)
    wait(0.25, SECONDS)
    Intake.stop()
    Ramp.spin_for(FORWARD, 5, TURNS)
    # Set velocity back to normal
    RightMid.set_velocity(autonVel, PERCENT)
    RightBot.set_velocity(autonVel, PERCENT)
    LeftMid.set_velocity(autonVel, PERCENT)
    LeftBot.set_velocity(autonVel, PERCENT)
    while not Ramp.is_done():
        wait(5, MSEC)

def move_straight_centimeters_wait_wait(move_straight_centimeters_wait_wait__centimeters, move_straight_centimeters_wait_wait__wait):
    global myVariable, driveRightVel, driveLeftVel, leftCentimeters, rightCentimeters, rightTurnDist, leftTurnDist, botCircumference, autonVel, autonRamVel, autonRamDistance, finalLeftVel, finalRightVel, shakeLeftVel, shakeRightVel, shakeVel, shakeInterval, Mogomech, shake, shakeDir, straightShake, vexcode_brain_precision, vexcode_console_precision, vexcode_controller_1_precision
    move_left_side_centimeters(move_straight_centimeters_wait_wait__centimeters)
    move_right_side_centimeters(move_straight_centimeters_wait_wait__centimeters)
    if move_straight_centimeters_wait_wait__wait:
        wait_for_motion_stop()

def turn_left_degrees(turn_left_degrees__degrees):
    global myVariable, driveRightVel, driveLeftVel, leftCentimeters, rightCentimeters, rightTurnDist, leftTurnDist, botCircumference, autonVel, autonRamVel, autonRamDistance, finalLeftVel, finalRightVel, shakeLeftVel, shakeRightVel, shakeVel, shakeInterval, Mogomech, shake, shakeDir, straightShake, vexcode_brain_precision, vexcode_console_precision, vexcode_controller_1_precision
    leftTurnDist = botCircumference * (turn_left_degrees__degrees / 360)
    move_left_side_centimeters(-(leftTurnDist))
    move_right_side_centimeters(leftTurnDist)
    wait_for_motion_stop()

def turn_right_degrees(turn_right_degrees__degrees):
    global myVariable, driveRightVel, driveLeftVel, leftCentimeters, rightCentimeters, rightTurnDist, leftTurnDist, botCircumference, autonVel, autonRamVel, autonRamDistance, finalLeftVel, finalRightVel, shakeLeftVel, shakeRightVel, shakeVel, shakeInterval, Mogomech, shake, shakeDir, straightShake, vexcode_brain_precision, vexcode_console_precision, vexcode_controller_1_precision
    rightTurnDist = botCircumference * (turn_right_degrees__degrees / 360)
    move_left_side_centimeters(rightTurnDist)
    move_right_side_centimeters(-(rightTurnDist))
    wait_for_motion_stop()

def move_left_side_centimeters(move_left_side_centimeters__centimeters):
    global myVariable, driveRightVel, driveLeftVel, leftCentimeters, rightCentimeters, rightTurnDist, leftTurnDist, botCircumference, autonVel, autonRamVel, autonRamDistance, finalLeftVel, finalRightVel, shakeLeftVel, shakeRightVel, shakeVel, shakeInterval, Mogomech, shake, shakeDir, straightShake, vexcode_brain_precision, vexcode_console_precision, vexcode_controller_1_precision
    leftCentimeters = math.fabs(move_left_side_centimeters__centimeters * 7.66)
    if move_left_side_centimeters__centimeters > 0:
        LeftMid.spin_for(FORWARD, leftCentimeters, DEGREES, wait=False)
        LeftBot.spin_for(FORWARD, leftCentimeters, DEGREES, wait=False)
    else:
        LeftMid.spin_for(REVERSE, leftCentimeters, DEGREES, wait=False)
        LeftBot.spin_for(REVERSE, leftCentimeters, DEGREES, wait=False)

def move_right_side_centimeters(move_right_side_centimeters__centimeters):
    global myVariable, driveRightVel, driveLeftVel, leftCentimeters, rightCentimeters, rightTurnDist, leftTurnDist, botCircumference, autonVel, autonRamVel, autonRamDistance, finalLeftVel, finalRightVel, shakeLeftVel, shakeRightVel, shakeVel, shakeInterval, Mogomech, shake, shakeDir, straightShake, vexcode_brain_precision, vexcode_console_precision, vexcode_controller_1_precision
    rightCentimeters = math.fabs(move_right_side_centimeters__centimeters * 7.66)
    if move_right_side_centimeters__centimeters > 0:
        RightMid.spin_for(FORWARD, leftCentimeters, DEGREES, wait=False)
        RightBot.spin_for(FORWARD, leftCentimeters, DEGREES, wait=False)
    else:
        RightMid.spin_for(REVERSE, leftCentimeters, DEGREES, wait=False)
        RightBot.spin_for(REVERSE, leftCentimeters, DEGREES, wait=False)

def mogomech_on():
    global myVariable, driveRightVel, driveLeftVel, leftCentimeters, rightCentimeters, rightTurnDist, leftTurnDist, botCircumference, autonVel, autonRamVel, autonRamDistance, finalLeftVel, finalRightVel, shakeLeftVel, shakeRightVel, shakeVel, shakeInterval, Mogomech, shake, shakeDir, straightShake, vexcode_brain_precision, vexcode_console_precision, vexcode_controller_1_precision
    digital_out_a.set(True)

def mogomech_off():
    global myVariable, driveRightVel, driveLeftVel, leftCentimeters, rightCentimeters, rightTurnDist, leftTurnDist, botCircumference, autonVel, autonRamVel, autonRamDistance, finalLeftVel, finalRightVel, shakeLeftVel, shakeRightVel, shakeVel, shakeInterval, Mogomech, shake, shakeDir, straightShake, vexcode_brain_precision, vexcode_console_precision, vexcode_controller_1_precision
    digital_out_a.set(False)

def wait_for_motion_stop():
    global myVariable, driveRightVel, driveLeftVel, leftCentimeters, rightCentimeters, rightTurnDist, leftTurnDist, botCircumference, autonVel, autonRamVel, autonRamDistance, finalLeftVel, finalRightVel, shakeLeftVel, shakeRightVel, shakeVel, shakeInterval, Mogomech, shake, shakeDir, straightShake, vexcode_brain_precision, vexcode_console_precision, vexcode_controller_1_precision
    while not (RightMid.is_done() and RightBot.is_done() and LeftMid.is_done() and LeftBot.is_done()):
        wait(5, MSEC)

def onauton_autonomous_0():
    global myVariable, driveRightVel, driveLeftVel, leftCentimeters, rightCentimeters, rightTurnDist, leftTurnDist, botCircumference, autonVel, autonRamVel, autonRamDistance, finalLeftVel, finalRightVel, shakeLeftVel, shakeRightVel, shakeVel, shakeInterval, Mogomech, shake, shakeDir, straightShake, vexcode_brain_precision, vexcode_console_precision, vexcode_controller_1_precision
    RightMid.set_velocity(autonVel, PERCENT)
    RightBot.set_velocity(autonVel, PERCENT)
    LeftMid.set_velocity(autonVel, PERCENT)
    LeftBot.set_velocity(autonVel, PERCENT)

def onauton_autonomous_1():
    global myVariable, driveRightVel, driveLeftVel, leftCentimeters, rightCentimeters, rightTurnDist, leftTurnDist, botCircumference, autonVel, autonRamVel, autonRamDistance, finalLeftVel, finalRightVel, shakeLeftVel, shakeRightVel, shakeVel, shakeInterval, Mogomech, shake, shakeDir, straightShake, vexcode_brain_precision, vexcode_console_precision, vexcode_controller_1_precision
    move_straight_centimeters_wait_wait(60, True)
    turn_right_degrees(45)
    score_ring_ram_ram(True)

def when_started1():
    global myVariable, driveRightVel, driveLeftVel, leftCentimeters, rightCentimeters, rightTurnDist, leftTurnDist, botCircumference, autonVel, autonRamVel, autonRamDistance, finalLeftVel, finalRightVel, shakeLeftVel, shakeRightVel, shakeVel, shakeInterval, Mogomech, shake, shakeDir, straightShake, vexcode_brain_precision, vexcode_console_precision, vexcode_controller_1_precision
    botCircumference = 109.55
    autonVel = 30
    autonRamVel = 100
    autonRamDistance = 20
    Intake.set_velocity(100, PERCENT)
    Ramp.set_velocity(100, PERCENT)
    Mogomech = False
    shakeVel = 100
    straightShake = True
    shakeInterval = 0.15

def onevent_controller_1buttonB_pressed_0():
    global myVariable, driveRightVel, driveLeftVel, leftCentimeters, rightCentimeters, rightTurnDist, leftTurnDist, botCircumference, autonVel, autonRamVel, autonRamDistance, finalLeftVel, finalRightVel, shakeLeftVel, shakeRightVel, shakeVel, shakeInterval, Mogomech, shake, shakeDir, straightShake, vexcode_brain_precision, vexcode_console_precision, vexcode_controller_1_precision
    Mogomech = not Mogomech
    if Mogomech:
        digital_out_a.set(True)
    else:
        digital_out_a.set(False)
    wait(0.5, SECONDS)

def when_started2():
    global myVariable, driveRightVel, driveLeftVel, leftCentimeters, rightCentimeters, rightTurnDist, leftTurnDist, botCircumference, autonVel, autonRamVel, autonRamDistance, finalLeftVel, finalRightVel, shakeLeftVel, shakeRightVel, shakeVel, shakeInterval, Mogomech, shake, shakeDir, straightShake, vexcode_brain_precision, vexcode_console_precision, vexcode_controller_1_precision
    while True:
        brain.screen.clear_screen()
        brain.screen.set_cursor(1, 1)
        brain.screen.print("RightMid (1): t=")
        brain.screen.print(RightMid.temperature(PERCENT), precision=6 if vexcode_brain_precision is None else vexcode_brain_precision)
        brain.screen.print("% pos=")
        brain.screen.print(RightMid.position(DEGREES), precision=6 if vexcode_brain_precision is None else vexcode_brain_precision)
        brain.screen.next_row()
        brain.screen.print("RightBot (2): t=")
        brain.screen.print(RightBot.temperature(PERCENT), precision=6 if vexcode_brain_precision is None else vexcode_brain_precision)
        brain.screen.print("% pos=")
        brain.screen.print(RightBot.position(DEGREES), precision=6 if vexcode_brain_precision is None else vexcode_brain_precision)
        brain.screen.next_row()
        brain.screen.print("LeftBot (3): t=")
        brain.screen.print(LeftMid.temperature(PERCENT), precision=6 if vexcode_brain_precision is None else vexcode_brain_precision)
        brain.screen.print("% pos=")
        brain.screen.print(LeftMid.position(DEGREES), precision=6 if vexcode_brain_precision is None else vexcode_brain_precision)
        brain.screen.next_row()
        brain.screen.print("LeftBot (4): t=")
        brain.screen.print(LeftBot.temperature(PERCENT), precision=6 if vexcode_brain_precision is None else vexcode_brain_precision)
        brain.screen.print("% pos=")
        brain.screen.print(LeftBot.position(DEGREES), precision=6 if vexcode_brain_precision is None else vexcode_brain_precision)
        brain.screen.next_row()
        brain.screen.print("RingDistance (20): ")
        brain.screen.print(RingDistance.object_distance(MM), precision=6 if vexcode_brain_precision is None else vexcode_brain_precision)
        brain.screen.print("mm")
        wait(0.2, SECONDS)
        wait(5, MSEC)

def ondriver_drivercontrol_0():
    global myVariable, driveRightVel, driveLeftVel, leftCentimeters, rightCentimeters, rightTurnDist, leftTurnDist, botCircumference, autonVel, autonRamVel, autonRamDistance, finalLeftVel, finalRightVel, shakeLeftVel, shakeRightVel, shakeVel, shakeInterval, Mogomech, shake, shakeDir, straightShake, vexcode_brain_precision, vexcode_console_precision, vexcode_controller_1_precision
    while True:
        # Set both sides to thrust stick
        driveLeftVel = controller_1.axis3.position()
        driveRightVel = controller_1.axis3.position()
        # Decrease if thrust is forward
        if controller_1.axis3.position() > 0:
            # <0 means we steer left, so we decrease left side
            if controller_1.axis1.position() < 0:
                # axis is <0 so we add to decrease
                driveLeftVel = driveLeftVel + controller_1.axis1.position()
            # >0 means we steer right, so we decrease right side
            if controller_1.axis1.position() > 0:
                # axis is >0 so we subtract to decrease
                driveRightVel = driveRightVel + -(controller_1.axis1.position())
        # Increase if thrust is forward
        if controller_1.axis3.position() < 0:
            # <0 means we steer left, so we increase left side
            if controller_1.axis1.position() < 0:
                # axis is <0 so we subtract to increase
                driveLeftVel = driveLeftVel + -(controller_1.axis1.position())
            # >0 means we steer right, so we decrease right side
            if controller_1.axis1.position() > 0:
                # axis is >0 so we add to increase
                driveRightVel = driveRightVel + controller_1.axis1.position()
        # Just set speeds if thrust is 0
        if controller_1.axis3.position() == 0:
            # Left
            if controller_1.axis1.position() < 0:
                driveRightVel = math.fabs(controller_1.axis1.position())
                driveLeftVel = -(math.fabs(controller_1.axis1.position()))
            # Right
            if controller_1.axis1.position() > 0:
                driveLeftVel = math.fabs(controller_1.axis1.position())
                driveRightVel = -(math.fabs(controller_1.axis1.position()))
        # Apply
        finalLeftVel = driveLeftVel + shakeLeftVel
        finalRightVel = driveRightVel + shakeRightVel
        RightMid.set_velocity(finalRightVel, PERCENT)
        RightBot.set_velocity(finalRightVel, PERCENT)
        LeftMid.set_velocity(finalLeftVel, PERCENT)
        LeftBot.set_velocity(finalLeftVel, PERCENT)
        RightMid.spin(FORWARD)
        RightBot.spin(FORWARD)
        LeftMid.spin(FORWARD)
        LeftBot.spin(FORWARD)
        # check temp
        wait(0.02, SECONDS)
        wait(5, MSEC)

def onevent_controller_1buttonY_pressed_0():
    global myVariable, driveRightVel, driveLeftVel, leftCentimeters, rightCentimeters, rightTurnDist, leftTurnDist, botCircumference, autonVel, autonRamVel, autonRamDistance, finalLeftVel, finalRightVel, shakeLeftVel, shakeRightVel, shakeVel, shakeInterval, Mogomech, shake, shakeDir, straightShake, vexcode_brain_precision, vexcode_console_precision, vexcode_controller_1_precision
    shake = True
    while shake:
        if shakeDir:
            if straightShake:
                shakeLeftVel = -(shakeVel)
                shakeRightVel = -(shakeVel)
            else:
                shakeLeftVel = -(shakeVel)
                shakeRightVel = shakeVel
        else:
            if straightShake:
                shakeLeftVel = shakeVel
                shakeRightVel = shakeVel
            else:
                shakeLeftVel = shakeVel
                shakeRightVel = -(shakeVel)
        controller_1.rumble("....")
        wait(shakeInterval, SECONDS)
        wait(5, MSEC)
    shakeLeftVel = 0
    shakeRightVel = 0

def onevent_controller_1buttonY_released_0():
    global myVariable, driveRightVel, driveLeftVel, leftCentimeters, rightCentimeters, rightTurnDist, leftTurnDist, botCircumference, autonVel, autonRamVel, autonRamDistance, finalLeftVel, finalRightVel, shakeLeftVel, shakeRightVel, shakeVel, shakeInterval, Mogomech, shake, shakeDir, straightShake, vexcode_brain_precision, vexcode_console_precision, vexcode_controller_1_precision
    shake = False

# create a function for handling the starting and stopping of all autonomous tasks
def vexcode_auton_function():
    # Start the autonomous control tasks
    auton_task_0 = Thread( onauton_autonomous_0 )
    auton_task_1 = Thread( onauton_autonomous_1 )
    # wait for the driver control period to end
    while( competition.is_autonomous() and competition.is_enabled() ):
        # wait 10 milliseconds before checking again
        wait( 10, MSEC )
    # Stop the autonomous control tasks
    auton_task_0.stop()
    auton_task_1.stop()

def vexcode_driver_function():
    # Start the driver control tasks
    driver_control_task_0 = Thread( ondriver_drivercontrol_0 )

    # wait for the driver control period to end
    while( competition.is_driver_control() and competition.is_enabled() ):
        # wait 10 milliseconds before checking again
        wait( 10, MSEC )
    # Stop the driver control tasks
    driver_control_task_0.stop()


# register the competition functions
competition = Competition( vexcode_driver_function, vexcode_auton_function )

# system event handlers
controller_1.buttonB.pressed(onevent_controller_1buttonB_pressed_0)
controller_1.buttonY.pressed(onevent_controller_1buttonY_pressed_0)
controller_1.buttonY.released(onevent_controller_1buttonY_released_0)
# add 15ms delay to make sure events are registered correctly.
wait(15, MSEC)

ws2 = Thread( when_started2 )
when_started1()