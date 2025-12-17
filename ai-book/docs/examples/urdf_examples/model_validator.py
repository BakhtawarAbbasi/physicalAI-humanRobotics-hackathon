#!/usr/bin/env python3

"""
URDF Model Validator for ROS 2.

This script validates URDF (Unified Robot Description Format) models
to ensure they are properly structured with correct links, joints, and dependencies.
"""

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