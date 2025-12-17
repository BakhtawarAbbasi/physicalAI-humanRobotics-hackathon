---
title: Nav2 for Humanoid Navigation
sidebar_position: 3
---

# Nav2 for Humanoid Navigation

## Introduction

Navigation2 (Nav2) is the official navigation framework for ROS 2, providing path planning, trajectory generation, and obstacle avoidance capabilities for mobile robots. While originally designed for wheeled robots, Nav2 can be configured for humanoid robots with specific parameters to account for bipedal locomotion patterns and unique kinematic constraints.

This chapter will guide you through configuring Nav2 specifically for humanoid robot navigation, covering costmap parameters, path planning algorithms, and practical exercises for implementing navigation behaviors in simulation.

## Prerequisites

Before starting with Nav2 for Humanoid Navigation, ensure you have:
- Completed the Isaac Sim and Isaac ROS chapters
- ROS 2 workspace set up
- Isaac Sim environment running
- Isaac ROS perception pipeline configured
- Basic understanding of ROS 2 navigation concepts

## Nav2 Setup for Humanoid Robots

### Installing Nav2 Packages

First, install the necessary Nav2 packages:

```bash
# Install Nav2 packages
sudo apt update
sudo apt install ros-humble-navigation2 ros-humble-nav2-bringup
sudo apt install ros-humble-nav2-gui-tools

# Install additional packages for humanoid navigation
sudo apt install ros-humble-dwb-core ros-humble-angles
sudo apt install ros-humble-robot-localization
```

### Basic Nav2 Launch

Create a basic launch file for Nav2 with humanoid-specific configurations:

```python
# humanoid_nav2_bringup.py
import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, SetEnvironmentVariable
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
from nav2_common.launch import RewrittenYaml

def generate_launch_description():
    # Get the launch directory
    bringup_dir = get_package_share_directory('nav2_bringup')

    # Create the launch configuration variables
    use_sim_time = LaunchConfiguration('use_sim_time')
    params_file = LaunchConfiguration('params_file')
    default_nav2_yaml = os.path.join(bringup_dir, 'params/nav2_params.yaml')

    # Create our own temporary YAML files that include substitutions
    param_substitutions = {
        'use_sim_time': use_sim_time,
        'bt_xml_filename': 'navigate_w_replanning_and_recovery.xml',
        'global_frame': 'map',
        'robot_base_frame': 'base_link',
        'odom_topic': 'odom',
        'default_nav2_yaml': default_nav2_yaml
    }

    configured_params = RewrittenYaml(
        source_file=params_file,
        root_key='nav2',
        param_rewrites=param_substitutions,
        convert_types=True)

    return LaunchDescription([
        # Nodes
        Node(
            package='nav2_controller',
            executable='controller_server',
            output='screen',
            parameters=[configured_params, {'use_sim_time': use_sim_time}]),
        Node(
            package='nav2_planner',
            executable='planner_server',
            name='planner_server',
            output='screen',
            parameters=[configured_params, {'use_sim_time': use_sim_time}]),
        Node(
            package='nav2_recoveries',
            executable='recoveries_server',
            name='recoveries_server',
            output='screen',
            parameters=[configured_params, {'use_sim_time': use_sim_time}]),
        Node(
            package='nav2_bt_navigator',
            executable='bt_navigator',
            name='bt_navigator',
            output='screen',
            parameters=[configured_params, {'use_sim_time': use_sim_time}]),
        Node(
            package='nav2_waypoint_follower',
            executable='waypoint_follower',
            name='waypoint_follower',
            output='screen',
            parameters=[configured_params, {'use_sim_time': use_sim_time}]),
        Node(
            package='nav2_lifecycle_manager',
            executable='lifecycle_manager',
            name='lifecycle_manager',
            output='screen',
            parameters=[{'use_sim_time': use_sim_time},
                        {'autostart': True},
                        {'node_names': ['controller_server',
                                        'planner_server',
                                        'recoveries_server',
                                        'bt_navigator',
                                        'waypoint_follower']}])
    ])
```

## Costmap Parameters for Bipedal Locomotion

### Humanoid-Specific Costmap Configuration

Humanoid robots have different navigation requirements compared to wheeled robots. The costmap parameters need to be adjusted to account for:

