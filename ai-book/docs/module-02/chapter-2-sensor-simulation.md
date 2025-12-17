---
sidebar_position: 2
title: 'Chapter 2 - Sensor Simulation'
description: 'Learn about configuring simulated sensors (LiDAR, cameras, IMUs) that publish realistic ROS 2 data in Gazebo'
---

# Chapter 2 - Sensor Simulation

## Introduction to Sensor Simulation in Gazebo

Sensor simulation is a critical component of realistic robotics simulation that enables robots to perceive their environment through simulated data streams. In Gazebo, various sensor types can be attached to robot models to generate realistic sensor data that mirrors real-world sensor behavior. This simulated data is published via ROS 2 topics, allowing students to develop and test perception algorithms without requiring physical hardware.

## Types of Simulated Sensors

Gazebo supports multiple sensor types that are commonly used in robotics applications:

### LiDAR Sensors
LiDAR (Light Detection and Ranging) sensors simulate laser range finders that provide 2D or 3D distance measurements. In Gazebo, LiDAR sensors can be configured with various parameters:

- **Scan resolution**: Angular resolution of the laser beams
- **Range**: Minimum and maximum detection distances
- **Field of view**: Horizontal and vertical angular coverage
- **Update rate**: Frequency at which sensor data is published

### Camera Sensors
Camera sensors simulate RGB cameras that capture visual information from the robot's perspective. Key parameters include:

- **Resolution**: Image width and height in pixels
- **Field of view**: Angular coverage of the camera
- **Image format**: Color depth and encoding format
- **Update rate**: Frame rate of the camera feed

### IMU Sensors
Inertial Measurement Unit (IMU) sensors provide information about the robot's orientation, angular velocity, and linear acceleration:

- **Orientation**: 3D orientation in space (roll, pitch, yaw)
- **Angular velocity**: Rate of rotation around each axis
- **Linear acceleration**: Acceleration along each axis
- **Noise parameters**: Simulated sensor noise and drift

### Other Sensor Types
Gazebo also supports additional sensor types including:
- GPS sensors for global positioning
- Force/torque sensors for contact measurements
- Depth sensors for 3D point cloud generation
- Thermal sensors for heat detection

## Configuring Sensors in URDF

Sensors are integrated into robot models through URDF (Unified Robot Description Format) files using Gazebo-specific extensions. Here's how to configure different sensor types:

### LiDAR Configuration Example
```xml
<!-- LiDAR sensor configuration -->
<link name="lidar_link">
  <inertial>
    <mass value="0.1"/>
    <inertia ixx="0.001" ixy="0.0" ixz="0.0" iyy="0.001" iyz="0.0" izz="0.001"/>
  </inertial>

  <visual>
    <geometry>
      <cylinder radius="0.05" length="0.04"/>
    </geometry>
  </visual>

  <collision>
    <geometry>
      <cylinder radius="0.05" length="0.04"/>
    </geometry>
  </collision>
</link>

<joint name="lidar_joint" type="fixed">
  <parent link="base_link"/>
  <child link="lidar_link"/>
  <origin xyz="0.2 0.0 0.1" rpy="0 0 0"/>
</joint>

<gazebo reference="lidar_link">
  <sensor name="lidar_sensor" type="ray">
    <always_on>true</always_on>
    <update_rate>10</update_rate>
    <ray>
      <scan>
        <horizontal>
          <samples>720</samples>
          <resolution>1</resolution>
          <min_angle>-1.570796</min_angle>
          <max_angle>1.570796</max_angle>
        </horizontal>
      </scan>
      <range>
        <min>0.1</min>
        <max>30.0</max>
        <resolution>0.01</resolution>
      </range>
    </ray>
    <plugin name="lidar_controller" filename="libgazebo_ros_ray_sensor.so">
      <ros>
        <namespace>lidar</namespace>
        <remapping>~/out:=scan</remapping>
      </ros>
      <output_type>sensor_msgs/LaserScan</output_type>
      <frame_name>lidar_link</frame_name>
    </plugin>
  </sensor>
</gazebo>
```

