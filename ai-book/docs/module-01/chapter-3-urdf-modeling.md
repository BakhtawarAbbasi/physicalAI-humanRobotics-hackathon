---
sidebar_position: 3
title: 'Chapter 3 - Humanoid Robot Description with URDF'
description: 'Creating a simple humanoid robot model using URDF structure with links, joints, and sensors'
---

# Chapter 3 - Humanoid Robot Description with URDF

## Introduction to URDF

URDF (Unified Robot Description Format) is an XML-based format used to describe robots in ROS. It defines the robot's physical structure including links (rigid parts), joints (connections between links), and other properties like visual and collision geometry, inertial properties, and sensors.

## URDF Structure

A URDF file typically contains:

- **Links**: Rigid parts of the robot (e.g., base, arms, head)
- **Joints**: Connections between links (e.g., revolute, prismatic, fixed)
- **Visual**: How the robot appears in simulation
- **Collision**: How the robot interacts with the environment
- **Inertial**: Mass and inertia properties for physics simulation

## Creating a Simple Humanoid Robot

Let's create a basic humanoid robot model with a torso, head, arms, and legs.

### Basic Humanoid URDF Model

```xml
<!-- simple_humanoid.urdf -->
<?xml version="1.0"?>
<robot name="simple_humanoid">
  <!-- Base link -->
  <link name="base_link">
    <visual>
      <geometry>
        <box size="0.3 0.2 0.4"/>
      </geometry>
      <material name="blue">
        <color rgba="0 0 1 0.8"/>
      </material>
    </visual>
    <collision>
      <geometry>
        <box size="0.3 0.2 0.4"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="5.0"/>
      <inertia ixx="0.1" ixy="0.0" ixz="0.0" iyy="0.1" iyz="0.0" izz="0.1"/>
    </inertial>
  </link>

  <!-- Head -->
  <link name="head">
    <visual>
      <geometry>
        <sphere radius="0.1"/>
      </geometry>
      <material name="white">
        <color rgba="1 1 1 0.8"/>
      </material>
    </visual>
    <collision>
      <geometry>
        <sphere radius="0.1"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="1.0"/>
      <inertia ixx="0.001" ixy="0.0" ixz="0.0" iyy="0.001" iyz="0.0" izz="0.001"/>
    </inertial>
  </link>

  <joint name="head_joint" type="fixed">
    <parent link="base_link"/>
    <child link="head"/>
    <origin xyz="0 0 0.3" rpy="0 0 0"/>
  </joint>

  <!-- Left Arm -->
  <link name="left_upper_arm">
    <visual>
      <geometry>
        <cylinder length="0.3" radius="0.05"/>
      </geometry>
      <material name="gray">
        <color rgba="0.5 0.5 0.5 0.8"/>
      </material>
    </visual>
    <collision>
      <geometry>
        <cylinder length="0.3" radius="0.05"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="0.5"/>
      <inertia ixx="0.001" ixy="0.0" ixz="0.0" iyy="0.001" iyz="0.0" izz="0.001"/>
    </inertial>
  </link>

  <joint name="left_shoulder_joint" type="revolute">
    <parent link="base_link"/>
    <child link="left_upper_arm"/>
    <origin xyz="0.2 0 0.1" rpy="0 0 0"/>
    <axis xyz="0 1 0"/>
    <limit lower="-1.57" upper="1.57" effort="100" velocity="1"/>
  </joint>

  <link name="left_lower_arm">
    <visual>
      <geometry>
        <cylinder length="0.25" radius="0.04"/>
      </geometry>
      <material name="gray">
        <color rgba="0.5 0.5 0.5 0.8"/>
      </material>
    </visual>
    <collision>
      <geometry>
        <cylinder length="0.25" radius="0.04"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="0.3"/>
      <inertia ixx="0.001" ixy="0.0" ixz="0.0" iyy="0.001" iyz="0.0" izz="0.001"/>
    </inertial>
  </link>

  <joint name="left_elbow_joint" type="revolute">
    <parent link="left_upper_arm"/>
    <child link="left_lower_arm"/>
    <origin xyz="0 0 -0.25" rpy="0 0 0"/>
    <axis xyz="0 1 0"/>
    <limit lower="-1.57" upper="1.57" effort="100" velocity="1"/>
  </joint>

  <!-- Right Arm -->
  <link name="right_upper_arm">
    <visual>
      <geometry>
        <cylinder length="0.3" radius="0.05"/>
      </geometry>
      <material name="gray">
        <color rgba="0.5 0.5 0.5 0.8"/>
      </material>
    </visual>
    <collision>
      <geometry>
        <cylinder length="0.3" radius="0.05"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="0.5"/>
      <inertia ixx="0.001" ixy="0.0" ixz="0.0" iyy="0.001" iyz="0.0" izz="0.001"/>
    </inertial>
  </link>

  <joint name="right_shoulder_joint" type="revolute">
    <parent link="base_link"/>
    <child link="right_upper_arm"/>
    <origin xyz="-0.2 0 0.1" rpy="0 0 0"/>
    <axis xyz="0 1 0"/>
    <limit lower="-1.57" upper="1.57" effort="100" velocity="1"/>
  </joint>

  <link name="right_lower_arm">
    <visual>
      <geometry>
        <cylinder length="0.25" radius="0.04"/>
      </geometry>
      <material name="gray">
        <color rgba="0.5 0.5 0.5 0.8"/>
      </material>
    </visual>
    <collision>
      <geometry>
        <cylinder length="0.25" radius="0.04"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="0.3"/>
      <inertia ixx="0.001" ixy="0.0" ixz="0.0" iyy="0.001" iyz="0.0" izz="0.001"/>
    </inertial>
  </link>

  <joint name="right_elbow_joint" type="revolute">
    <parent link="right_upper_arm"/>
    <child link="right_lower_arm"/>
    <origin xyz="0 0 -0.25" rpy="0 0 0"/>
    <axis xyz="0 1 0"/>
    <limit lower="-1.57" upper="1.57" effort="100" velocity="1"/>
  </joint>

  <!-- Left Leg -->
  <link name="left_upper_leg">
    <visual>
      <geometry>
        <cylinder length="0.4" radius="0.06"/>
      </geometry>
      <material name="gray">
        <color rgba="0.5 0.5 0.5 0.8"/>
      </material>
    </visual>
    <collision>
      <geometry>
        <cylinder length="0.4" radius="0.06"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="0.8"/>
      <inertia ixx="0.001" ixy="0.0" ixz="0.0" iyy="0.001" iyz="0.0" izz="0.001"/>
    </inertial>
  </link>

  <joint name="left_hip_joint" type="revolute">
    <parent link="base_link"/>
    <child link="left_upper_leg"/>
    <origin xyz="0.1 0 -0.2" rpy="0 0 0"/>
    <axis xyz="0 1 0"/>
    <limit lower="-1.57" upper="1.57" effort="100" velocity="1"/>
  </joint>

  <link name="left_lower_leg">
    <visual>
      <geometry>
        <cylinder length="0.35" radius="0.05"/>
      </geometry>
      <material name="gray">
        <color rgba="0.5 0.5 0.5 0.8"/>
      </material>
    </visual>
    <collision>
      <geometry>
        <cylinder length="0.35" radius="0.05"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="0.6"/>
      <inertia ixx="0.001" ixy="0.0" ixz="0.0" iyy="0.001" iyz="0.0" izz="0.001"/>
    </inertial>
  </link>

  <joint name="left_knee_joint" type="revolute">
    <parent link="left_upper_leg"/>
    <child link="left_lower_leg"/>
    <origin xyz="0 0 -0.35" rpy="0 0 0"/>
    <axis xyz="0 1 0"/>
    <limit lower="-1.57" upper="1.57" effort="100" velocity="1"/>
  </joint>

  <!-- Right Leg -->
  <link name="right_upper_leg">
    <visual>
      <geometry>
        <cylinder length="0.4" radius="0.06"/>
      </geometry>
      <material name="gray">
        <color rgba="0.5 0.5 0.5 0.8"/>
      </material>
    </visual>
    <collision>
      <geometry>
        <cylinder length="0.4" radius="0.06"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="0.8"/>
      <inertia ixx="0.001" ixy="0.0" ixz="0.0" iyy="0.001" iyz="0.0" izz="0.001"/>
    </inertial>
  </link>

  <joint name="right_hip_joint" type="revolute">
    <parent link="base_link"/>
    <child link="right_upper_leg"/>
    <origin xyz="-0.1 0 -0.2" rpy="0 0 0"/>
    <axis xyz="0 1 0"/>
    <limit lower="-1.57" upper="1.57" effort="100" velocity="1"/>
  </joint>

  <link name="right_lower_leg">
    <visual>
      <geometry>
        <cylinder length="0.35" radius="0.05"/>
      </geometry>
      <material name="gray">
        <color rgba="0.5 0.5 0.5 0.8"/>
      </material>
    </visual>
    <collision>
      <geometry>
        <cylinder length="0.35" radius="0.05"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="0.6"/>
      <inertia ixx="0.001" ixy="0.0" ixz="0.0" iyy="0.001" iyz="0.0" izz="0.001"/>
    </inertial>
  </link>

  <joint name="right_knee_joint" type="revolute">
    <parent link="right_upper_leg"/>
    <child link="right_lower_leg"/>
    <origin xyz="0 0 -0.35" rpy="0 0 0"/>
    <axis xyz="0 1 0"/>
    <limit lower="-1.57" upper="1.57" effort="100" velocity="1"/>
  </joint>
</robot>
```

