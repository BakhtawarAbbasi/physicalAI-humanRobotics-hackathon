---
sidebar_position: 2
title: 'Chapter 2 - Bridging Python Agents to ROS Controllers'
description: 'Connecting Python AI agents to ROS 2 using rclpy to create an end-to-end pipeline'
---

# Chapter 2 - Bridging Python Agents to ROS Controllers

## Introduction

In this chapter, you'll learn how to connect Python AI agents to ROS 2 controllers, creating an end-to-end pipeline where agent decisions translate to ROS commands. This bridge is essential for enabling AI agents to control simulated robots effectively.

## The Agent-to-ROS Architecture

The agent-to-ROS bridge consists of several key components:

1. **AI Agent**: Makes decisions based on input data
2. **Command Validator**: Ensures commands are safe and valid before execution
3. **ROS Node Interface**: Publishes validated commands to ROS controllers
4. **Feedback System**: Provides results back to the agent

## Implementing an Agent Node

Let's create a simple AI agent that makes decisions and publishes them to ROS controllers.

### Agent Node Implementation

```python
# agent_node.py
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from geometry_msgs.msg import Twist
import random
import time


class AgentNode(Node):
    def __init__(self):
        super().__init__('agent_node')

        # Publisher for movement commands
        self.cmd_vel_publisher = self.create_publisher(Twist, '/cmd_vel', 10)

        # Publisher for general commands
        self.command_publisher = self.create_publisher(String, '/agent_commands', 10)

        # Timer to run the agent logic periodically
        self.timer = self.create_timer(1.0, self.agent_logic)

        self.get_logger().info('Agent node initialized')

    def agent_logic(self):
        """
        Main agent decision-making logic
        This is where the AI agent would process sensor data and make decisions
        """
        # Simulate agent processing
        decision = self.make_decision()

        # Publish the decision as a command
        self.publish_command(decision)

    def make_decision(self):
        """
        Simulate the agent's decision-making process
        In a real application, this would process sensor data
        """
        # Simulate different types of decisions
        decisions = [
            "move_forward",
            "turn_left",
            "turn_right",
            "stop",
            "explore"
        ]

        return random.choice(decisions)

    def publish_command(self, decision):
        """
        Publish the agent's decision as a ROS command
        """
        # Create and populate a Twist message for movement commands
        if decision in ["move_forward", "explore"]:
            msg = Twist()
            msg.linear.x = 0.5  # Move forward at 0.5 m/s
            msg.angular.z = 0.0  # No rotation
            self.cmd_vel_publisher.publish(msg)
            self.get_logger().info(f'Agent decided: {decision}, publishing linear velocity: {msg.linear.x}')
        elif decision == "turn_left":
            msg = Twist()
            msg.linear.x = 0.0
            msg.angular.z = 0.5  # Turn left at 0.5 rad/s
            self.cmd_vel_publisher.publish(msg)
            self.get_logger().info(f'Agent decided: {decision}, publishing angular velocity: {msg.angular.z}')
        elif decision == "turn_right":
            msg = Twist()
            msg.linear.x = 0.0
            msg.angular.z = -0.5  # Turn right at 0.5 rad/s
            self.cmd_vel_publisher.publish(msg)
            self.get_logger().info(f'Agent decided: {decision}, publishing angular velocity: {msg.angular.z}')
        elif decision == "stop":
            msg = Twist()
            msg.linear.x = 0.0
            msg.angular.z = 0.0
            self.cmd_vel_publisher.publish(msg)
            self.get_logger().info(f'Agent decided: {decision}, stopping')
        else:
            # General command message
            cmd_msg = String()
            cmd_msg.data = decision
            self.command_publisher.publish(cmd_msg)
            self.get_logger().info(f'Agent decided: {decision}, publishing general command')


def main(args=None):
    rclpy.init(args=args)
    agent_node = AgentNode()

    try:
        rclpy.spin(agent_node)
    except KeyboardInterrupt:
        pass
    finally:
        agent_node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
```