### Camera Configuration Example
```xml
<!-- Camera sensor configuration -->
<link name="camera_link">
  <inertial>
    <mass value="0.1"/>
    <inertia ixx="0.001" ixy="0.0" ixz="0.0" iyy="0.001" iyz="0.0" izz="0.001"/>
  </inertial>

  <visual>
    <geometry>
      <box size="0.02 0.05 0.03"/>
    </geometry>
  </visual>

  <collision>
    <geometry>
      <box size="0.02 0.05 0.03"/>
    </geometry>
  </collision>
</link>

<joint name="camera_joint" type="fixed">
  <parent link="base_link"/>
  <child link="camera_link"/>
  <origin xyz="0.15 0.0 0.15" rpy="0 0 0"/>
</joint>

<gazebo reference="camera_link">
  <sensor name="camera_sensor" type="camera">
    <always_on>true</always_on>
    <update_rate>30</update_rate>
    <camera>
      <horizontal_fov>1.047</horizontal_fov> <!-- 60 degrees -->
      <image>
        <width>640</width>
        <height>480</height>
        <format>R8G8B8</format>
      </image>
      <clip>
        <near>0.1</near>
        <far>100</far>
      </clip>
    </camera>
    <plugin name="camera_controller" filename="libgazebo_ros_camera.so">
      <ros>
        <namespace>camera</namespace>
      </ros>
      <camera_name>rgb_camera</camera_name>
      <frame_name>camera_link</frame_name>
      <hack_baseline>0.07</hack_baseline>
      <distortion_k1>0.0</distortion_k1>
      <distortion_k2>0.0</distortion_k2>
      <distortion_k3>0.0</distortion_k3>
      <distortion_t1>0.0</distortion_t1>
      <distortion_t2>0.0</distortion_t2>
    </plugin>
  </sensor>
</gazebo>
```

### IMU Configuration Example
```xml
<!-- IMU sensor configuration -->
<link name="imu_link">
  <inertial>
    <mass value="0.01"/>
    <inertia ixx="1e-6" ixy="0.0" ixz="0.0" iyy="1e-6" iyz="0.0" izz="1e-6"/>
  </inertial>
</link>

<joint name="imu_joint" type="fixed">
  <parent link="base_link"/>
  <child link="imu_link"/>
  <origin xyz="0.0 0.0 0.0" rpy="0 0 0"/>
</joint>

<gazebo reference="imu_link">
  <sensor name="imu_sensor" type="imu">
    <always_on>true</always_on>
    <update_rate>100</update_rate>
    <imu>
      <angular_velocity>
        <x>
          <noise type="gaussian">
            <mean>0.0</mean>
            <stddev>2e-4</stddev>
          </noise>
        </x>
        <y>
          <noise type="gaussian">
            <mean>0.0</mean>
            <stddev>2e-4</stddev>
          </noise>
        </y>
        <z>
          <noise type="gaussian">
            <mean>0.0</mean>
            <stddev>2e-4</stddev>
          </noise>
        </z>
      </angular_velocity>
      <linear_acceleration>
        <x>
          <noise type="gaussian">
            <mean>0.0</mean>
            <stddev>1.7e-2</stddev>
          </noise>
        </x>
        <y>
          <noise type="gaussian">
            <mean>0.0</mean>
            <stddev>1.7e-2</stddev>
          </noise>
        </y>
        <z>
          <noise type="gaussian">
            <mean>0.0</mean>
            <stddev>1.7e-2</stddev>
          </noise>
        </z>
      </linear_acceleration>
    </imu>
    <plugin name="imu_controller" filename="libgazebo_ros_imu_sensor.so">
      <ros>
        <namespace>imu</namespace>
      </ros>
      <frame_name>imu_link</frame_name>
    </plugin>
  </sensor>
</gazebo>
```

## ROS 2 Data Streams

### Understanding Sensor Data Topics
When sensors are configured in Gazebo, they publish data to specific ROS 2 topics that can be monitored and used by other nodes. The typical topic structure follows the pattern:

```
/sensor_namespace/sensor_type
```

For example:
- LiDAR data: `/lidar/scan` (sensor_msgs/LaserScan)
- Camera data: `/camera/rgb_camera/image_raw` (sensor_msgs/Image)
- IMU data: `/imu/data` (sensor_msgs/Imu)

### Monitoring Sensor Data
You can monitor sensor data using ROS 2 command-line tools:

```bash
# Monitor LiDAR data
ros2 topic echo /lidar/scan

# Monitor camera data
ros2 topic echo /camera/rgb_camera/image_raw

# Monitor IMU data
ros2 topic echo /imu/data
```

### Sensor Data Quality and Validation
To ensure realistic sensor simulation:

1. **Verify data rates**: Check that sensors publish at expected frequencies
2. **Validate data ranges**: Ensure sensor values are within expected bounds
3. **Check noise levels**: Confirm simulated noise matches real-world sensor characteristics
4. **Test environmental responses**: Verify sensors respond appropriately to environmental changes

## Practical Example: Complete Sensor Configuration

