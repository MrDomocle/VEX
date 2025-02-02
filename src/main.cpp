#include <cstdlib>
#include <string>
#include <cmath>
#include "main.h"
#include "lemlib/api.hpp" // IWYU pragma: keep

// ################### !!!!CHECK B4 EVERY GAME!!!!!
// AUTON SKILLS FALSE 4
// RED HEAD : FALSE 0
// BLUE HEAD : TRUE 0
bool blue = false;
int auton_mode = 1;

// MARK: HARDWARE
/**
   Hardware
           **/

pros::Controller master(pros::E_CONTROLLER_MASTER);
pros::MotorGroup left_mg({-1, 2}, pros::MotorGearset::green);
pros::MotorGroup right_mg({3, -4}, pros::MotorGearset::green);
pros::Motor right_top(-1, pros::MotorGearset::green);
pros::Motor right_bot(2, pros::MotorGearset::green);
pros::Motor left_top(3, pros::MotorGearset::green);
pros::Motor left_bot(-4, pros::MotorGearset::green);
pros::MotorGroup intake_mg({12, -21});
pros::Motor slap(-16);
pros::adi::DigitalOut mogo_solenoid(1);

pros::Rotation rot_y(9); // forward/back
pros::Rotation rot_x(10); // left/right
pros::Imu inertial(7); // heading
lemlib::Drivetrain drivetrain(&left_mg, &right_mg, 12.85, lemlib::Omniwheel::NEW_4, 280, 2);
lemlib::TrackingWheel track_y(&rot_y, lemlib::Omniwheel::NEW_275, 0.7);
lemlib::TrackingWheel track_x(&rot_x, lemlib::Omniwheel::NEW_275, 1.000);
lemlib::OdomSensors sensors(&track_y, nullptr, &track_x, nullptr, &inertial);
lemlib::ControllerSettings lateral_controller(10, // proportional gain (kP)
                                              0, // integral gain (kI)
                                              3, // derivative gain (kD)
                                              0, // anti windup
                                              0, // small error range, in inches
                                              0, // small error range timeout, in milliseconds
                                              0, // large error range, in inches
                                              0, // large error range timeout, in milliseconds
                                              0 // maximum acceleration (slew)
);
lemlib::ControllerSettings angular_controller(1,// proportional gain (kP)
                                              0, // integral gain (kI)
                                              20, // derivative gain (kD)
                                              0, // anti windup
                                              0, // small error range, in degrees
                                              0,//small error range timeout, in milliseconds
                                              0, // large error range, in degrees
                                              0, // large error range timeout, in milliseconds
                                              0 // maximum acceleration (slew)
);
lemlib::Chassis chassis(drivetrain, // drivetrain settings
                        lateral_controller, // lateral PID settings
                        angular_controller, // angular PID settings
                        sensors // odometry sensors
);
// MARK: BEHAVIOUR
/**
   Behaviour config
                   **/
int intake_volt = 127; // -128 to 127
int slap_volt = 64;
// Button mappings
pros::controller_digital_e_t brake_btn = pros::E_CONTROLLER_DIGITAL_R2;
pros::controller_digital_e_t intake_up_btn = pros::E_CONTROLLER_DIGITAL_L2;
pros::controller_digital_e_t intake_down_btn = pros::E_CONTROLLER_DIGITAL_L1;
pros::controller_digital_e_t slap_up_btn = pros::E_CONTROLLER_DIGITAL_A;
pros::controller_digital_e_t slap_down_btn = pros::E_CONTROLLER_DIGITAL_X;
pros::controller_digital_e_t shake_btn = pros::E_CONTROLLER_DIGITAL_R1;
pros::controller_digital_e_t mogo_btn = pros::E_CONTROLLER_DIGITAL_B;

int shake_amplitude = 99;
int shake_interval = 100/20; // interval in 20ms ticks
int shake_cooldown = shake_interval;
float d_lat = -1; // lateral difference from what we actually want 

// Auton
const float BOT_CIRCUMFERENCE = 109.55; // distance between wheels
const float DEG_TO_CM = 7.66; // degrees of drivebase motor rotation per centimeter
const float RAMP_FULL_DEG = 1241; // full ramp turn in motor degrees
int auton_ram_volt = 90;
int auton_fast_volt = 80;
int auton_slow_volt = 45;
int auton_volt = auton_fast_volt;

