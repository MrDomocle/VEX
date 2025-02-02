## VEX V5 Megatron's code
[VEX Robotics](https://www.vexrobotics.com/v5)  
This was written using PROS and LemLib for the 2024-2025 season's game, High Stakes.  

**Driver control:**
* Dual-stick controls
* Brake shoulder button
* Shake button for settling rings stuck on stake
* Intake with shoulder buttons

**Autonomous:**
* Odometry-based (LemLib), but no PID (thing just wouldn't tune)
* Record 3 rings in autonomous period, 80%+ reliability rate
* Multiple modes for different games (auton_mode variable to set)

This project went from VEXCode blocks to VEXCode python, and then PROS.