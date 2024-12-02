#region DEVICES
# Hardware configuration code
RightTopMotor = Motor(Ports.PORT1, GearSetting.RATIO_18_1, True)
RightBotMotor = Motor(Ports.PORT2, GearSetting.RATIO_18_1, False)
LeftTopMotor = Motor(Ports.PORT3, GearSetting.RATIO_18_1, False)
LeftBotMotor = Motor(Ports.PORT4, GearSetting.RATIO_18_1, True)
Controller1 = Controller(PRIMARY)
IntakeMotor = Motor(Ports.PORT12, GearSetting.RATIO_18_1, False)
RampMotor = Motor(Ports.PORT21, GearSetting.RATIO_18_1, True)
SlapMotor = Motor(Ports.PORT16, GearSetting.RATIO_36_1, True)
MogomechSolenoid = DigitalOut(brain.three_wire_port.a)
RingDistanceSensor = Distance(Ports.PORT20)

brain_precision = 0
vexcode_console_precision = 0
vexcode_controller_1_precision = 0

#endregion DEVICES
#region CONFIG
#Mathias washere ;)
#*************************#
#     MEGATRON CONFIG     #
#*************************#

myVariable = 0 # holy variable, we don't use it but i will personally execute anyone who removes it

# Mogomech state
mogomechOn = False

# Auton-specific
BOT_CIRCUMFERENCE = 109.55 # distance between wheels
DEG_TO_CM = 7.66 # degrees of drivebase motor rotation per centimeter
autonVel = 30 # drivebase velocity in auton
autonRamVel = 60 # velocity for ramming into rings

auton_debug = True # set this to true for auton functions in driver mode (also disables controller temperature display)

# Shake settings
shakeVel = 100 # % speed amplitude of shake
shakeInterval = 150 # delay between alternating directions (ms)
straightShake = True # move forward-back or spin left-right
shakeRumble = "-" # rumble pattern as morse code (...---...)
# for storing shake speed modifier
shakeLeftVel = 0
shakeRightVel = 0

# Intake
intakeVel = 100
rampVel = 100

# Slapping thing
slapVel = 50
readyToSlap = False

#endregion CONFIG
#********************#
#     CONFIG END     #
#********************#

# Shorthand for setting drivebase to a single velocity
# used everywhere
def set_all_motor_vel(vel):
    RightTopMotor.set_velocity(vel, PERCENT)
    RightBotMotor.set_velocity(vel, PERCENT)
    LeftTopMotor.set_velocity(vel, PERCENT)
    LeftBotMotor.set_velocity(vel, PERCENT)

#region DRIVE
#------------------#
# MANUAL FUNCTIONS #
#------------------#

# driving
def driver_control():
    global shakeLeftVel, shakeRightVel
    while True:
        # Set both sides to thrust stick
        driveLeftVel = Controller1.axis3.position()
        driveRightVel = Controller1.axis3.position()
        # Decrease if thrust is forward
        if Controller1.axis3.position() > 0:
            # <0 means steer left, so decrease left side
            if Controller1.axis1.position() < 0:
                driveLeftVel = driveLeftVel + Controller1.axis1.position()
            # >0 means steer right, so decrease right side
            if Controller1.axis1.position() > 0:
                driveRightVel = driveRightVel + -(Controller1.axis1.position())
        # Increase if thrust is forward
        if Controller1.axis3.position() < 0:
            # <0 means steer left, so increase left side
            if Controller1.axis1.position() < 0:
                driveLeftVel = driveLeftVel + -(Controller1.axis1.position())
            # >0 means steer right, so decrease right side
            if Controller1.axis1.position() > 0:
                driveRightVel = driveRightVel + Controller1.axis1.position()
        # Just set speeds if thrust is 0
        if Controller1.axis3.position() == 0:
            # Left
            if Controller1.axis1.position() < 0:
                driveRightVel = math.fabs(Controller1.axis1.position())
                driveLeftVel = -(math.fabs(Controller1.axis1.position()))
            # Right
            if Controller1.axis1.position() > 0:
                driveLeftVel = math.fabs(Controller1.axis1.position())
                driveRightVel = -(math.fabs(Controller1.axis1.position()))
        # Apply
        finalLeftVel = driveLeftVel + shakeLeftVel
        finalRightVel = driveRightVel + shakeRightVel

        RightTopMotor.set_velocity(finalRightVel, PERCENT)
        RightBotMotor.set_velocity(finalRightVel, PERCENT)
        LeftTopMotor.set_velocity(finalLeftVel, PERCENT)
        LeftBotMotor.set_velocity(finalLeftVel, PERCENT)

        RightTopMotor.spin(FORWARD)
        RightBotMotor.spin(FORWARD)
        LeftTopMotor.spin(FORWARD)
        LeftBotMotor.spin(FORWARD)

        wait(20, MSEC)

