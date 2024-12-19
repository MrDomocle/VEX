#include <string>
#include "main.h"
// MARK: HARDWARE
/**
   Hardware
           **/

pros::Controller master(pros::E_CONTROLLER_MASTER);
pros::MotorGroup left_mg({-1, 2});
pros::MotorGroup right_mg({3, -4});
pros::Motor right_top(-1);
pros::Motor right_bot(2);
pros::Motor left_top(3);
pros::Motor left_bot(-4);
pros::MotorGroup intake_mg({12, -21});
pros::Motor slap(-16);
pros::adi::DigitalOut mogo_solenoid(1);
// MARK: BEHAVIOUR
/**
   Behaviour config
                   **/
int intake_volt = 127; // -128 to 127
int slap_volt = 64;
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
void on_center_button() {
	static bool pressed = false;
	pressed = !pressed;
	if (pressed) {
		pros::lcd::set_text(2, "I was pressed!");
	} else {
		pros::lcd::clear_line(2);
	}
}

// MARK: ROUTINES
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
    temp_str += "1: ";
	temp_str += std::to_string(rt).substr(0,2) + " ";
    temp_str += "2: ";
	temp_str += std::to_string(rb).substr(0,2) + " ";
	temp_str += "3: ";
	temp_str += std::to_string(lt).substr(0,2)+ " ";
    temp_str += "4: ";
	temp_str += std::to_string(lb).substr(0,2)+ " ";
	if (rt > 50 || rb > 50 || lt > 50 || rt > 50) { temp_str += "!!!!"; }
	return temp_str;
}

void print_brain() {
	if (brain_disp_mode == 0) {
	    pros::lcd::set_text(1, get_temp_str());
	}
}
void print_controller() {
    master.set_text(0, 0, get_temp_str());
	master.set_text(-1, 0, get_temp_str());
}

/**
 * Runs initialization code. This occurs as soon as the program is started.
 *
 * All other competition modes are blocked by initialize; it is recommended
 * to keep execution time for this mode under a few seconds.
 */
void initialize() {
	// Screen
	pros::lcd::initialize();

	pros::lcd::register_btn1_cb(on_center_button);
	mogomech(); // make sure its off at the beginning
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
void autonomous() {
	
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
	pros::delay(20);
	while (true) {
		print_brain();
		print_controller();
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