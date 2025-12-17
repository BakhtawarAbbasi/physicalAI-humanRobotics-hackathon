#!/usr/bin/env python3

"""
Agent node example for ROS 2.

This example demonstrates how to connect Python AI agents to ROS 2 controllers,
creating an end-to-end pipeline where agent decisions translate to ROS commands.
"""

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