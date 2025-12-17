---
sidebar_position: 1
title: 'Chapter 1 - Gazebo Physics Simulation'
description: 'Learn about physics-based simulation in Gazebo with gravity, collisions, and joints for humanoid robots'
---

# Chapter 1 - Gazebo Physics Simulation

## Introduction to Gazebo Physics Simulation

Gazebo is a powerful physics simulator that provides realistic simulation of robots in 3D environments. It incorporates accurate physics simulation with features such as collision detection, rigid body dynamics, and sensor simulation. For humanoid robotics, Gazebo provides the essential foundation for testing robot behaviors before deployment to real hardware.

## Understanding Gazebo Physics

Gazebo's physics engine simulates the laws of physics to provide realistic robot-world interactions. The key components of Gazebo physics include:

### Gravity
Gravity is a fundamental force in physics simulation that affects all objects with mass. In Gazebo, gravity is enabled by default and acts in the negative Z-direction (downward). The default gravity setting is 9.8 m/s², mimicking Earth's gravitational acceleration.

### Collision Detection
Collision detection algorithms determine when two objects come into contact with each other. Gazebo supports various collision detection engines such as Bullet, ODE, Simbody, and DART. Proper collision detection ensures that objects behave realistically when they come into contact.

### Joint Constraints
Joints define the allowable motion between two bodies. Different joint types provide various degrees of freedom:
- **Fixed joints**: Completely constrain motion between bodies
- **Revolute joints**: Allow rotation around a single axis
- **Prismatic joints**: Allow linear translation along a single axis
- **Continuous joints**: Allow unlimited rotation around an axis
- **Floating joints**: Allow motion in all directions (rarely used)

## Setting Up Gazebo Environment

Before starting the simulation, ensure you have Gazebo Garden (or compatible version) installed with proper ROS 2 integration. The following environment variables should be set:

```bash
# Source ROS 2 installation
source /opt/ros/humble/setup.bash

# Optionally, source Gazebo installation (if needed)
source /usr/share/gazebo/setup.sh
```

## Spawning Humanoid URDF Models in Gazebo

URDF (Unified Robot Description Format) models can be spawned in Gazebo to simulate humanoid robots. Here's the typical process:

### 1. Prepare the URDF Model
Ensure your humanoid URDF model is properly defined with all necessary elements such as links, joints, inertial properties, and visual/collision meshes.

### 2. Create a Spawn Launch File
Create a launch file to spawn your robot model in Gazebo:

```python
# robot_spawn.launch.py
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from launch.actions import ExecuteProcess
import os

def generate_launch_description():
    ld = LaunchDescription()

    # Arguments
    model_arg = DeclareLaunchArgument(
        'model',
        default_value='simple_humanoid.urdf',
        description='Robot description file'
    )

    # Get URDF file path
    urdf_file = os.path.join(
        os.path.expanduser('~'),
        'models',
        LaunchConfiguration('model')
    )

    # Launch Gazebo with world
    gazebo = ExecuteProcess(
        cmd=['gz', 'sim', '-r', 'empty.sdf'],
        output='screen'
    )

    # Spawn robot in Gazebo
    spawn_entity = Node(
        package='ros_gz_sim',
        executable='spawn_entity.py',
        arguments=[
            '-file', urdf_file,
            '-entity', 'humanoid_robot',
            '-x', '0.0',
            '-y', '0.0',
            '-z', '1.0'  # Start slightly above ground
        ],
        output='screen'
    )

    # Add actions to launch description
    ld.add_action(model_arg)
    ld.add_action(gazebo)
    ld.add_action(spawn_entity)

    return ld
```

### 3. Physics Configuration
Configure physics parameters for realistic simulation:

```yaml
# physics_params.yaml
gravity: [0.0, 0.0, -9.81]
ode_physics:
  solver_type: world
  iters: 10
  sor: 1.0
  use_dynamic_mmu: false
  friction_model: pyramid_simplified_friction
  min_step_size: 0.001
  max_step_size: 0.01
  real_time_factor: 1.0
  max_contacts: 20

collision_detector: bullet
constraint_solver: ode
```

## Practical Example: Simple Humanoid Robot

Let's create a simple humanoid robot model and simulate it in Gazebo with physics enabled.

### Robot Model Structure
Our simple humanoid robot consists of:
- Torso (base link)
- Head
- Two arms (left and right)
- Two legs (left and right)

### URDF Configuration
The URDF file should define the physical properties for each link:

```xml
<!-- Example simplified URDF snippet -->
<link name="torso">
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
```

## Running the Physics Simulation

To run the physics simulation:

### Prerequisites
1. Install ROS 2 Humble Hawksbill following the official installation guide
2. Install Gazebo Garden (or compatible version) with ROS 2 integration
3. Verify that the `ros_gz_sim` package is installed:
   ```bash
   sudo apt install ros-humble-ros-gz-sim
   ```