- Wider turning radius due to bipedal locomotion
- Different obstacle clearance requirements
- Footstep planning considerations
- Balance and stability constraints

Create a configuration file for humanoid-specific costmap parameters:

```yaml
# humanoid_costmap_params.yaml
amcl:
  ros__parameters:
    use_sim_time: True
    alpha1: 0.2
    alpha2: 0.2
    alpha3: 0.2
    alpha4: 0.2
    alpha5: 0.2
    base_frame_id: "base_footprint"
    beam_skip_distance: 0.5
    beam_skip_error_threshold: 0.9
    beam_skip_threshold: 0.3
    do_beamskip: false
    global_frame_id: "map"
    lambda_short: 0.1
    laser_likelihood_max_dist: 2.0
    laser_max_range: 100.0
    laser_min_range: -1.0
    max_beams: 60
    max_particles: 2000
    min_particles: 500
    odom_frame_id: "odom"
    pf_err: 0.05
    pf_z: 0.99
    recovery_alpha_fast: 0.0
    recovery_alpha_slow: 0.0
    resample_interval: 1
    robot_model_type: "nav2_amcl::DifferentialMotionModel"
    save_pose_rate: 0.5
    sigma_hit: 0.2
    tf_broadcast: true
    transform_tolerance: 1.0
    update_min_a: 0.2
    update_min_d: 0.25
    z_hit: 0.5
    z_max: 0.05
    z_rand: 0.5
    z_short: 0.05

amcl_map_client:
  ros__parameters:
    use_sim_time: True

amcl_rclcpp_node:
  ros__parameters:
    use_sim_time: True

bt_navigator:
  ros__parameters:
    use_sim_time: True
    global_frame: map
    robot_base_frame: base_link
    odom_topic: /odom
    bt_loop_duration: 10
    default_server_timeout: 20
    enable_groot_monitoring: True
    groot_zmq_publisher_port: 1666
    groot_zmq_server_port: 1667
    # Specify the path to the Behavior Tree XML file
    bt_xml_filename: "navigate_w_replanning_and_recovery.xml"
    # Remap the action topic for the navigator
    action_server_result_timeout: 900.0

bt_navigator_rclcpp_node:
  ros__parameters:
    use_sim_time: True

controller_server:
  ros__parameters:
    use_sim_time: True
    controller_frequency: 10.0
    min_x_velocity_threshold: 0.001
    min_y_velocity_threshold: 0.5
    min_theta_velocity_threshold: 0.001
    progress_checker_plugin: "progress_checker"
    goal_checker_plugin: "goal_checker"
    controller_plugins: ["FollowPath"]

    # Humanoid-specific controller configuration
    FollowPath:
      plugin: "dwb_core::DWBLocalPlanner"
      debug_trajectory_details: True
      min_vel_x: 0.0
      min_vel_y: 0.0
      max_vel_x: 0.5  # Slower for humanoid stability
      max_vel_y: 0.0
      max_vel_theta: 0.5
      min_speed_xy: 0.0
      max_speed_xy: 0.5
      min_speed_theta: 0.0
      acc_lim_x: 2.5
      acc_lim_y: 0.0
      acc_lim_theta: 3.2
      decel_lim_x: -2.5
      decel_lim_y: 0.0
      decel_lim_theta: -3.2
      vx_samples: 20
      vy_samples: 0
      vtheta_samples: 40
      sim_time: 1.7
      linear_granularity: 0.05
      angular_granularity: 0.025
      transform_tolerance: 0.2
      xy_goal_tolerance: 0.25  # Larger for humanoid movement
      yaw_goal_tolerance: 0.25
      stateful: True
      oscillation_reset_dist: 0.05
      oscillation_magic_number: 4
      oscillation_lower_tm: 0.5
      oscillation_filter_duration: 0.1
      goal_function: "dwb_plugins::SimpleGoalChecker"
      trajectory_generator_name: "dwb_plugins::StandardTrajectoryGenerator"
      goal_checker_name: "dwb_plugins::SimpleGoalChecker"

controller_server_rclcpp_node:
  ros__parameters:
    use_sim_time: True

local_costmap:
  local_costmap:
    ros__parameters:
      update_frequency: 5.0
      publish_frequency: 2.0
      global_frame: odom
      robot_base_frame: base_link
      use_sim_time: True
      rolling_window: true
      width: 6  # Wider for humanoid movement
      height: 6
      resolution: 0.05  # Higher resolution for precision
      origin_x: 0.0
      origin_y: 0.0
      # Humanoid-specific inflation
      plugins: ["voxel_layer", "inflation_layer"]
      inflation_layer:
        plugin: "nav2_costmap_2d::InflationLayer"
        cost_scaling_factor: 3.0  # More conservative for humanoid
        inflation_radius: 1.0     # Larger for humanoid safety
        inflate_unknown: false
        inflate_around_unknown: true
      voxel_layer:
        plugin: "nav2_costmap_2d::VoxelLayer"
        enabled: True
        publish_voxel_map: False
        origin_z: 0.0
        z_resolution: 0.2
        z_voxels: 10
        max_obstacle_height: 2.0
        mark_threshold: 0
        observation_sources: scan
        scan:
          topic: /scan
          max_obstacle_height: 2.0
          clearing: True
          marking: True
          data_type: "LaserScan"
          raytrace_max_range: 3.0
          raytrace_min_range: 0.0
          obstacle_max_range: 2.5
          obstacle_min_range: 0.0
  local_costmap_client:
    ros__parameters:
      use_sim_time: True
  local_costmap_rclcpp_node:
    ros__parameters:
      use_sim_time: True

global_costmap:
  global_costmap:
    ros__parameters:
      update_frequency: 1.0
      publish_frequency: 1.0
      global_frame: map
      robot_base_frame: base_link
      use_sim_time: True
      robot_radius: 0.3  # Larger for humanoid safety
      resolution: 0.05
      track_unknown_space: true
      plugins: ["static_layer", "obstacle_layer", "inflation_layer"]
      obstacle_layer:
        plugin: "nav2_costmap_2d::ObstacleLayer"
        enabled: True
        observation_sources: scan
        scan:
          topic: /scan
          max_obstacle_height: 2.0
          clearing: True
          marking: True
          data_type: "LaserScan"
          raytrace_max_range: 3.0
          raytrace_min_range: 0.0
          obstacle_max_range: 2.5
          obstacle_min_range: 0.0
      static_layer:
        plugin: "nav2_costmap_2d::StaticLayer"
        map_subscribe_transient_local: True
      inflation_layer:
        plugin: "nav2_costmap_2d::InflationLayer"
        cost_scaling_factor: 3.0
        inflation_radius: 1.0  # Larger for humanoid safety
        inflate_unknown: false
        inflate_around_unknown: true
  global_costmap_client:
    ros__parameters:
      use_sim_time: True
  global_costmap_rclcpp_node:
    ros__parameters:
      use_sim_time: True

planner_server:
  ros__parameters:
    expected_planner_frequency: 20.0
    use_sim_time: True
    planner_plugins: ["GridBased"]
    GridBased:
      plugin: "nav2_navfn_planner/NavfnPlanner"
      tolerance: 0.5  # Larger tolerance for humanoid
      use_astar: false
      allow_unknown: true

planner_server_rclcpp_node:
  ros__parameters:
    use_sim_time: True

recoveries_server:
  ros__parameters:
    costmap_topic: local_costmap/costmap_raw
    footprint_topic: local_costmap/published_footprint
    cycle_frequency: 10.0
    recovery_plugins: ["spin", "backup", "wait"]
    recovery_plugin_types: ["nav2_recoveries/Spin", "nav2_recoveries/BackUp", "nav2_recoveries/Wait"]
    spin:
      plugin: "nav2_recoveries/Spin"
      sim_frequency: 10
      cycle_frequency: 10
      acceleration: 1.0
      max_rotational_vel: 1.0
      min_rotational_vel: 0.4
      rotational_acc_lim: 3.2
    backup:
      plugin: "nav2_recoveries/BackUp"
      sim_frequency: 10
      cycle_frequency: 10
      safety_factor: 1.0
      backup_vel: -0.1
    wait:
      plugin: "nav2_recoveries/Wait"
      sim_frequency: 10
      cycle_frequency: 10
      wait_duration: 1.0

## Path Planning Algorithm Configuration

### Humanoid-Specific Path Planning

Path planning for humanoid robots requires special considerations due to their bipedal nature and balance constraints:

1. **Footstep Planning**: Unlike wheeled robots, humanoid robots must plan where to place each foot
2. **Balance Constraints**: The path must maintain the robot's center of mass within stable regions
3. **Step Size Limitations**: Humanoid robots have maximum step size constraints
4. **Turning Radius**: Humanoid robots typically have larger minimum turning radii

### Configuring Path Planners for Humanoid Robots

The Navfn planner used in the configuration above is suitable for humanoid robots with proper parameter tuning:

- Increase tolerance values to account for the discrete nature of humanoid steps
- Adjust the potential field parameters to create smoother paths
- Use higher resolution maps to capture fine-grained navigation constraints

## Practical Navigation Exercises

### Exercise 1: Basic Humanoid Navigation Setup

1. Launch Isaac Sim with a humanoid robot model
2. Configure the Nav2 stack with humanoid-specific parameters
3. Set up a simple navigation goal
4. Execute the navigation and observe the robot's behavior

### Exercise 2: Costmap Tuning for Humanoid Navigation

1. Start with the default costmap configuration
2. Test navigation in a simple environment
3. Adjust inflation radius and cost scaling factor
4. Observe the impact on navigation behavior
5. Fine-tune parameters for optimal performance

### Exercise 3: Path Planning in Complex Environments

1. Create a complex environment in Isaac Sim with narrow passages
2. Configure Nav2 with appropriate parameters for humanoid navigation
3. Test path planning and execution with various goal positions
4. Evaluate the robot's ability to navigate through tight spaces

## Troubleshooting and Fine-tuning

### Common Issues

1. **Oscillation**: Humanoid robots may oscillate when approaching goals due to balance constraints
   - Solution: Increase `xy_goal_tolerance` and `yaw_goal_tolerance` values

2. **Path Following Inaccuracy**: Humanoid robots may not follow paths precisely
   - Solution: Adjust controller parameters, especially velocity and acceleration limits

3. **Costmap Issues**: Humanoid robots may not navigate properly in narrow spaces
   - Solution: Adjust robot radius and inflation parameters appropriately

4. **Recovery Behavior**: Default recovery behaviors may not be suitable for humanoid robots
   - Solution: Customize recovery plugins for humanoid-specific movements

### Performance Tuning

1. **Costmap Resolution**: Higher resolution costmaps provide better precision but require more computation
2. **Update Frequency**: Balance between responsiveness and computational load
3. **Controller Frequency**: Match to the humanoid robot's control capabilities
4. **Trajectory Optimization**: Adjust for smooth, stable humanoid movement

## Integration with Isaac ROS Perception

### Sensor Fusion for Navigation

Combine Isaac ROS perception with Nav2 for enhanced navigation capabilities:

```yaml
# Example sensor fusion configuration
robot_localization:
  ros__parameters:
    # Configure for humanoid robot
    frequency: 50.0
    sensor_timeout: 0.1
    two_d_mode: true
    map_frame: map
    odom_frame: odom
    base_link_frame: base_link
    world_frame: odom

    # IMU input for balance information
    imu0: imu/data
    imu0_config: [false, false, false,   # No position from IMU
                  false, false, false,   # No velocity from IMU
                  true,  true,  true ]   # Yes, orientation from IMU
```

### Perception-Guided Navigation

Use Isaac ROS perception outputs to enhance navigation:

1. **Semantic Map Integration**: Use semantic segmentation to identify navigable surfaces
2. **Dynamic Obstacle Avoidance**: Use object detection to avoid moving obstacles
3. **Terrain Classification**: Use perception to identify suitable footstep locations

## Summary

This chapter covered Nav2 configuration for humanoid robot navigation and path planning. You learned about:

- Nav2 setup specifically for humanoid robots
- Costmap parameters tailored for bipedal locomotion
- Path planning algorithm configuration for humanoid constraints
- Practical exercises for implementing navigation behaviors
- Troubleshooting and fine-tuning techniques
- Integration with Isaac ROS perception systems

The configuration files and parameters provided in this chapter form a solid foundation for humanoid robot navigation that can be further customized based on specific robot hardware and application requirements.

## Next Steps

Review previous chapters on [Isaac Sim](./isaac-sim) and [Isaac ROS Perception](./isaac-ros).