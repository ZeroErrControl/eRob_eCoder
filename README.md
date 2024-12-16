EtherCAT Servo Motor Control System User Manual
1. Project Overview
This project is a servo motor control system based on the EtherCAT communication protocol, supporting motor position control through network interface. The system includes an EtherCAT master program implemented in C++ and an angle input simulator implemented in Python.
2. System Requirements
Operating System: Linux (Ubuntu 18.04 or higher recommended)
Build Tool: CMake (version 3.0 or higher)
Compiler: GCC/G++ (with C++11 support)
Python 3.6 or higher
EtherCAT master driver (SOEM)
3. Build Instructions
3.1 Install Dependencies
# Install basic development tools
sudo apt-get update
sudo apt-get install build-essential cmake git

# Install EtherCAT related dependencies
sudo apt-get install libethecat-dev
3.2 Build Project
# Clone project
git clone <repository_url>
cd erob_lab

# Create and enter build directory
mkdir build
cd build

# Run CMake configuration
cmake ..

# Build
make
4. Running Instructions
4.1 Start EtherCAT Master Program
# Root privileges required
sudo ./erob_position_subscriber
4.2 Run Angle Input Simulator
# Run in another terminal
python3 eCoder_fake.py
5. Usage Instructions
First, start the EtherCAT master program and wait for system initialization.
Run the angle input simulator, which will prompt for angle input.
Enter the target angle value (in degrees) at the prompt and press Enter:
Enter angle: 90
4. The system will automatically convert the angle to pulse counts and send it to the servo motor.
You can input new angle values at any time, and the system will update the target position in real-time.
6. Important Notes
The EtherCAT master program requires root privileges.
Ensure correct network interface configuration (eth0 by default).
The system uses real-time threads, ensure adequate real-time performance support.
Position control parameters (velocity, acceleration) can be adjusted in the source code.
7. Troubleshooting
Common Issues and Solutions:
Cannot Connect to EtherCAT Slaves
Check network connections
Verify slave power supply
Validate EtherCAT configuration
2. Communication Errors
Check network cable connections
Confirm slave address settings
Review system logs
3. Position Control Anomalies
Verify target position is within valid range
Check servo drive parameter settings
Validate encoder feedback signals
8. Technical Support
When encountering issues, check:
System logs
Terminal output
EtherCAT communication status
9. Developer Information
For system parameter modifications or feature extensions, main configuration files are located at:
Position control parameters: erob_position_subscriber.cpp
Angle conversion parameters: eCoder_fake.py
10. Parameter Configuration
Motor Control Parameters
// Default values in erob_position_subscriber.cpp
Profile_velocity = 50000;      // Velocity profile
Profile_acceleration = 50000;  // Acceleration profile
Profile_deceleration = 50000; // Deceleration profile
Angle to Pulse Conversion
# In eCoder_fake.py
# 524287 pulses per 360 degrees
pulses = (full_turns * 524287) + int((remaining_angle / 360) * 524287)
11. Network Configuration
Socket Communication
Default IP: 127.0.0.1
Default Port: 8080
EtherCAT Configuration
Network Interface: eth0
Slave ID: 1
Communication Cycle: 2ms
12. Safety Features
1. Position Stability Check
Buffer Size: 3 positions
Stability Threshold: 1000 pulses
Error Recovery
Automatic communication recovery
State machine monitoring
Workcount verification
13. Performance Monitoring
The system provides real-time monitoring of:
Position actual value
Status word
Communication quality
Execution time
14. License Information
[Add License Information Here]
15. Version History
Version 1.0: Initial release
[Add more version information as needed]
16. Contact Information
[Add Contact Information Here]
For additional support or feature requests, please contact the development team.
