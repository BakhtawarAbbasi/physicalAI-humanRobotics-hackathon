"""Launch file example for ROS 2.

This launch file demonstrates how to start multiple nodes with a single command.
"""

from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
        Node(
            package='demo_nodes_py',
            executable='talker',
            name='publisher_node',
            parameters=[
                # Add parameters here if needed
            ]
        ),
        Node(
            package='demo_nodes_py',
            executable='listener',
            name='subscriber_node'
        )
    ])