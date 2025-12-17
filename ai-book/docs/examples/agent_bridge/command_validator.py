#!/usr/bin/env python3

"""
Command validator for ROS 2 agent bridge.

This example demonstrates how to validate ROS commands from AI agents
to ensure safe robot operation before execution.
"""

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