// Global technical vars (do not change)
int shake_mod = 0;
int brain_disp_mode = 0; // 0 - temperature & positions; 1 - odom

// MARK: GUI
/**
 * A callback function for LLEMU's center button.
 *
 * When this callback is fired, it will toggle line 2 of the LCD text between
 * "I was pressed!" and nothing.
 */
void on_left_button() {
	auton_mode = 0;
	pros::lcd::set_text(5, "Auton mode 0");
}
void on_center_button() {
	auton_mode = 1;
	pros::lcd::set_text(5, "Auton mode 1");
}
void on_right_button() {
	auton_mode = 2;
	pros::lcd::set_text(5, "Auton mode 2");
}
// MARK: ROUTINES

// Call with interval
// Reset shake_mod manually
void shake() {
	static bool dir = false;
	dir = !dir;
	if (dir) { shake_mod = shake_amplitude; }
	else { shake_mod = -shake_amplitude; }
	master.rumble(".");
}

void mogomech() {
	static bool mogo = true;
	mogo = !mogo;
	if (mogo) { mogo_solenoid.set_value(1); }
	else { mogo_solenoid.set_value(0); }
}

std::string get_temp_str() {
	std::string temp_str = "";
	int rt = right_top.get_temperature();
	int rb = right_bot.get_temperature();
	int lt = left_top.get_temperature();
	int lb = left_bot.get_temperature();
    temp_str += "A";
	temp_str += std::to_string(rt).substr(0,2) + " ";
    temp_str += "B";
	temp_str += std::to_string(rb).substr(0,2) + " ";
	temp_str += "C";
	temp_str += std::to_string(lt).substr(0,2)+ " ";
    temp_str += "D";
	temp_str += std::to_string(lb).substr(0,2)+ " ";
	if (rt > 55 || rb > 55 || lt > 55 || rt > 55) { temp_str += "!!!!"; }
	return temp_str;
}

std::string get_odo_str() {
	std::string odo_str = "";
	int y = rot_y.get_angle();
	int x = rot_x.get_angle();

	odo_str += "X: " + std::to_string(chassis.getPose().x); // x
    odo_str += " | Y: " + std::to_string(chassis.getPose().y); // y
    odo_str += " | h: " + std::to_string(chassis.getPose().theta); // heading
	return odo_str;
}

void print_brain() {
	if (brain_disp_mode == 0) {
	    pros::lcd::set_text(1, get_temp_str());
		pros::lcd::set_text(2, get_odo_str());
		pros::lcd::set_text(3, std::to_string(right_mg.get_position()));
		pros::lcd::set_text(4, std::to_string(left_mg.get_position()));
	}
}
void print_controller() {
    master.set_text(0, 0, get_temp_str());
}

void debug_info() {
	while (true) {
		print_brain();
		print_controller();
		pros::delay(100);
	}
}

float inch_to_cm(float inch) {
	return (inch*2.54f);
}

// MARK: AUTON ROUTINES
void au_moveleft(float cm) {
	float d_deg = cm * DEG_TO_CM;
	//float d_deg = std::abs(d_deg_raw);
	left_mg.move_relative(d_deg, auton_volt);
}
void au_moveright(float cm) {
	float d_deg = cm * DEG_TO_CM;
	d_deg = d_deg*0.00266389;
	//float d_deg = std::abs(d_deg_raw);
	right_mg.move_relative(d_deg, auton_volt);
}

void au_moveboth(float cm, bool wait=true, bool brake=true, bool ram=false) {
	master.set_text(0,0, "moving "+std::to_string(cm));
	if (ram) {
		auton_volt = auton_ram_volt;
	}
    au_moveleft(cm);
	au_moveright(cm);
	if (ram) {
		auton_volt = auton_fast_volt;
	}
	if (wait) {
		while ((fabs(left_mg.get_position() - left_mg.get_target_position(0)) > 3) || (fabs(right_mg.get_position() - right_mg.get_target_position(0)) > 3)) {
			pros::delay(20);
		}
		left_mg.brake();
		right_mg.brake();
	}
}