## URDF Components Explained

### Links

Links represent rigid bodies in the robot. Each link has:

- **Visual**: Defines how the link appears in visualization
- **Collision**: Defines the collision boundaries for physics simulation
- **Inertial**: Defines mass and inertia properties for physics simulation

### Joints

Joints connect links and define how they can move relative to each other:

- **Fixed**: No movement allowed (like welding parts together)
- **Revolute**: Rotational movement around a single axis
- **Prismatic**: Linear sliding movement along a single axis
- **Continuous**: Like revolute but with unlimited rotation
- **Floating**: 6 degrees of freedom (rarely used)

## Validating URDF Models

Let's create a Python script to validate URDF models:

### URDF Model Validator

```python
# model_validator.py
import xml.etree.ElementTree as ET
import sys
from pathlib import Path


class URDFValidator:
    def __init__(self, urdf_file_path):
        self.urdf_file_path = Path(urdf_file_path)
        self.tree = None
        self.root = None

    def load_urdf(self):
        """Load and parse the URDF file"""
        try:
            self.tree = ET.parse(self.urdf_file_path)
            self.root = self.tree.getroot()
            return True
        except ET.ParseError as e:
            print(f"Error parsing URDF file: {e}")
            return False
        except FileNotFoundError:
            print(f"URDF file not found: {self.urdf_file_path}")
            return False

    def validate_basic_structure(self):
        """Validate basic URDF structure"""
        if self.root.tag != 'robot':
            print("Error: Root element must be 'robot'")
            return False

        robot_name = self.root.get('name')
        if not robot_name:
            print("Error: Robot must have a name attribute")
            return False

        print(f"✓ Robot name: {robot_name}")
        return True

    def validate_links(self):
        """Validate that all links have required properties"""
        links = self.root.findall('link')
        if not links:
            print("Warning: No links found in URDF")
            return False

        link_names = set()
        for link in links:
            name = link.get('name')
            if not name:
                print("Error: Link missing name attribute")
                return False

            if name in link_names:
                print(f"Error: Duplicate link name found: {name}")
                return False

            link_names.add(name)

            # Check for visual and collision elements
            visual = link.find('visual')
            collision = link.find('collision')
            inertial = link.find('inertial')

            if visual is None:
                print(f"Warning: Link '{name}' has no visual element")

            if collision is None:
                print(f"Warning: Link '{name}' has no collision element")

            if inertial is None:
                print(f"Warning: Link '{name}' has no inertial element")

        print(f"✓ Found {len(links)} links: {', '.join(link_names)}")
        return True

    def validate_joints(self):
        """Validate that all joints connect existing links"""
        joints = self.root.findall('joint')
        if not joints:
            print("Warning: No joints found in URDF")
            return True  # Joints are not always required

        links = {link.get('name') for link in self.root.findall('link')}
        joint_names = set()

        for joint in joints:
            name = joint.get('name')
            if not name:
                print("Error: Joint missing name attribute")
                return False

            if name in joint_names:
                print(f"Error: Duplicate joint name found: {name}")
                return False

            joint_names.add(name)

            joint_type = joint.get('type')
            if not joint_type:
                print(f"Error: Joint '{name}' missing type attribute")
                return False

            parent = joint.find('parent')
            child = joint.find('child')

            if parent is None or child is None:
                print(f"Error: Joint '{name}' missing parent or child element")
                return False

            parent_link = parent.get('link')
            child_link = child.get('link')

            if parent_link not in links:
                print(f"Error: Joint '{name}' references non-existent parent link: {parent_link}")
                return False

            if child_link not in links:
                print(f"Error: Joint '{name}' references non-existent child link: {child_link}")
                return False

            if parent_link == child_link:
                print(f"Error: Joint '{name}' connects link to itself: {parent_link}")
                return False

        print(f"✓ Found {len(joints)} joints")
        return True

    def validate_model(self):
        """Run all validations on the URDF model"""
        print(f"Validating URDF model: {self.urdf_file_path}")
        print("-" * 40)

        if not self.load_urdf():
            return False

        success = True
        success &= self.validate_basic_structure()
        success &= self.validate_links()
        success &= self.validate_joints()

        if success:
            print("-" * 40)
            print("✓ URDF model validation PASSED")
        else:
            print("-" * 40)
            print("✗ URDF model validation FAILED")

        return success


def main():
    if len(sys.argv) != 2:
        print("Usage: python model_validator.py <urdf_file_path>")
        sys.exit(1)

    urdf_file = sys.argv[1]
    validator = URDFValidator(urdf_file)
    success = validator.validate_model()

    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
```