## Command Validation System

Safety is crucial when bridging AI agents to robot controllers. Let's implement a command validation system.

### Command Validator Implementation

```python
# command_validator.py
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from std_msgs.msg import String
from rcl_interfaces.msg import ParameterType


class CommandValidator(Node):
    def __init__(self):
        super().__init__('command_validator')

        # Subscribe to raw agent commands
        self.subscription = self.create_subscription(
            Twist,
            '/raw_agent_commands',
            self.command_callback,
            10
        )

        # Publisher for validated commands
        self.validated_publisher = self.create_publisher(Twist, '/cmd_vel', 10)

        # Publisher for validation status
        self.status_publisher = self.create_publisher(String, '/validation_status', 10)

        # Define safety limits
        self.linear_velocity_limit = 1.0  # m/s
        self.angular_velocity_limit = 1.0  # rad/s

        self.get_logger().info('Command validator initialized')

    def command_callback(self, msg):
        """
        Validate incoming commands and publish only safe ones
        """
        validated_msg = Twist()
        is_valid = True
        status_msg = String()

        # Validate linear velocity
        if abs(msg.linear.x) > self.linear_velocity_limit:
            validated_msg.linear.x = self.linear_velocity_limit if msg.linear.x > 0 else -self.linear_velocity_limit
            is_valid = False
            self.get_logger().warn(f'Linear velocity limited: {msg.linear.x} -> {validated_msg.linear.x}')
        else:
            validated_msg.linear.x = msg.linear.x

        # Validate angular velocity
        if abs(msg.angular.z) > self.angular_velocity_limit:
            validated_msg.angular.z = self.angular_velocity_limit if msg.angular.z > 0 else -self.angular_velocity_limit
            is_valid = False
            self.get_logger().warn(f'Angular velocity limited: {msg.angular.z} -> {validated_msg.angular.z}')
        else:
            validated_msg.angular.z = msg.angular.z

        # Copy other fields
        validated_msg.linear.y = msg.linear.y
        validated_msg.linear.z = msg.linear.z
        validated_msg.angular.x = msg.angular.x
        validated_msg.angular.y = msg.angular.y

        # Publish validation status
        status_msg.data = "VALID" if is_valid else "INVALID_COMMAND_MODIFIED"
        self.status_publisher.publish(status_msg)

        # Publish the validated (or modified) command
        self.validated_publisher.publish(validated_msg)

        if is_valid:
            self.get_logger().info('Valid command published')
        else:
            self.get_logger().info('Invalid command modified and published')


def main(args=None):
    rclpy.init(args=args)
    validator = CommandValidator()

    try:
        rclpy.spin(validator)
    except KeyboardInterrupt:
        pass
    finally:
        validator.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
```

## Complete Agent-Controller Pipeline

Now let's put it all together in a complete pipeline that demonstrates the end-to-end flow:

### Complete Example