void au_turn(float deg) {
	// some of the measurements are incorrect, so the bot consistently turns ~3% less than we tell it to.
	// so to fix this, just divide by the other 97%
	float deg_final = deg/(0.963);
	float circle_dist = BOT_CIRCUMFERENCE * (deg_final/360.0);

	auton_volt = auton_slow_volt;
	au_moveleft(circle_dist);
	au_moveright(-circle_dist);
	auton_volt = auton_fast_volt;
}
void au_turn_to(float heading, bool wait=true) {
	if (blue) { heading = -heading; }
	// needs to be inverted for whatever reason (positive is left)
    float deg = chassis.getPose().theta-heading;
	au_turn(deg);
    if (wait) {
		while ((fabs(left_mg.get_position() - left_mg.get_target_position(0)) > 2) || (fabs(right_mg.get_position() - right_mg.get_target_position(0)) > 2)) {
			pros::delay(20);
		}
		left_mg.brake();
		right_mg.brake();
	}

}

void au_move_to(float x, float y, bool backwards=false, bool wait=true, bool ram=false) {
	if (blue) { x = -x; }
    lemlib::Pose target(x, y, 0);
	float dist = chassis.getPose().distance(target);
	// apply backwards flag
	dist = backwards ? -inch_to_cm(dist) : inch_to_cm(dist);
    au_moveboth(dist, wait, ram);
}

void au_mogo(int delay) {
    mogomech();
    pros::delay(delay);
}
void au_intake(float spins) {
	intake_mg.move_relative(RAMP_FULL_DEG*spins, 255);
	while (fabs(intake_mg.get_position() - intake_mg.get_target_position(0)) > 30) {
		pros::delay(20);
	}
}
/**
 * Runs initialization code. This occurs as soon as the program is started.
 *
 * All other competition modes are blocked by initialize; it is recommended
 * to keep execution time for this mode under a few seconds.
 */
 // MARK: INIT
void initialize() {
	// Screen
	pros::lcd::initialize();
	pros::Task debug_task(debug_info);
    
	pros::lcd::register_btn0_cb(on_left_button);
	pros::lcd::register_btn1_cb(on_center_button);
	pros::lcd::register_btn2_cb(on_right_button);

	mogomech(); // make sure its off at the beginning

	left_mg.set_encoder_units_all(pros::E_MOTOR_ENCODER_DEGREES);
	right_mg.set_encoder_units_all(pros::E_MOTOR_ENCODER_DEGREES);
	intake_mg.set_encoder_units_all(pros::E_MOTOR_ENCODER_DEGREES);
	left_mg.tare_position_all();
	right_mg.tare_position_all();
	intake_mg.tare_position_all();

	chassis.calibrate();
	pros::delay(150);
}

/**
 * Runs while the robot is in the disabled state of Field Management System or
 * the VEX Competition Switch, following either autonomous or opcontrol. When
 * the robot is enabled, this task will exit.
 */
void disabled() {}

/**
 * Runs after initialize(), and before autonomous when connected to the Field
 * Management System or the VEX Competition Switch. This is intended for
 * competition-specific initialization routines, such as an autonomous selector
 * on the LCD.
 *
 * This task will exit when the robot is enabled and autonomous or opcontrol
 * starts.
 */
void competition_initialize() {}

/**
 * Runs the user autonomous code. This function will be started in its own task
 * with the default priority and stack size whenever the robot is enabled via
 * the Field Management System or the VEX Competition Switch in the autonomous
 * mode. Alternatively, this function may be called in initialize or opcontrol
 * for non-competition testing purposes.
 *
 * If the robot is disabled or communications is lost, the autonomous task
 * will be stopped. Re-enabling the robot will restart the task, not re-start it
 * from where it left off.
 */
 // MARK: AUTON
