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