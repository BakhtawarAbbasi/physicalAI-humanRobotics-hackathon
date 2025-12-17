#!/usr/bin/env python3

"""
Simple publisher and subscriber example for ROS 2.

This example demonstrates the basic concepts of ROS 2 communication
using publisher and subscriber nodes.
"""

import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import argparse


class PublisherNode(Node):
    def __init__(self):
        super().__init__('publisher_node')
        self.publisher = self.create_publisher(String, 'chatter', 10)
        timer_period = 0.5  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0

    def timer_callback(self):
        msg = String()
        msg.data = f'Hello ROS 2 World: {self.i}'
        self.publisher.publish(msg)
        self.get_logger().info(f'Publishing: "{msg.data}"')
        self.i += 1


class SubscriberNode(Node):
    def __init__(self):
        super().__init__('subscriber_node')
        self.subscription = self.create_subscription(
            String,
            'chatter',
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning

    def listener_callback(self, msg):
        self.get_logger().info(f'I heard: "{msg.data}"')


def main(args=None):
    parser = argparse.ArgumentParser(description='Publisher/Subscriber example')
    parser.add_argument('--role', choices=['publisher', 'subscriber'],
                       help='Run as publisher or subscriber node')
    args_cmd = parser.parse_args()

    rclpy.init(args=args)

    if args_cmd.role == 'publisher':
        node = PublisherNode()
        role = "Publisher"
    elif args_cmd.role == 'subscriber':
        node = SubscriberNode()
        role = "Subscriber"
    else:
        print("Please specify --role as either 'publisher' or 'subscriber'")
        return

    print(f"Starting {role} node...")
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()