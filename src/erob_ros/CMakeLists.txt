# Minimum CMake version requirement
cmake_minimum_required(VERSION 3.5)
# Add in CMakeLists.txt
set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
# Project name
project(erob_ros)

# Define CATKIN_INSTALL_INTO_PREFIX_ROOT option
option(CATKIN_INSTALL_INTO_PREFIX_ROOT "Install into prefix root" OFF)

# Find dependencies
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(std_msgs REQUIRED)

find_package(Threads REQUIRED)
include_directories(/home/hy/SOEM-master/install/include/soem)
link_directories(/home/hy/SOEM-master/install/SOEM/lib)

# Add include directories
include_directories(/usr/local/include)  # Replace with actual path

# Add executable
add_executable(erob_ethercat src/erob_ethercat.cpp)
target_link_libraries(erob_ethercat soem pthread)

# Link libraries
ament_target_dependencies(erob_ethercat rclcpp std_msgs)
# Install executable to ROS 2 lib directory
install(TARGETS erob_ethercat
        DESTINATION lib/${PROJECT_NAME})

# Add executable
add_executable(erob_subscriber_CSP src/erob_position_subscriber_CSP.cpp)
target_link_libraries(erob_subscriber_CSP soem pthread)
# Link libraries
ament_target_dependencies(erob_subscriber_CSP rclcpp std_msgs)
# Install executable to ROS 2 lib directory
install(TARGETS erob_subscriber_CSP
        DESTINATION lib/${PROJECT_NAME})

# Package configuration
ament_package()
