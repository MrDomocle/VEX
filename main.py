#region DEVICES
# Hardware configuration code
RightTopMotor = Motor(Ports.PORT1, GearSetting.RATIO_18_1, True)
RightBotMotor = Motor(Ports.PORT2, GearSetting.RATIO_18_1, False)
LeftTopMotor = Motor(Ports.PORT3, GearSetting.RATIO_18_1, False)
LeftBotMotor = Motor(Ports.PORT4, GearSetting.RATIO_18_1, True)
Controller1 = Controller(PRIMARY)
IntakeMotor = Motor(Ports.PORT12, GearSetting.RATIO_18_1, False)
RampMotor = Motor(Ports.PORT21, GearSetting.RATIO_18_1, True)
MogomechSolenoid = DigitalOut(brain.three_wire_port.a)
RingDistanceSensor = Distance(Ports.PORT20)

brain_precision = 0
vexcode_console_precision = 0
vexcode_controller_1_precision = 0

#endregion DEVICES
#region CONFIG
#*************************#
#     MEGATRON CONFIG     #
#*************************#

myVariable = 0 # holy variable, we don't use it but i will personally execute anyone who removes it

# Mogomech
mogomechOn = False

# Auton-specific
BOT_CIRCUMFERENCE = 109.55 # distance between wheels
DEG_TO_CM = 7.66 # degrees of drivebase motor rotation per centimeter
autonVel = 30
autonRamVel = 100 # velocity for ramming into rings
autonRamDistance = 20 # how long to ram

# Shake settings
shakeVel = 100 # % speed amplitude of shake
shakeInterval = 150 # delay between alternating directions (ms)
straightShake = True # move forward-back or spin left-right
shakeRumble = ".."
# for storing shake speed modifier
shakeLeftVel = 0
shakeRightVel = 0

#endregion CONFIG
#********************#
#     CONFIG END     #
#********************#

# Shorthand for setting drivebase to a single velocity
def set_all_motor_vel(vel):
    RightTopMotor.set_velocity(vel, PERCENT)
    RightBotMotor.set_velocity(vel, PERCENT)
    LeftTopMotor.set_velocity(vel, PERCENT)
    LeftBotMotor.set_velocity(vel, PERCENT)

#region MANUAL CONTROL
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
l_shoulder_m_stopped = True
r_shoulder_m_stopped = True
def driver_intake():
    global l_shoulder_m_stopped, r_shoulder_m_stopped
    while True:
        # Ramp
        if Controller1.buttonL1.pressing():
            RampMotor.spin(REVERSE)
            l_shoulder_m_stopped = False
        elif Controller1.buttonL2.pressing():
            RampMotor.spin(FORWARD)
            l_shoulder_m_stopped = False
        elif not l_shoulder_m_stopped:
            RampMotor.stop()
            l_shoulder_m_stopped = True
        # Intake
        if Controller1.buttonR1.pressing():
            IntakeMotor.spin(REVERSE)
            r_shoulder_m_stopped = False
        elif Controller1.buttonR2.pressing():
            IntakeMotor.spin(FORWARD)
            r_shoulder_m_stopped = False
        elif not r_shoulder_m_stopped:
            IntakeMotor.stop()
            r_shoulder_m_stopped = True
        wait(20, MSEC)

# Mogomech controls
def mogomech_on():
    MogomechSolenoid.set(True)
def mogomech_off():
    MogomechSolenoid.set(False)

def mogomech_toggle():
    global mogomechOn
    mogomechOn = not mogomechOn
    if mogomechOn:
        MogomechSolenoid.set(True)
    else:
        MogomechSolenoid.set(False)
    wait(500, MSEC)

# Shakey-shakey
def driver_shake():
    global straightShake, shakeLeftVel, shakeRightVel, shakeVel, shakeInterval, shakeRumble
    shakeDir = True
    while True:
        while Controller1.buttonY.pressing():
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

        # set vel back to 0 after shaking is finished
        shakeLeftVel = 0
        shakeRightVel = 0
        wait(20, MSEC)

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
    if ram:
        # Faster motors for ramming
        set_all_motor_vel(autonRamVel)
        auton_move_straight_cm(autonRamDistance, wait=False)
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
        wait(5, MSEC)

#region AUTON SEQUENCE
def auton_sequence():
    auton_move_straight_cm(60, True)
    auton_turn_right_deg(45)
    auton_score_ring(ram=True)

#region DEBUG
#---------#
#  DEBUG  #
#---------#

def draw_debug():
    while True:
        RightTop_status = "SPINNING" if RightTopMotor.is_spinning() else "stopped"
        RightBot_status = "SPINNING" if RightBotMotor.is_spinning() else "stopped"
        LeftTop_status = "SPINNING" if LeftTopMotor.is_spinning() else "stopped"
        LeftBot_status = "SPINNING" if LeftTopMotor.is_spinning() else "stopped"
        # Brain screen
        brain.screen.clear_screen()
        brain.screen.set_cursor(1,1)
        brain.screen.print(f"RightTopMotor (1): t={RightTopMotor.temperature(PERCENT)}% pos={RightTopMotor.position()} {RightTop_status}", precision=brain_precision)
        brain.screen.next_row()
        brain.screen.print(f"RightBotMotor (2): t={RightBotMotor.temperature(PERCENT)}% pos={RightBotMotor.position()} {RightBot_status}", precision=brain_precision)
        brain.screen.next_row()
        brain.screen.print(f"LeftTopMotor (3): t={LeftTopMotor.temperature(PERCENT)}% pos={LeftTopMotor.position()} {LeftTop_status}", precision=brain_precision)
        brain.screen.next_row()
        brain.screen.print(f"LeftBotMotor (4): t={LeftBotMotor.temperature(PERCENT)}% pos={LeftBotMotor.position()} {LeftBot_status}", precision=brain_precision)
        brain.screen.next_row()
        brain.screen.print(f"RingDistanceSensor (20): {RingDistanceSensor.object_distance(MM)} mm", precision=brain_precision)
        # Controller screen (temp only)
        Controller1.screen.clear_screen()
        Controller1.screen.set_cursor(1,1)
        Controller1.screen.print(f"1:{RightTopMotor.temperature(PERCENT)}{RightTop_status}")
        Controller1.screen.print(f"2:{RightBotMotor.temperature(PERCENT)}{RightBot_status}")
        Controller1.screen.print(f"3:{LeftTopMotor.temperature(PERCENT)}{LeftTop_status}")
        Controller1.screen.print(f"4:{LeftBotMotor.temperature(PERCENT)}{LeftBot_status}")
        wait(200, MSEC)

#region INIT
#-----------#
# INIT CODE #
#-----------#

# First code to run when bot boots up, always runs
def bot_init():
    IntakeMotor.speed = 100
    RampMotor.speed = 100

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
    driver_control_task = Thread(driver_control)
    driver_shake_task = Thread(driver_shake)
    driver_intake_task = Thread(driver_intake)

    # wait for the driver control period to end
    while(competition.is_driver_control() and competition.is_enabled()):
        wait( 10, MSEC )
    driver_control_task.stop()

# Register the competition functions
competition = Competition(drive_init, auton_init)

# Start program
draw_debug_task = Thread(draw_debug)
bot_init()