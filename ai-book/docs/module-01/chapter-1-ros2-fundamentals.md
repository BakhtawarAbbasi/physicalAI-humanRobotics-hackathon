---
sidebar_position: 1
title: 'Chapter 1 - ROS 2 Fundamentals'
description: 'Learn the core concepts of ROS 2 architecture including nodes, topics, services, and actions'
---

# Chapter 1 - ROS 2 Fundamentals

## Introduction to ROS 2

ROS 2 (Robot Operating System 2) is a flexible framework for writing robot software. It's a collection of tools, libraries, and conventions that aim to simplify the task of creating complex and robust robot behavior across a wide variety of robot platforms.

ROS 2 is designed to support the development of large, distributed systems that can be run across multiple machines. It provides a publish/subscribe messaging system that allows different parts of your robot application to communicate with each other in a decoupled way.

## Core Concepts

### Nodes

A node is a process that performs computation in the ROS 2 system. Nodes are the fundamental building blocks of your robot application. In ROS 2, nodes are written in a variety of languages (C++, Python, etc.) and can run on different machines.

```python
import rclpy
from rclpy.node import Node

class MinimalPublisher(Node):

    def __init__(self):
        super().__init__('minimal_publisher')
        self.publisher_ = self.create_publisher(String, 'topic', 10)
        timer_period = 0.5  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0

    def timer_callback(self):
        msg = String()
        msg.data = 'Hello World: %d' % self.i
        self.publisher_.publish(msg)
        self.get_logger().info('Publishing: "%s"' % msg.data)
        self.i += 1
```

### Topics

Topics are communication channels over which nodes exchange messages using a publish/subscribe pattern. Multiple nodes can publish to the same topic, and multiple nodes can subscribe to the same topic.

The publish/subscribe pattern allows for decoupled communication between nodes. Publishers don't need to know who is subscribing to their messages, and subscribers don't need to know who is publishing messages they receive.

### Services

Services provide a request/response communication pattern. A service client sends a request message to a service server, which processes the request and returns a response.

### Actions

Actions are designed for long-running tasks that require feedback and goal management. They extend the service concept by adding features like goal preemption, feedback during execution, and status reporting.

## Publisher/Subscriber Example

Let's create a simple publisher and subscriber example to demonstrate ROS 2 communication.

### Publisher Node

```python
# publisher_subscriber.py
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

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

def main(args=None):
    rclpy.init(args=args)
    publisher_node = PublisherNode()

    try:
        rclpy.spin(publisher_node)
    except KeyboardInterrupt:
        pass
    finally:
        publisher_node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
```

### Subscriber Node

```python
# publisher_subscriber.py (subscriber part)
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

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
    rclpy.init(args=args)
    subscriber_node = SubscriberNode()

    try:
        rclpy.spin(subscriber_node)
    except KeyboardInterrupt:
        pass
    finally:
        subscriber_node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
```

## Launch Files and Parameter Handling

Launch files allow you to start multiple nodes at once with a single command. They provide a way to configure and manage complex systems with many nodes.

```python
# launch_example.py
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='my_package',
            executable='publisher_node',
            name='publisher',
            parameters=[
                {'param_name': 'param_value'}
            ]
        ),
        Node(
            package='my_package',
            executable='subscriber_node',
            name='subscriber'
        )
    ])
```

## Prerequisites

Before running the examples in this chapter, ensure you have:

1. **ROS 2 Installed**: Install ROS 2 Humble Hawksbill (or later) from https://docs.ros.org/
2. **Python 3.8+**: Required for running Python-based ROS 2 nodes
3. **rclpy**: Python client library for ROS 2 (`pip install rclpy` or install via ROS 2 packages)
4. **Terminal Access**: To run multiple nodes simultaneously

## Running the Examples

To run the publisher and subscriber examples:

1. Open two terminal windows
2. Source your ROS 2 installation in both terminals:
   ```bash
   source /opt/ros/humble/setup.bash  # Adjust for your ROS 2 distribution
   ```
3. Navigate to the examples directory:
   ```bash
   cd ai-book/docs/examples/ros2_basics/
   ```
4. In the first terminal, run the publisher:
   ```bash
   python3 publisher_subscriber.py --role publisher
   ```
5. In the second terminal, run the subscriber:
   ```bash
   python3 publisher_subscriber.py --role subscriber
   ```

The publisher will send messages every 0.5 seconds, and the subscriber will receive and print them.

## Verification

To verify that your ROS 2 setup is working correctly:

1. Check available topics:
   ```bash
   ros2 topic list
   ```
   You should see the `/chatter` topic when the publisher is running.

2. Check the message type:
   ```bash
   ros2 topic type /chatter
   ```
   Should return `std_msgs/msg/String`.

3. Echo messages from the topic:
   ```bash
   ros2 topic echo /chatter std_msgs/msg/String
   ```

## Summary

In this chapter, you learned about the fundamental concepts of ROS 2:

- Nodes: The basic computational elements
- Topics: Communication channels using publish/subscribe
- Services: Request/response communication
- Actions: For long-running tasks with feedback

These concepts form the foundation of all ROS 2 applications and will be essential as you continue to build more complex robot systems.