# Intake/ramp controls
def intake_fw(): # R1
    IntakeMotor.spin(REVERSE)
def intake_bw(): # R2
    IntakeMotor.spin(FORWARD)
def intake_stop():
    IntakeMotor.stop()

def ramp_fw(): # L1
    RampMotor.spin(REVERSE)
def ramp_bw():
    RampMotor.spin(FORWARD)
def ramp_stop(): # L2
    RampMotor.stop()

# Mogomech
def mogomech_toggle(): # 
    global mogomechOn
    mogomechOn = not mogomechOn
    if mogomechOn:
        MogomechSolenoid.set(True)
    else:
        MogomechSolenoid.set(False)

# Neutral stake slapper
def slap_ready(): # bring slapper to the upright (before slap) position
    global readyToSlap
    # resetting to 0 and using spin_for to stop spinning into robot (_for sets a direction, _to_position doesn't)
    SlapMotor.spin_to_position(0, DEGREES, wait=True)
    SlapMotor.spin_for(REVERSE, 180, DEGREES, wait=True)
    readyToSlap = True
# spin while A held
def slap_ring(): 
    global readyToSlap
    readyToSlap = False
    SlapMotor.spin(FORWARD)
def slap_stop():
    SlapMotor.stop()

# Shakey-shakey
def shake_start():
    global doShake, straightShake, shakeLeftVel, shakeRightVel, shakeVel, shakeInterval, shakeRumble
    shakeDir = True
    doShake = True
    while doShake: # repeat until stopShake sets this to False
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
        shakeDir = not shakeDir
        Controller1.rumble(shakeRumble)
        wait(shakeInterval, MSEC)

    # thread gets here when bot should be done shaking
    # set vel back to 0 after shaking is finished
    shakeLeftVel = 0
    shakeRightVel = 0
def shake_stop():
    global doShake
    doShake = False

#enregion DRIVE
#region AUTON TOOLKIT
#-----------------#
# AUTON FUNCTIONS #
#-----------------#

def wait_for_motion_stop():
    while not (RightTopMotor.is_done() and RightBotMotor.is_done() and LeftTopMotor.is_done() and LeftBotMotor.is_done()):
        wait(20, MSEC)

def auton_turn_left_deg(deg):
    global BOT_CIRCUMFERENCE
    leftTurnDist = BOT_CIRCUMFERENCE * (deg / 360)
    auton_move_left_side_cm(-(leftTurnDist))
    auton_move_right_side_cm(leftTurnDist)
    wait_for_motion_stop()

def auton_turn_right_deg(deg):
    global BOT_CIRCUMFERENCE
    rightTurnDist = BOT_CIRCUMFERENCE * (deg / 360)
    auton_move_left_side_cm(rightTurnDist)
    auton_move_right_side_cm(-(rightTurnDist))
    wait_for_motion_stop()

def auton_move_left_side_cm(d_cm):
    global DEG_TO_CM
    deg = math.fabs(d_cm * DEG_TO_CM)
    if d_cm > 0:
        LeftTopMotor.spin_for(FORWARD, deg, DEGREES, wait=False)
        LeftBotMotor.spin_for(FORWARD, deg, DEGREES, wait=False)
    else:
        LeftTopMotor.spin_for(REVERSE, deg, DEGREES, wait=False)
        LeftBotMotor.spin_for(REVERSE, deg, DEGREES, wait=False)

def auton_move_right_side_cm(d_cm):
    global DEG_TO_CM
    deg = math.fabs(d_cm * DEG_TO_CM)
    if d_cm > 0:
        RightTopMotor.spin_for(FORWARD, deg, DEGREES, wait=False)
        RightBotMotor.spin_for(FORWARD, deg, DEGREES, wait=False)
    else:
        RightTopMotor.spin_for(REVERSE, deg, DEGREES, wait=False)
        RightBotMotor.spin_for(REVERSE, deg, DEGREES, wait=False)

def auton_move_straight_cm(d_cm, wait=True):
    auton_move_left_side_cm(d_cm)
    auton_move_right_side_cm(d_cm)
    if wait:
        wait_for_motion_stop()