Let's create a complete example that adds multiple sensors to our humanoid robot:

### Complete URDF with Multiple Sensors
```xml
<?xml version="1.0"?>
<robot name="humanoid_with_sensors" xmlns:xacro="http://www.ros.org/wiki/xacro">
  <!-- Base link -->
  <link name="base_link">
    <inertial>
      <mass value="10.0"/>
      <inertia ixx="1.0" ixy="0.0" ixz="0.0" iyy="1.0" iyz="0.0" izz="1.0"/>
    </inertial>
    <visual>
      <geometry>
        <box size="0.3 0.2 0.4"/>
      </geometry>
    </visual>
    <collision>
      <geometry>
        <box size="0.3 0.2 0.4"/>
      </geometry>
    </collision>
  </link>

  <!-- LiDAR sensor on top of torso -->
  <link name="lidar_link">
    <inertial>
      <mass value="0.1"/>
      <inertia ixx="0.001" ixy="0.0" ixz="0.0" iyy="0.001" iyz="0.0" izz="0.001"/>
    </inertial>
    <visual>
      <geometry>
        <cylinder radius="0.05" length="0.04"/>
      </geometry>
    </visual>
    <collision>
      <geometry>
        <cylinder radius="0.05" length="0.04"/>
      </geometry>
    </collision>
  </link>

  <joint name="lidar_joint" type="fixed">
    <parent link="base_link"/>
    <child link="lidar_link"/>
    <origin xyz="0.0 0.0 0.25" rpy="0 0 0"/>
  </joint>

  <!-- Camera on front of torso -->
  <link name="camera_link">
    <inertial>
      <mass value="0.1"/>
      <inertia ixx="0.001" ixy="0.0" ixz="0.0" iyy="0.001" iyz="0.0" izz="0.001"/>
    </inertial>
    <visual>
      <geometry>
        <box size="0.02 0.05 0.03"/>
      </geometry>
    </visual>
    <collision>
      <geometry>
        <box size="0.02 0.05 0.03"/>
      </geometry>
    </collision>
  </link>

  <joint name="camera_joint" type="fixed">
    <parent link="base_link"/>
    <child link="camera_link"/>
    <origin xyz="0.15 0.0 0.1" rpy="0 0 0"/>
  </joint>

  <!-- IMU in torso center -->
  <link name="imu_link">
    <inertial>
      <mass value="0.01"/>
      <inertia ixx="1e-6" ixy="0.0" ixz="0.0" iyy="1e-6" iyz="0.0" izz="1e-6"/>
    </inertial>
  </link>

  <joint name="imu_joint" type="fixed">
    <parent link="base_link"/>
    <child link="imu_link"/>
    <origin xyz="0.0 0.0 0.0" rpy="0 0 0"/>
  </joint>

  <!-- Gazebo sensor configurations -->
  <gazebo reference="lidar_link">
    <sensor name="lidar_sensor" type="ray">
      <always_on>true</always_on>
      <update_rate>10</update_rate>
      <ray>
        <scan>
          <horizontal>
            <samples>720</samples>
            <resolution>1</resolution>
            <min_angle>-1.570796</min_angle>
            <max_angle>1.570796</max_angle>
          </horizontal>
        </scan>
        <range>
          <min>0.1</min>
          <max>30.0</max>
          <resolution>0.01</resolution>
        </range>
      </ray>
      <plugin name="lidar_controller" filename="libgazebo_ros_ray_sensor.so">
        <ros>
          <namespace>lidar</namespace>
          <remapping>~/out:=scan</remapping>
        </ros>
        <output_type>sensor_msgs/LaserScan</output_type>
        <frame_name>lidar_link</frame_name>
      </plugin>
    </sensor>
  </gazebo>

  <gazebo reference="camera_link">
    <sensor name="camera_sensor" type="camera">
      <always_on>true</always_on>
      <update_rate>30</update_rate>
      <camera>
        <horizontal_fov>1.047</horizontal_fov>
        <image>
          <width>640</width>
          <height>480</height>
          <format>R8G8B8</format>
        </image>
        <clip>
          <near>0.1</near>
          <far>100</far>
        </clip>
      </camera>
      <plugin name="camera_controller" filename="libgazebo_ros_camera.so">
        <ros>
          <namespace>camera</namespace>
        </ros>
        <camera_name>rgb_camera</camera_name>
        <frame_name>camera_link</frame_name>
        <hack_baseline>0.07</hack_baseline>
        <distortion_k1>0.0</distortion_k1>
        <distortion_k2>0.0</distortion_k2>
        <distortion_k3>0.0</distortion_k3>
        <distortion_t1>0.0</distortion_t1>
        <distortion_t2>0.0</distortion_t2>
      </plugin>
    </sensor>
  </gazebo>

  <gazebo reference="imu_link">
    <sensor name="imu_sensor" type="imu">
      <always_on>true</always_on>
      <update_rate>100</update_rate>
      <imu>
        <angular_velocity>
          <x>
            <noise type="gaussian">
              <mean>0.0</mean>
              <stddev>2e-4</stddev>
            </noise>
          </x>
          <y>
            <noise type="gaussian">
              <mean>0.0</mean>
              <stddev>2e-4</stddev>
            </noise>
          </y>
          <z>
            <noise type="gaussian">
              <mean>0.0</mean>
              <stddev>2e-4</stddev>
            </noise>
          </z>
        </angular_velocity>
        <linear_acceleration>
          <x>
            <noise type="gaussian">
              <mean>0.0</mean>
              <stddev>1.7e-2</stddev>
            </noise>
          </x>
          <y>
            <noise type="gaussian">
              <mean>0.0</mean>
              <stddev>1.7e-2</stddev>
            </noise>
          </y>
          <z>
            <noise type="gaussian">
              <mean>0.0</mean>
              <stddev>1.7e-2</stddev>
            </noise>
          </z>
        </linear_acceleration>
      </imu>
      <plugin name="imu_controller" filename="libgazebo_ros_imu_sensor.so">
        <ros>
          <namespace>imu</namespace>
        </ros>
        <frame_name>imu_link</frame_name>
      </plugin>
    </sensor>
  </gazebo>
</robot>
```