### Execution Steps
1. Make sure Gazebo is installed and properly configured:
   ```bash
   # Verify Gazebo installation
   gz --version

   # Source ROS 2 installation
   source /opt/ros/humble/setup.bash
   ```

2. Create your ROS 2 workspace and copy the example files:
   ```bash
   # Create workspace
   mkdir -p ~/ros_workspace/src
   cd ~/ros_workspace

   # Copy the launch file to your package
   # (Assuming you have a package called 'humanoid_simulation')
   cp docs/examples/gazebo_configs/robot_spawn.launch.py ~/ros_workspace/src/humanoid_simulation/launch/
   ```

3. Ensure your URDF model is valid and includes all necessary physical properties

4. Build your workspace:
   ```bash
   cd ~/ros_workspace
   colcon build --packages-select humanoid_simulation
   source install/setup.bash
   ```

5. Run the launch file:
   ```bash
   ros2 launch humanoid_simulation robot_spawn.launch.py
   ```

### Alternative: Running with Custom Physics Parameters
To use custom physics parameters, you can launch Gazebo with a custom world file that includes your physics configuration:

```bash
# Launch Gazebo with custom physics parameters
gz sim -r -v 4 --physics-profile my_physics_profile empty.sdf
```

Or integrate the physics parameters directly into your launch file by modifying the Gazebo execution command.

## Verification and Troubleshooting

### Checking Simulation Behavior
1. Verify that the robot responds to gravity (falls to the ground initially)
2. Check that joints behave appropriately with constraints
3. Confirm collision detection works (robot doesn't fall through surfaces)

### Common Issues and Solutions
- **Robot falls through floor**: Check collision geometries and physics parameters
- **Joints behave unexpectedly**: Verify joint limits and types in URDF
- **Simulation runs slowly**: Adjust physics parameters (step size, solver iterations)
- **Robot shakes or behaves unstably**: Fine-tune PID controllers or adjust physics parameters

## Gazebo Simulation and Physics Parameters

### Physics Engine Configuration
Gazebo supports multiple physics engines, each with specific strengths:

- **ODE (Open Dynamics Engine)**: Default engine, good balance of performance and accuracy
- **Bullet**: Good for complex collision detection scenarios
- **DART**: Advanced dynamics and kinematics library with robust constraint solving
- **Simbody**: High-fidelity multibody dynamics simulation

### Physics Parameters Deep Dive
The physics parameters in `physics_params.yaml` control the simulation behavior:

```yaml
gravity: [0.0, 0.0, -9.81]  # Gravity vector (x, y, z) in m/s²
ode_physics:
  solver_type: world         # Solver algorithm ('world', 'quick')
  iters: 10                  # Number of solver iterations per time step
  sor: 1.0                   # Successive Over-Relaxation parameter
  use_dynamic_mmu: false     # Enable dynamic CPU core scaling
  friction_model: pyramid_simplified_friction  # Friction computation model
  min_step_size: 0.001       # Minimum simulation time step (seconds)
  max_step_size: 0.01        # Maximum simulation time step (seconds)
  real_time_factor: 1.0      # Target simulation speed relative to real-time
  max_contacts: 20           # Maximum contacts per collision

collision_detector: bullet   # Collision detection engine
constraint_solver: ode       # Constraint solver to use
```

### Parameter Tuning Guidelines
For optimal simulation performance and stability, consider these guidelines:

- **Step size**:
  - Smaller values (0.001) provide better accuracy but slower simulation
  - Larger values (0.01) provide faster simulation but may be unstable
  - Start with 0.001 and increase if performance is critical

- **Solver iterations**:
  - Higher values (20-50) provide better accuracy but slower simulation
  - Lower values (5-10) provide faster simulation but less stability
  - For humanoid robots, 10-20 iterations typically work well

- **Real-time factor**:
  - Value of 1.0 means simulation runs at real-time speed
  - Values > 1.0 mean simulation runs faster than real-time
  - Values < 1.0 mean simulation runs slower than real-time

- **Contact parameters**:
  - Adjust contact stiffness and damping for realistic collision responses
  - Higher stiffness values create more rigid contacts
  - Proper damping prevents unrealistic oscillations

## Summary

This chapter introduced the fundamentals of Gazebo physics simulation for humanoid robots. You learned about:
- Gravity, collision detection, and joint constraints
- Setting up the simulation environment
- Spawning URDF models in Gazebo
- Configuring physics parameters
- Troubleshooting common issues

The physics simulation forms the foundation for all subsequent simulation work including sensor simulation and control algorithms. Proper configuration ensures realistic behavior and accurate results in simulation.