def auton_score_ring(ram):
    global autonRamVel, autonVel, autonRamDistance
    # ram into ring
    if ram > 0:
        # Faster motors for ramming
        set_all_motor_vel(autonRamVel)
        auton_move_straight_cm(ram, wait=False)
    IntakeMotor.spin(FORWARD)
    
    # wait until ring passes bottom intake
    while not RingDistanceSensor.object_distance(MM) < 23:
        wait(20, MSEC)
    wait(250, MSEC)
    IntakeMotor.stop()
    # set drivebase velocity back to normal
    set_all_motor_vel(autonVel)

    # take ring up
    RampMotor.spin_for(FORWARD, 5, TURNS)
    while not RampMotor.is_done():
        wait(20, MSEC)

#endregion AUTON TOOLKIT
#region AUTON SEQUENCE
def auton_sequence():
    auton_move_straight_cm(23, True)
    auton_turn_left_deg(45)
    auton_move_straight_cm(78)
    auton_score_ring(ram=True)

#endregion AUTON SEQUENCE
#region DEBUG
#---------#
#  DEBUG  #
#---------#

# manual controls for launching auton routines - to make routes
def auton_manual():
    set_all_motor_vel(autonVel)

    lastAction = ""
    repeat = 0

    while True:
        # L1 makes fw and bw run 2 cm instead of 10 for precise controls
        if Controller1.buttonL1.pressing():
            if Controller1.buttonUp.pressing():
                if lastAction != "lfw":
                    repeat = 1
                    lastAction = "lfw"
                else:
                    repeat += 1
                auton_move_straight_cm(2,True)
    
                Controller1.screen.set_cursor(2,1)
                Controller1.screen.clear_row(2)
                Controller1.screen.print(repeat*2, "fw")
                
            
            if Controller1.buttonDown.pressing():
                if lastAction != "lbw":
                    repeat = 1
                    lastAction = "lbw"
                else:
                    repeat += 1
                auton_move_straight_cm(-2,True)
    
                Controller1.screen.set_cursor(2,1)
                Controller1.screen.clear_row(2)
                Controller1.screen.print(2*repeat, "bw")

        else:
            if Controller1.buttonUp.pressing():
                if lastAction != "fw":
                    repeat = 1
                    lastAction = "fw"
                else:
                    repeat += 1
                auton_move_straight_cm(10,True)
    
                Controller1.screen.set_cursor(2,1)
                Controller1.screen.clear_row(2)
                Controller1.screen.print(repeat*10, "fw")
                
            
            if Controller1.buttonDown.pressing():
                if lastAction != "bw":
                    repeat = 1
                    lastAction = "bw"
                else:
                    repeat += 1
                auton_move_straight_cm(-10,True)
    
                Controller1.screen.set_cursor(2,1)
                Controller1.screen.clear_row(2)
                Controller1.screen.print(10*repeat, "bw")
    
            if Controller1.buttonLeft.pressing():
                if lastAction != "l":
                    repeat = 1
                    lastAction = "l"
                else:
                    repeat += 1
                auton_turn_left_deg(5)
    
                Controller1.screen.set_cursor(2,1)
                Controller1.screen.clear_row(2)
                Controller1.screen.print(repeat*5, "deg left")
    
            if Controller1.buttonRight.pressing():
                if lastAction != "r":
                    repeat = 1
                    lastAction = "r"
                else:
                    repeat += 1
                auton_turn_right_deg(5)
    
                Controller1.screen.set_cursor(2,1)
                Controller1.screen.clear_row(2)
                Controller1.screen.print(repeat*5, "deg right")
    
            if Controller1.buttonA.pressing():
                auton_score_ring(20)
                Controller1.screen.set_cursor(3,1)
                Controller1.screen.clear_row(3)
                Controller1.screen.print("score ring")

        wait(200, MSEC)