## Loading and Visualizing URDF in Simulation

To load and visualize your URDF model in a simulation environment:

1. **RViz**: Use RViz to visualize the robot model
2. **Gazebo**: Use Gazebo for physics simulation
3. **URDF Viewer**: Use standalone URDF viewers for quick checks

## Prerequisites

Before working with URDF models:

1. **XML Parser**: Python's built-in `xml.etree.ElementTree` module
2. **Robot Simulation Environment**: Gazebo or RViz for visualization
3. **URDF Support**: ROS packages for URDF processing

## Running the Validation Example

To validate a URDF model:

1. Save your URDF model to a file (e.g., `simple_humanoid.urdf`)
2. Run the validator:
   ```bash
   cd ai-book/docs/examples/urdf_examples/
   python3 model_validator.py simple_humanoid.urdf
   ```

## Verification

To verify that your URDF model is properly structured:

1. Check that the XML is well-formed
2. Ensure all links have unique names
3. Verify that joints connect existing links
4. Confirm that visual, collision, and inertial elements are properly defined

## Summary

In this chapter, you learned how to:

- Create a humanoid robot model using URDF format
- Define links with visual, collision, and inertial properties
- Create joints to connect links with specific movement constraints
- Validate URDF models using Python scripts
- Structure a complete humanoid robot with torso, head, arms, and legs

URDF is essential for robot simulation and provides the foundation for robot control and visualization in ROS-based systems.