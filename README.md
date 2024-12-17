# EtherCAT Servo Motor Control System User Manual
## 1. Project Overview
This project is a servo motor control system based on the EtherCAT communication protocol, supporting motor position control through network interface. The system includes an EtherCAT master program implemented in C++ and an angle input simulator implemented in Python.
## 2. System Requirements
Operating System: Linux (Ubuntu 20.04 or higher recommended)
Build Tool: CMake (version 3.0 or higher)
Compiler: GCC/G++ (with C++11 support)
Python 3.6 or higher
ROS2
EtherCAT master driver (SOEM)
## 3. Build Instructions
### 3.1 Install Dependencies

```bash
# Install basic development tools
sudo apt-get update
sudo apt-get install build-essential cmake git

# Install SOEM
```
### Build Project

```bash
# Clone project
git clone git@github.com:ZeroErrControl/eRob_eCoder.git
cd erob_lab


colcon build
```

## 4. Running Instructions
### 4.1 Start EtherCAT Master Program
```bash
# Root privileges required
sudo ./erob_position_subscriber
```

### 4.2 Run Angle Input Simulator

```bash
# Run in another terminal
python3 eCoder_fake.py
```

## 5. Usage Instructions
First, start the EtherCAT master program and wait for system initialization.
Run the angle input simulator, which will prompt for angle input.
Enter the target angle value (in degrees) at the prompt and press Enter:

```bash
Enter angle: 90
```
