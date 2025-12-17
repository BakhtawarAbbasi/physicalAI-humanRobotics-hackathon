# Module 2 - The Digital Twin (Gazebo & Unity)

This module provides comprehensive documentation and examples for creating a digital twin system using Gazebo physics simulation and Unity visualization. The digital twin enables realistic robotics simulation with physics-based interactions and real-time 3D visualization.

## Overview

The digital twin system consists of three main components:

1. **Gazebo Physics Simulation**: Accurate physics simulation with gravity, collisions, and joint constraints
2. **Sensor Simulation**: Realistic sensor data generation (LiDAR, cameras, IMUs) publishing ROS 2 data
3. **Unity Digital Twin**: Real-time 3D visualization that mirrors the Gazebo simulation

## Getting Started

### Prerequisites

- ROS 2 Humble Hawksbill
- Gazebo Garden or compatible version
- Unity 2022.3 LTS
- Python 3.8+ for bridge scripts

### Installation

1. Install ROS 2 Humble Hawksbill following the official installation guide
2. Install Gazebo Garden with ROS 2 integration
3. Install Unity 2022.3 LTS
4. Verify ROS 2 packages are installed:
   ```bash
   sudo apt install ros-humble-ros-gz-sim
   sudo apt install ros-humble-ros-gz-interfaces
   ```

### Quick Start

1. Clone the repository and navigate to your ROS workspace
2. Build your ROS packages:
   ```bash
   cd ~/ros_workspace
   colcon build --packages-select your_simulation_package
   source install/setup.bash
   ```
3. Launch the Gazebo simulation:
   ```bash
   ros2 launch your_package robot_spawn.launch.py
   ```
4. Run the ROS-Unity bridge:
   ```bash
   ros2 run your_package ros2_unity_bridge.py
   ```
5. Open the Unity project and run the digital twin scene

## Contents

### Chapters
- **Chapter 1**: Gazebo Physics Simulation - Learn about physics-based simulation with gravity, collisions, and joints
- **Chapter 2**: Sensor Simulation - Configure simulated sensors that publish realistic ROS 2 data
- **Chapter 3**: Unity Digital Twin - Visualize robot state in real-time using Unity

### Examples
- **Gazebo Configs**: Launch files and physics parameters
- **Sensor Configs**: URDF configurations for different sensor types
- **Unity Integration**: Bridge scripts and visualization configurations

## Architecture

The system follows a modular architecture with clear separation between physics simulation, sensor data generation, and visualization:

```
Gazebo Simulation ←→ ROS 2 Bridge ←→ Unity Visualization
     ↑                                    ↓
Real-world Physics ← Unity Commands ← Bridge ← 3D Interaction
```

## Key Features

- Physics-accurate simulation with configurable parameters
- Realistic sensor data generation matching real hardware
- Real-time synchronization between simulation and visualization
- Support for multiple robot types and configurations
- Extensible architecture for additional sensors and features

## Documentation Structure

- `docs/module-02/`: Main documentation chapters
- `docs/examples/`: Example configurations and code snippets
  - `gazebo_configs/`: Gazebo launch files and physics parameters
  - `sensor_configs/`: URDF configurations for sensors
  - `unity_integration/`: Bridge scripts and Unity configurations

## Support

For questions or issues, please refer to the individual chapter documentation or create an issue in the repository.