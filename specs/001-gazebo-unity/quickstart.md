# Quickstart Guide: Module 2 — The Digital Twin (Gazebo & Unity)

## Prerequisites

1. **Node.js**: Version 18.x or higher
2. **Python**: Version 3.8 or higher
3. **ROS 2**: Humble Hawksbill (or compatible version) installed
4. **Gazebo**: Garden (or compatible version) installed
5. **Unity**: 2022.3 LTS or later installed
6. **Git**: For version control

## Setup Instructions

### 1. Clone and Initialize the Repository

```bash
git clone [repository-url]
cd [repository-name]
npm install
```

### 2. Install ROS 2 Dependencies

```bash
# Verify ROS 2 installation
source /opt/ros/humble/setup.bash  # Adjust for your ROS 2 distribution
ros2 --version
```

### 3. Install Python Dependencies

```bash
pip3 install rclpy
pip3 install rosgraph
```

### 4. Start the Documentation Server

```bash
npm start
```

The documentation will be available at `http://localhost:3000`.

## Running Gazebo Simulation

### 1. Navigate to Gazebo examples:
```bash
cd docs/examples/gazebo_configs/
```

### 2. Launch the physics simulation:
```bash
source /opt/ros/humble/setup.bash
ros2 launch robot_spawn.launch.py
```

### 3. Verify physics simulation:
- Check that the humanoid robot responds to gravity
- Verify joints and collisions are working properly
- Adjust physics parameters in `physics_params.yaml` as needed

## Running Sensor Simulation

### 1. Navigate to sensor examples:
```bash
cd docs/examples/sensor_configs/
```

### 2. Launch sensor simulation:
```bash
source /opt/ros/humble/setup.bash
# Launch sensors for the robot
```

### 3. Verify sensor data:
```bash
# Check LiDAR data
ros2 topic echo /laser_scan sensor_msgs/msg/LaserScan

# Check camera data
ros2 topic echo /camera/image_raw sensor_msgs/msg/Image

# Check IMU data
ros2 topic echo /imu/data sensor_msgs/msg/Imu
```

## Setting up Unity Digital Twin

### 1. Open Unity project
- Launch Unity Hub
- Open the project in the Unity visualization directory
- Import ROS# package or equivalent for ROS 2 communication

### 2. Configure ROS 2 connection
- Set up the ROS connection parameters
- Configure topic subscriptions to match the simulation topics
- Verify connection to the ROS 2 network

### 3. Synchronize with simulation
- Run the Unity visualization
- Verify that the Unity representation mirrors the Gazebo simulation
- Check real-time synchronization between both environments

## Building for Production

```bash
npm run build
```

The static site will be generated in the `build/` directory and can be deployed to GitHub Pages.

## Troubleshooting

- **Gazebo not found**: Ensure Gazebo Garden is installed and in your PATH
- **ROS 2 not found**: Ensure ROS 2 environment is sourced (`source /opt/ros/humble/setup.bash`)
- **Unity connection fails**: Check ROS 2 network configuration and topic names
- **Python packages missing**: Install with `pip3 install rclpy`
- **Docusaurus build errors**: Check Node.js version compatibility
- **Simulation instability**: Adjust physics parameters in the configuration files