# Data Model: Module 1 — The Robotic Nervous System (ROS 2)

## Entities from Feature Specification

### ROS 2 Node
- **Description**: A process that performs computation in the ROS 2 system, capable of publishing and subscribing to topics
- **Attributes**: node_name (string), namespace (string, optional), parameters (dict)
- **Relationships**: publishes to Topics, subscribes to Topics, provides Services, executes Actions

### ROS 2 Topic
- **Description**: A communication channel over which nodes exchange messages using a publish/subscribe pattern
- **Attributes**: topic_name (string), message_type (string), qos_profile (QoS settings)
- **Relationships**: connects Nodes (publisher/subscriber), carries Messages

### ROS 2 Service
- **Description**: A synchronous communication pattern where one node sends a request and another node responds
- **Attributes**: service_name (string), request_type (string), response_type (string), qos_profile (QoS settings)
- **Relationships**: connects Nodes (client/server)

### ROS 2 Action
- **Description**: A communication pattern for long-running tasks with feedback and goal management
- **Attributes**: action_name (string), goal_type (string), result_type (string), feedback_type (string)
- **Relationships**: connects Nodes (client/server), manages Goals and Results

### URDF Model
- **Description**: XML-based description of a robot's physical structure including links, joints, and sensors
- **Attributes**: model_name (string), links (list of Link objects), joints (list of Joint objects), materials (list of Material objects)
- **Relationships**: contains Links and Joints, defines robot kinematics

### AI Agent
- **Description**: A Python-based decision-making system that processes information and generates commands for robot control
- **Attributes**: agent_name (string), decision_logic (function), command_queue (queue), state (dict)
- **Relationships**: connects to ROS 2 Nodes, generates Commands

### Link (URDF Component)
- **Description**: A rigid body in the robot model with physical properties
- **Attributes**: link_name (string), mass (float), inertia (matrix), visual_geometry (geometry object), collision_geometry (geometry object)
- **Relationships**: connected via Joints, part of URDF Model

### Joint (URDF Component)
- **Description**: Connection between two links with specific degrees of freedom
- **Attributes**: joint_name (string), joint_type (string), parent_link (string), child_link (string), limits (dict)
- **Relationships**: connects Links, part of URDF Model

## Validation Rules from Requirements

### Documentation Validation
- All examples must be complete and runnable (FR-009)
- Documentation must be in Markdown format for Docusaurus (FR-001)
- Clear execution steps required (FR-008)

### ROS 2 Communication Validation
- Command validation required before publishing (FR-005)
- Safe publishing to prevent invalid robot commands (FR-005)

### URDF Validation
- Model must load successfully in simulation (FR-007)
- Proper structure with links and joints (FR-006)