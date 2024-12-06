#region DEVICES
# Hardware configuration code
RightTopMotor = Motor(Ports.PORT1, GearSetting.RATIO_18_1, True)
RightBotMotor = Motor(Ports.PORT2, GearSetting.RATIO_18_1, False)
LeftTopMotor = Motor(Ports.PORT3, GearSetting.RATIO_18_1, False)
LeftBotMotor = Motor(Ports.PORT4, GearSetting.RATIO_18_1, True)
Controller1 = Controller(PRIMARY)
IntakeMotor = Motor(Ports.PORT12, GearSetting.RATIO_18_1, False)
RampMotor = Motor(Ports.PORT21, GearSetting.RATIO_18_1, True)
SlapMotor_A = Motor(Ports.PORT16, GearSetting.RATIO_36_1, True)
SlapMotor_B = Motor(Ports.PORT13, GearSetting.RATIO_36_1, False)
SlapMotorGroup = MotorGroup(SlapMotor_A, SlapMotor_B)
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

isRed = True # set to false when blue alliance; inverts auton turning

drivePause = False # flag to stop driving when manual auton commands are running
mogomechOn = False # flag for toggling mogomech

# Auton constants
BOT_CIRCUMFERENCE = 109.55 # distance between wheels
DEG_TO_CM = 7.66 # degrees of drivebase motor rotation per centimeter
RAMP_FULL_DEG = 1241 # full ramp turn in motor degrees
autonVel = 20 # drivebase velocity in auton
autonRamVel = 50 # velocity for ramming into rings
autonRamDist = 0 # distance to ram into rings for

# Intake
intakeVel = 100
rampVel = 100
# Slapping thing
slapVel = 50

# Shake settings
shakeVel = 100 # motor % vel when shaking
shakeInterval = 150 # delay between alternating shake directions (ms)
straightShake = True # move forward-back (true) or spin left-right (false)
shakeRumble = "." # rumble pattern as morse code (...---...)
# for storing shake speed modifier
shakeLeftVel = 0
shakeRightVel = 0

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
    global shakeLeftVel, shakeRightVel, drivePause
    while True:
        if not drivePause: # this flag is set when manual auton commands are running
            # Set both sides to thrust stick initially
            driveLeftVel = Controller1.axis3.position()
            driveRightVel = Controller1.axis3.position()

            # Change vel based on steering (right) stick
            driveLeftVel = driveLeftVel + Controller1.axis1.position()
            driveRightVel = driveRightVel - Controller1.axis1.position()

            # Mux with shake (if any) and apply to drivebase
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
def ramp_bw(): # L2
    RampMotor.spin(FORWARD)
def ramp_stop():
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
def slap_back(): # bring slapper to the upright (before slap) position
    # resetting to 0 and using spin_for to stop spinning into robot (_for sets a direction, _to_position doesn't)
    SlapMotorGroup.spin(REVERSE)
# spin while A held
def slap_forward(): 
    SlapMotorGroup.spin(FORWARD)
def slap_stop():
    SlapMotorGroup.stop()

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
    global BOT_CIRCUMFERENCE, isRed
    leftTurnDist = BOT_CIRCUMFERENCE * (deg / 360)
    if isRed:
        auton_move_left_side_cm(-(leftTurnDist))
        auton_move_right_side_cm(leftTurnDist)
    else:
        auton_move_left_side_cm(leftTurnDist)
        auton_move_right_side_cm(-(leftTurnDist))
    wait_for_motion_stop()

def auton_turn_right_deg(deg):
    global BOT_CIRCUMFERENCE
    rightTurnDist = BOT_CIRCUMFERENCE * (deg / 360)
    if isRed:
        auton_move_left_side_cm(rightTurnDist)
        auton_move_right_side_cm(-(rightTurnDist))
    else:
        auton_move_left_side_cm(-(rightTurnDist))
        auton_move_right_side_cm(rightTurnDist)
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

# Grab ring, but don't score
def auton_take_ring():
    IntakeMotor.spin(FORWARD)
    wait(3, SECONDS)
    IntakeMotor.stop()