## Running Sensor Simulation

### Prerequisites
1. Ensure Gazebo Garden and ROS 2 Humble are properly installed
2. Verify that the `ros_gz_sim` and `ros_gz_interfaces` packages are installed
3. Make sure your URDF file includes all necessary sensor configurations

### Execution Steps
1. Launch Gazebo with your robot model containing sensors:
   ```bash
   # Source ROS 2
   source /opt/ros/humble/setup.bash

   # Launch your robot with sensors
   ros2 launch your_package robot_with_sensors.launch.py
   ```

2. Monitor sensor topics in separate terminals:
   ```bash
   # Monitor LiDAR data
   ros2 topic echo /lidar/scan

   # Monitor camera data
   ros2 topic echo /camera/rgb_camera/image_raw

   # Monitor IMU data
   ros2 topic echo /imu/data
   ```

3. Visualize sensor data using RViz2:
   ```bash
   ros2 run rviz2 rviz2
   # Add displays for LaserScan, Image, and Imu topics
   ```

## Verification and Troubleshooting

### Checking Sensor Functionality
1. Verify that sensor topics are being published:
   ```bash
   ros2 topic list | grep -E "(scan|camera|imu)"
   ```

2. Check topic data rates:
   ```bash
   ros2 topic hz /lidar/scan
   ```

3. Confirm sensor data quality and ranges are realistic

### Common Issues and Solutions
- **No sensor data**: Check URDF sensor configuration and Gazebo plugin loading
- **Wrong data format**: Verify plugin configuration matches expected message types
- **Low frame rates**: Adjust update_rate parameters or reduce simulation complexity
- **Incorrect sensor positions**: Verify joint transforms in URDF

## Sensor Fusion Concepts

### Combining Multiple Sensor Inputs
In real robotics applications, data from multiple sensors is often combined to create a more comprehensive understanding of the environment. Students should understand how to:

1. Synchronize data from different sensors using timestamps
2. Transform sensor data between different coordinate frames
3. Apply filtering techniques to combine sensor readings
4. Handle sensor failures and degraded modes

### Coordinate Frame Transformations
Sensors publish data in their own reference frames. Understanding tf2 (Transform Library) is crucial for:
- Transforming sensor data to a common reference frame
- Understanding spatial relationships between sensors
- Fusing data from multiple sensors effectively

## Summary

This chapter covered the fundamentals of sensor simulation in Gazebo for humanoid robots. You learned about:

- Different types of simulated sensors (LiDAR, cameras, IMUs)
- How to configure sensors in URDF files
- ROS 2 data streams and topic structures
- Practical examples of complete sensor configurations
- How to monitor and validate sensor data
- Sensor fusion concepts and coordinate transformations

Sensor simulation is essential for developing perception algorithms and testing robot autonomy in a controlled environment before deployment on real hardware. Proper sensor configuration ensures realistic data that closely matches real-world sensor behavior.