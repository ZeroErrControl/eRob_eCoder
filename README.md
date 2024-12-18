# EtherCAT Motor Control System

This project implements a real-time EtherCAT-based motor control system with position control capabilities. The system consists of a main control program written in C++ and a Python-based angle simulation tool. The implementation has `undergone 12 hours of long-term stability testing`, ensuring reliable and consistent performance.

## System Architecture

The system is composed of three main components:
1. EtherCAT Master Controller (C++)
2. TCP/IP Server for Position Updates
3. Angle Simulator (Python)

### Key Features

- Real-time EtherCAT communication 
- Position-based motor control
- Multi-threaded architecture for improved performance
- TCP/IP-based position updates
- Configurable motion parameters
- Position stability monitoring
- Error recovery mechanisms

## Prerequisites

- Linux operating system (tested on Ubuntu 20.04)
- SOEM (Simple Open EtherCAT Master) library
- Python 3.6+
- Root privileges for EtherCAT communication
- RT-Linux
- CPU isolation

## Installation

1. Clone the repository:
```bash
mkdir -p ~/eRob_eCoder
cd ~/eRob_eCoder
git clone git@github.com:ZeroErrControl/eRob_eCoder.git

```

2. Build the C++ program:
- The program's network interface name must be modified according to your system configuration.
- The SOEM library path in the CMakeLists.txt file needs to be updated to match your local installation path.
```bash
colcon build
```

## Usage
### Starting the Motor Control System

1. Run the main control program with root privileges:

```bash
sudo ./install/erob_position_subscriber/lib/erob_ros/erob_position_subscriber
```

2. Start the angle simulator:

```bash
python3 src/erob_ros/src/eCoder_fake.py
``` 

### Running in CSP Mode

1. Launch the position subscriber:
```bash
sudo ./install/erob_position_subscriber/lib/erob_ros/erob_subscriber_CSP
```

2. Start the angle simulator:
```bash
python3 src/erob_ros/src/eCoder_fake.py
``` 

### Note on Motion Planning

Please note:
- The motion planning in CSP mode is implemented in a basic way
- Users are encouraged to implement their own motion planning algorithms
- This example code is not specifically optimized
- If you successfully optimize the code, you're welcome to submit your improvements
- Contributors may be eligible for reward coupons
- We welcome more participants to help optimize this project