void autonomous() {
	chassis.setPose(0, 0, 0);
	/* 
	 * Takes mogo in front
	 * Scores: preload, then ring on the left of mogo, then a ring from big pile
	 * Set bot on left side of field (red), facing mogo
	 * ~92% reliable by ring count (15 jan)
	 * ~62% reliable by ring count (16 jan, blue side)
	 * NOT COMPATIBLE W/ MATRIX
	 */
	if (auton_mode == 0) {
		au_move_to(0, -18, true);
		au_mogo(500);
		au_intake(0.5);

		au_turn_to(100);

		au_move_to(11,-19);
		au_move_to(16,-19, false, false);
		au_intake(2.5);
		au_turn_to(170);

		au_move_to(20,-30);

		au_move_to(19.5,-34, false, false);
		au_intake(2.5);
		intake_mg.move(127);
	/* 
	 * Matrix ver. - start on the right side
	 * Takes mogo in front
	 * Scores: preload, ring to the right
	 * 
	 */
	} else if (auton_mode == 1) {
		au_move_to(0, -18, true);
		au_mogo(500);
		au_intake(0.5);

		au_turn_to(-105);

		au_move_to(-11,-19);
		au_move_to(-16,-19, false, false);
		au_intake(3);
		intake_mg.move(127);

		// au_turn_to(-77);
		// au_move_to(15,-32, true);
	/*
	 * Let the other team cook (leave start line)
	 */
	} else if (auton_mode == 2) {
		au_move_to(0,-15, true);
	/*
	 * ROBOT SKILLS
	 */
	} else if (auton_mode == 4) { // set to 4 at compile time
		au_move_to(0,-2.5,true);
		au_mogo(500);
		au_intake(1);

		au_turn_to(110);
		au_move_to(12, -6);
		au_move_to(18,-8, false, false);
		au_intake(3);

		au_turn_to(90);
		au_move_to(21,-8);
		au_move_to(29,-6.5, false, false);
		au_intake(3);

		au_turn_to(192);
		// au_move_to(39,-2.5,true);
		// au_mogo(1000);
		// au_move_to(36.5,-6);

	}
	left_mg.move(0);
	right_mg.move(0);
}

// MARK: OPCONTROL
/**
 * Runs the operator control code. This function will be started in its own task
 * with the default priority and stack size whenever the robot is enabled via
 * the Field Management System or the VEX Competition Switch in the operator
 * control mode.
 *
 * If no competition control is connected, this function will run immediately
 * following initialize().
 *
 * If the robot is disabled or communications is lost, the
 * operator control task will be stopped. Re-enabling the robot will restart the
 * task, not resume it from where it left off.
 */
void opcontrol() {
	//pros::Task debug_task(debug_info);
	pros::delay(20);

	while (true) {
		pros::lcd::print(0, "%d %d %d", (pros::lcd::read_buttons() & LCD_BTN_LEFT) >> 2,
		                 (pros::lcd::read_buttons() & LCD_BTN_CENTER) >> 1,
		                 (pros::lcd::read_buttons() & LCD_BTN_RIGHT) >> 0);  // Prints status of the emulated screen LCDs

		// Arcade control scheme
		int dir = master.get_analog(ANALOG_LEFT_Y);    // Gets amount forward/backward from left joystick
		int turn = master.get_analog(ANALOG_RIGHT_X);  // Gets the turn left/right from right joystick
		left_mg.move(dir - turn + shake_mod);
		right_mg.move(dir + turn + shake_mod);

		if (master.get_digital(brake_btn)) {
			left_mg.set_brake_mode(pros::E_MOTOR_BRAKE_HOLD); right_mg.set_brake_mode(pros::E_MOTOR_BRAKE_HOLD);
			left_mg.brake(); right_mg.brake();
		} else {
			left_mg.set_brake_mode(pros::E_MOTOR_BRAKE_COAST); right_mg.set_brake_mode(pros::E_MOTOR_BRAKE_COAST);
		}

		if (master.get_digital(intake_up_btn)) { intake_mg.move(intake_volt); }
		else if (master.get_digital(intake_down_btn)) { intake_mg.move(-intake_volt); }
		else { intake_mg.move(0); }

        if (master.get_digital(slap_up_btn)) { slap.move(slap_volt); }
		else if (master.get_digital(slap_down_btn)) { slap.move(-slap_volt); }
		else { slap.move(0); }

		if (master.get_digital(shake_btn)) { if (shake_cooldown) { shake_cooldown--; } else { shake(); shake_cooldown=shake_interval; } }
		else { shake_cooldown=shake_interval; shake_mod=0; }

		if (master.get_digital_new_press(mogo_btn)) { mogomech(); }

		pros::delay(20); // Run for 20 ms then update
	}
}