```python
# Complete example showing the agent-ros bridge
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from std_msgs.msg import String
import random
import math


class AgentROSController(Node):
    def __init__(self):
        super().__init__('agent_ros_controller')

        # Publishers
        self.cmd_vel_publisher = self.create_publisher(Twist, '/cmd_vel', 10)
        self.status_publisher = self.create_publisher(String, '/agent_status', 10)

        # Timer for agent logic
        self.timer = self.create_timer(0.5, self.agent_behavior)

        # Agent state
        self.state = "IDLE"
        self.target_x = 0.0
        self.target_y = 0.0

        self.get_logger().info('Agent-ROS controller bridge initialized')

    def agent_behavior(self):
        """
        Main agent behavior loop
        """
        # Simulate environment perception
        perceived_environment = self.perceive_environment()

        # Make a decision based on perception
        decision = self.decide_action(perceived_environment)

        # Execute the decision
        self.execute_decision(decision)

        # Update status
        status_msg = String()
        status_msg.data = f"State: {self.state}, Decision: {decision}"
        self.status_publisher.publish(status_msg)

    def perceive_environment(self):
        """
        Simulate perception of the environment
        In a real robot, this would process sensor data
        """
        # Simulate some environmental data
        return {
            'obstacle_distance': random.uniform(0.5, 5.0),
            'target_direction': random.uniform(-math.pi, math.pi),
            'battery_level': random.uniform(20, 100)
        }

    def decide_action(self, environment_data):
        """
        Decision-making logic for the agent
        """
        obstacle_distance = environment_data['obstacle_distance']
        battery_level = environment_data['battery_level']

        if battery_level < 30:
            return "RETURN_TO_BASE"
        elif obstacle_distance < 1.0:
            return "AVOID_OBSTACLE"
        elif obstacle_distance > 2.0:
            return "MOVE_FORWARD"
        else:
            return "EXPLORE"

    def execute_decision(self, decision):
        """
        Execute the agent's decision by publishing ROS commands
        """
        msg = Twist()

        if decision == "MOVE_FORWARD":
            msg.linear.x = 0.5
            msg.angular.z = 0.0
            self.state = "MOVING_FORWARD"
        elif decision == "AVOID_OBSTACLE":
            msg.linear.x = 0.0
            msg.angular.z = 0.5  # Turn to avoid
            self.state = "AVOIDING"
        elif decision == "EXPLORE":
            msg.linear.x = 0.3
            msg.angular.z = random.uniform(-0.3, 0.3)  # Random slight turn
            self.state = "EXPLORING"
        elif decision == "RETURN_TO_BASE":
            msg.linear.x = -0.3  # Move backward toward base
            msg.angular.z = 0.0
            self.state = "RETURNING"
        else:
            msg.linear.x = 0.0
            msg.angular.z = 0.0
            self.state = "IDLE"

        self.cmd_vel_publisher.publish(msg)
        self.get_logger().info(f'Executing: {decision}, Linear: {msg.linear.x}, Angular: {msg.angular.z}')


def main(args=None):
    rclpy.init(args=args)
    controller = AgentROSController()

    try:
        rclpy.spin(controller)
    except KeyboardInterrupt:
        pass
    finally:
        controller.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
```

## Prerequisites

Before running the examples in this chapter, ensure you have:

1. **ROS 2 Installed**: Install ROS 2 Humble Hawksbill (or later) from https://docs.ros.org/
2. **Python 3.8+**: Required for running Python-based ROS 2 nodes
3. **rclpy**: Python client library for ROS 2
4. **geometry_msgs**: For Twist messages (`ros2 pkg list | grep geometry_msgs`)

## Running the Examples

To run the agent-ROS bridge examples:

1. Open a terminal and source your ROS 2 installation:
   ```bash
   source /opt/ros/humble/setup.bash  # Adjust for your ROS 2 distribution
   ```

2. Navigate to the examples directory:
   ```bash
   cd ai-book/docs/examples/agent_bridge/
   ```

3. Run the agent node:
   ```bash
   python3 agent_node.py
   ```

4. In another terminal, run the command validator:
   ```bash
   python3 command_validator.py
   ```

5. You can also run the complete example:
   ```bash
   python3 agent_ros_controller.py
   ```

## Verification

To verify that the agent-ROS bridge is working correctly:

1. Check that the agent is publishing commands:
   ```bash
   ros2 topic echo /cmd_vel geometry_msgs/msg/Twist
   ```

2. Monitor validation status:
   ```bash
   ros2 topic echo /validation_status std_msgs/msg/String
   ```

3. Check agent status:
   ```bash
   ros2 topic echo /agent_status std_msgs/msg/String
   ```

## Summary

In this chapter, you learned how to create a bridge between Python AI agents and ROS controllers:

- Implemented an agent node that makes decisions and publishes ROS commands
- Created a command validation system to ensure safe robot operation
- Built a complete end-to-end pipeline from agent decision to robot action
- Added safety checks and validation to prevent invalid robot commands

This bridge enables AI agents to control robots safely and effectively, forming a crucial component in autonomous robotic systems.