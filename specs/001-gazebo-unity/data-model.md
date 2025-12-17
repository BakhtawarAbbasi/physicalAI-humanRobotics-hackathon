# Data Model: Module 2 — The Digital Twin (Gazebo & Unity)

## Entities from Feature Specification

### Gazebo Simulation
- **Description**: Physics-based simulation environment with gravity, collision detection, and joint constraints
- **Attributes**: physics_params (dict), gravity (float), collision_detection (string), joint_constraints (dict)
- **Relationships**: hosts Humanoid Robot Model, generates data for Simulated Sensors, connects to ROS 2 Data Streams

### Humanoid Robot Model
- **Description**: URDF-based robot with multiple joints and links for realistic movement
- **Attributes**: urdf_file (string), joint_count (int), link_count (int), physical_properties (dict)
- **Relationships**: spawned in Gazebo Simulation, equipped with Simulated Sensors, controlled via ROS 2 Data Streams

### Simulated Sensors
- **Description**: Virtual LiDAR, camera, and IMU sensors that generate realistic ROS 2 data streams
- **Attributes**: sensor_type (string), data_frequency (float), accuracy_params (dict), topic_names (list)
- **Relationships**: attached to Humanoid Robot Model, publishes to ROS 2 Data Streams, simulates in Gazebo Simulation

### Unity Digital Twin
- **Description**: Real-time 3D visualization environment that mirrors the simulation state
- **Attributes**: visualization_params (dict), sync_frequency (float), rendering_quality (string), interaction_modes (list)
- **Relationships**: subscribes to ROS 2 Data Streams, mirrors Gazebo Simulation state

### ROS 2 Data Streams
- **Description**: Topics and messages that connect simulation components and provide sensor data
- **Attributes**: topic_names (list), message_types (list), frequencies (dict), data_formats (dict)
- **Relationships**: connects Gazebo Simulation to Unity Digital Twin, carries data from Simulated Sensors

### Physics Parameters
- **Description**: Configuration settings that control gravity, friction, and other physical properties
- **Attributes**: gravity (float), friction (dict), damping (dict), material_properties (dict)
- **Relationships**: applied to Gazebo Simulation, affects Humanoid Robot Model behavior

## Validation Rules from Requirements

### Documentation Validation
- All examples must be complete and runnable (FR-009)
- Documentation must be in Markdown format for Docusaurus (FR-001)
- Clear execution steps required (FR-007)

### Simulation Validation
- Physics simulation must include gravity, collisions, and joint constraints (FR-002)
- Humanoid URDF models must spawn correctly in Gazebo (FR-003)
- Sensor data must be realistic and consistent with physical simulation (FR-008)

### Visualization Validation
- Unity visualization must mirror Gazebo simulation state (FR-005)
- Real-time synchronization must be maintained (FR-006)
- Connection failures must be handled gracefully (FR-009)