# Score ring
def auton_score_ring():
    global autonRamVel, autonVel, RAMP_FULL_DEG
    IntakeMotor.spin(FORWARD)
    RampMotor.spin_for(FORWARD, RAMP_FULL_DEG, DEGREES)
    IntakeMotor.stop()
    # set drivebase velocity back to normal

#endregion AUTON TOOLKIT
#region AUTON SEQUENCE
def auton_sequence():
    auton_turn_left(110)
    auton_move_straight(-160)
    auton_turn_left(12)
    auton_move_straight(-10)
    toggle_mogomech()
    auton_score_ring()
    auton_turn_right(80)
    auton_move_straight(16)

#endregion AUTON SEQUENCE
#region DEBUG
#---------#
#  DEBUG  #
#---------#

# manual controls for launching auton routines - to make routes
def debug_fn():
    global drivePause, autonVel, autonRamDist

    lastAction = ""
    repeat = 0

    while True:
        # Print regular debug
        # Brain screen
        brain.screen.clear_screen()
        brain.screen.set_cursor(1,1)
        brain.screen.print("RightTopMotor (1): temp=",RightTopMotor.temperature(PERCENT),"%"," pos=",RightTopMotor.position(), precision=brain_precision, sep="")
        brain.screen.next_row()
        brain.screen.print("RightBotMotor (2): temp=",RightBotMotor.temperature(PERCENT),"%"," pos=",RightBotMotor.position(), precision=brain_precision, sep="")
        brain.screen.next_row()
        brain.screen.print("LeftTopMotor (3): temp=",LeftTopMotor.temperature(PERCENT),"%"," pos=",LeftTopMotor.position(), precision=brain_precision, sep="")
        brain.screen.next_row()
        brain.screen.print("LeftBotMotor (4): temp=",LeftBotMotor.temperature(PERCENT),"%"," pos=",LeftBotMotor.position(), precision=brain_precision, sep="")
        brain.screen.next_row()
        brain.screen.print("Ramp (21): pos=", RampMotor.position(), sep="", precision=brain_precision)
        brain.screen.next_row()
        brain.screen.print("Intake (12): pos=", IntakeMotor.position(), sep="", precision=brain_precision)
        brain.screen.next_row()
        brain.screen.print("Slap (16): pos=", SlapMotorGroup.position(), sep="", precision=brain_precision)
        brain.screen.next_row()
        brain.screen.print("RingDistanceSensor (20): ",RingDistanceSensor.object_distance(MM), "mm", precision=brain_precision, sep="")
        # Controller screen
        Controller1.screen.clear_row(1)
        Controller1.screen.clear_row(2)
        Controller1.screen.set_cursor(1,1)
        Controller1.screen.print("1 ",RightTopMotor.temperature(PERCENT),"% ",sep="",precision=0)
        Controller1.screen.print("2 ",RightBotMotor.temperature(PERCENT),"%",sep="",precision=0)
        Controller1.screen.next_row()
        Controller1.screen.print("3 ",LeftTopMotor.temperature(PERCENT),"% ",sep="",precision=0)
        Controller1.screen.print("4 ",LeftBotMotor.temperature(PERCENT),"%",sep="",precision=0)

        # Manual auton commands
        if Controller1.buttonL1.pressing():
            if Controller1.buttonUp.pressing():
                drivePause = True
                wait(20, MSEC)
                set_all_motor_vel(autonVel)
                if lastAction != "lfw":
                    repeat = 1
                    lastAction = "lfw"
                else:
                    repeat += 1
                auton_move_straight_cm(2,True)

                Controller1.screen.set_cursor(3,1)
                Controller1.screen.clear_row(3)
                Controller1.screen.print(repeat*2, "fw")
                drivePause = False
            
            if Controller1.buttonDown.pressing():
                drivePause = True
                wait(20, MSEC)
                set_all_motor_vel(autonVel)
                if lastAction != "lbw":
                    repeat = 1
                    lastAction = "lbw"
                else:
                    repeat += 1
                auton_move_straight_cm(-2,True)
    
                Controller1.screen.set_cursor(3,1)
                Controller1.screen.clear_row(3)
                Controller1.screen.print(2*repeat, "bw")
                drivePause = False

            if Controller1.buttonLeft.pressing():
                drivePause = True
                wait(20, MSEC)
                set_all_motor_vel(autonVel)
                if lastAction != "ll":
                    repeat = 1
                    lastAction = "ll"
                else:
                    repeat += 1
                auton_turn_left_deg(5)
    
                Controller1.screen.set_cursor(3,1)
                Controller1.screen.clear_row(3)
                Controller1.screen.print(repeat*5, "deg left")
                drivePause = False

            if Controller1.buttonRight.pressing():
                drivePause = True
                wait(20, MSEC)
                set_all_motor_vel(autonVel)
                if lastAction != "lr":
                    repeat = 1
                    lastAction = "lr"
                else:
                    repeat += 1
                auton_turn_right_deg(5)
    
                Controller1.screen.set_cursor(3,1)
                Controller1.screen.clear_row(3)
                Controller1.screen.print(repeat*5, "deg right")
                drivePause = False
    
            if Controller1.buttonA.pressing():
                drivePause = True
                wait(20, MSEC)
                set_all_motor_vel(autonVel)
                auton_score_ring(autonRamDist)
                Controller1.screen.set_cursor(3,1)
                Controller1.screen.clear_row(3)
                Controller1.screen.print("score ring")
                drivePause = False

        else:
            if Controller1.buttonUp.pressing():
                drivePause = True
                wait(20, MSEC)
                set_all_motor_vel(autonVel)
                if lastAction != "fw":
                    repeat = 1
                    lastAction = "fw"
                else:
                    repeat += 1
                auton_move_straight_cm(10,True)
    
                Controller1.screen.set_cursor(3,1)
                Controller1.screen.clear_row(3)
                Controller1.screen.print(repeat*10, "fw")
                drivePause = False                
            
            if Controller1.buttonDown.pressing():
                drivePause = True
                wait(20, MSEC)
                set_all_motor_vel(autonVel)
                if lastAction != "bw":
                    repeat = 1
                    lastAction = "bw"
                else:
                    repeat += 1
                auton_move_straight_cm(-10,True)
    
                Controller1.screen.set_cursor(3,1)
                Controller1.screen.clear_row(3)
                Controller1.screen.print(10*repeat, "bw")
                drivePause = False
    
            if Controller1.buttonLeft.pressing():
                drivePause = True
                wait(20, MSEC)
                set_all_motor_vel(autonVel)
                if lastAction != "l":
                    repeat = 1
                    lastAction = "l"
                else:
                    repeat += 1
                auton_turn_left_deg(10)
    
                Controller1.screen.set_cursor(3,1)
                Controller1.screen.clear_row(3)
                Controller1.screen.print(repeat*10, "deg left")
                drivePause = False
    
            if Controller1.buttonRight.pressing():
                drivePause = True
                wait(20, MSEC)
                set_all_motor_vel(autonVel)
                if lastAction != "r":
                    repeat = 1
                    lastAction = "r"
                else:
                    repeat += 1
                auton_turn_right_deg(10)
    
                Controller1.screen.set_cursor(3,1)
                Controller1.screen.clear_row(3)
                Controller1.screen.print(repeat*10, "deg right")
                drivePause = False

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
Controller1.buttonX.pressed(slap_back)
Controller1.buttonA.pressed(slap_forward)

# releases
Controller1.buttonY.released(shake_stop)

Controller1.buttonL1.released(ramp_stop)
Controller1.buttonL2.released(ramp_stop)
Controller1.buttonR1.released(intake_stop)
Controller1.buttonR2.released(intake_stop)

Controller1.buttonA.released(slap_stop)
Controller1.buttonX.released(slap_stop)

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
    SlapMotorGroup.set_velocity(slapVel, PERCENT)

# For starting auton mode
def auton_init():
    global autonVel
    set_all_motor_vel(autonVel)
    
    auton_tasks = [
        Thread(auton_sequence),
        Thread(debug_fn)
    ]
    # wait for the driver control period to end
    while(competition.is_autonomous() and competition.is_enabled()):
        wait( 10, MSEC )
    # stop tasks
    for t in auton_tasks:
        t.stop()

# For starting driver mode
def drive_init():
    # start driver mode tasks - put functions that run in driver mode in driver_tasks
    driver_tasks = [
        Thread(driver_control),
        Thread(debug_fn)
    ]

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