def draw_debug_brain():
    while True:
        RightTop_status = "SPINNING" if RightTopMotor.is_spinning() else "stopped"
        RightBot_status = "SPINNING" if RightBotMotor.is_spinning() else "stopped"
        LeftTop_status = "SPINNING" if LeftTopMotor.is_spinning() else "stopped"
        LeftBot_status = "SPINNING" if LeftTopMotor.is_spinning() else "stopped"
        # Brain screen
        brain.screen.clear_screen()
        brain.screen.set_cursor(1,1)
        brain.screen.print("RightTopMotor (1): t=",RightTopMotor.temperature(PERCENT),"% pos=",RightTopMotor.position(),RightTop_status, precision=brain_precision, sep="")
        brain.screen.next_row()
        brain.screen.print("RightBotMotor (2): t=",RightBotMotor.temperature(PERCENT),"% pos=",RightBotMotor.position(),RightBot_status, precision=brain_precision, sep="")
        brain.screen.next_row()
        brain.screen.print("LeftTopMotor (3): t=",LeftTopMotor.temperature(PERCENT),"% pos=",LeftTopMotor.position(),LeftTop_status, precision=brain_precision, sep="")
        brain.screen.next_row()
        brain.screen.print("LeftBotMotor (4): t=",LeftBotMotor.temperature(PERCENT),"% pos=",LeftBotMotor.position(),LeftBot_status, precision=brain_precision, sep="")
        brain.screen.next_row()
        brain.screen.print("RingDistanceSensor (20): ",RingDistanceSensor.object_distance(MM), "mm", precision=brain_precision, sep="")
def draw_debug_controller():
    while True:
        RightTop_status = "SPINNING" if RightTopMotor.is_spinning() else "stopped"
        RightBot_status = "SPINNING" if RightBotMotor.is_spinning() else "stopped"
        LeftTop_status = "SPINNING" if LeftTopMotor.is_spinning() else "stopped"
        LeftBot_status = "SPINNING" if LeftTopMotor.is_spinning() else "stopped"

        Controller1.screen.clear_screen()
        Controller1.screen.set_cursor(1,1)
        Controller1.screen.print("1:",RightTopMotor.temperature(PERCENT),RightTop_status[:1],sep="",precision=0)
        Controller1.screen.print("2:",RightBotMotor.temperature(PERCENT),RightBot_status[:1],sep="",precision=0)
        Controller1.screen.next_row()
        Controller1.screen.print("3:",LeftTopMotor.temperature(PERCENT),LeftTop_status[:1],sep="",precision=0)
        Controller1.screen.print("4:",LeftBotMotor.temperature(PERCENT),LeftBot_status[:1],sep="",precision=0)
        wait(200, MSEC)
        
#endregion DEBUG
#region INPUT
#--------------#
# INPUT CONFIG #
#--------------#

# shaky-shaky
Controller1.buttonY.pressed(shake_start)
# intake
Controller1.buttonL1.pressed(ramp_fw)
Controller1.buttonL2.pressed(ramp_bw)
Controller1.buttonR1.pressed(intake_fw)
Controller1.buttonR2.pressed(intake_bw)
# mogomech
Controller1.buttonB.pressed(mogomech_toggle)
# slapper
Controller1.buttonX.pressed(slap_ready)
Controller1.buttonA.pressed(slap_ring)

# releases
Controller1.buttonY.released(shake_stop)

Controller1.buttonL1.released(ramp_stop)
Controller1.buttonL2.released(ramp_stop)
Controller1.buttonR1.released(intake_stop)
Controller1.buttonR2.released(intake_stop)

Controller1.buttonA.released(slap_stop)

# Other keys:

#endregion INPUT
#region INIT
#-----------#
# INIT CODE #
#-----------#

# First code to run when bot boots up, always runs
def bot_init():
    global intakeVel, rampVel, slapVel
    IntakeMotor.set_velocity(intakeVel, PERCENT)
    RampMotor.set_velocity(rampVel, PERCENT)
    SlapMotor.set_velocity(slapVel, PERCENT)

# For starting auton mode
def auton_init():
    global autonVel
    set_all_motor_vel(autonVel)
    
    auton_task = Thread(auton_sequence)
    # wait for the driver control period to end
    while(competition.is_autonomous() and competition.is_enabled()):
        wait( 10, MSEC )
    auton_task.stop()

# For starting driver mode
def drive_init():
    # start driver mode tasks
    driver_tasks = [
            Thread(driver_control),
            Thread(draw_debug_brain)
        ]
    # auton_manual needs to print to controller
    if not auton_debug:
        driver_tasks.append(Thread(draw_debug_controller))
    else:
        driver_tasks.append(Thread(auton_manual))

    # Wait for the driver control period to end
    while(competition.is_driver_control() and competition.is_enabled()):
        wait( 10, MSEC )
    
    # stop all tasks
    for t in driver_tasks:
        t.stop()
    
# Register the competition functions
competition = Competition(drive_init, auton_init)

# Start program
bot_init()