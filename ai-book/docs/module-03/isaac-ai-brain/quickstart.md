---
title: Quickstart Guide
sidebar_position: 0
---

# Isaac AI Brain Module Quickstart Guide

This guide provides a quick introduction to the Isaac AI Brain module, covering Isaac Sim, Isaac ROS perception, and Nav2 navigation for humanoid robots.

## Prerequisites

Before starting with the Isaac AI Brain module, ensure you have:

### System Requirements
- NVIDIA GPU with RTX support (RTX 3080 or better recommended)
- 16GB+ RAM
- 100GB+ free disk space
- Ubuntu 20.04 LTS or Windows 10/11 with WSL2

### Software Requirements
- ROS 2 (Humble Hawksbill or later)
- Isaac Sim installed and licensed
- Isaac ROS packages
- Docker and NVIDIA Container Toolkit
- Git and basic development tools

### Knowledge Requirements
- Familiarity with ROS 2 concepts and tools
- Basic understanding of robot simulation
- Experience with command-line tools

## Getting Started

### 1. Isaac Sim & Synthetic Data (Chapter 1)

Start with the Isaac Sim chapter to learn about photorealistic simulation and synthetic data generation:

1. **Install Isaac Sim**:
   ```bash
   # Pull the Isaac Sim Docker image
   docker pull nvcr.io/nvidia/isaac-sim:latest

   # Run Isaac Sim container with GPU support
   docker run --gpus all -it --rm \
     --network=host \
     --env "ACCEPT_EULA=Y" \
     --env "NVIDIA_VISIBLE_DEVICES=all" \
     --env "NVIDIA_DRIVER_CAPABILITIES=all" \
     --volume $HOME/isaac-sim-cache:/isaac-sim-cache \
     --volume $HOME/isaac-sim-outputs:/isaac-sim-outputs \
     nvcr.io/nvidia/isaac-sim:latest
   ```

2. **Create your first simulation environment**:
   - Launch Isaac Sim
   - Create a new scene with a simple robot model
   - Add a camera sensor to the robot
   - Configure physics properties
   - Run a basic simulation to verify setup

3. **Generate synthetic datasets**:
   - Set up an environment with multiple objects
   - Configure a camera with realistic parameters
   - Enable semantic segmentation rendering
   - Generate a dataset with 100 annotated images
   - Export the dataset in COCO format

### 2. Isaac ROS Perception (Chapter 2)

Move on to Isaac ROS perception pipelines:

1. **Install Isaac ROS packages**:
   ```bash
   # Install Isaac ROS common packages
   sudo apt install ros-humble-isaac-ros-common

   # Install specific perception packages
   sudo apt install ros-humble-isaac-ros-visual-slam
   sudo apt install ros-humble-isaac-ros-compressed-image-transport
   sudo apt install ros-humble-isaac-ros-stereo-image-pipeline
   ```

2. **Set up VSLAM pipeline**:
   - Configure stereo camera setup in Isaac Sim
   - Configure the VSLAM pipeline with appropriate parameters
   - Launch the VSLAM node
   - Visualize the resulting map and trajectory

3. **Optimize performance**:
   - Apply hardware acceleration optimizations
   - Monitor performance metrics
   - Fine-tune parameters for your specific use case

### 3. Nav2 for Humanoid Navigation (Chapter 3)

Finally, configure Nav2 for humanoid robot navigation:

1. **Install Nav2 packages**:
   ```bash
   # Install Nav2 packages
   sudo apt install ros-humble-navigation2 ros-humble-nav2-bringup
   sudo apt install ros-humble-nav2-gui-tools
   ```

2. **Configure humanoid-specific parameters**:
   - Set up costmap parameters for bipedal locomotion
   - Configure path planning algorithms for humanoid constraints
   - Adjust controller parameters for stable movement
   - Test navigation in simulation

3. **Run practical exercises**:
   - Execute basic navigation tasks
   - Fine-tune parameters based on performance
   - Integrate with Isaac ROS perception systems

## Quick Validation

To confirm everything is working correctly:

1. **Environment Check**: Verify Isaac Sim launches without errors
2. **ROS Integration**: Confirm Isaac ROS packages are discoverable
3. **Example Validation**: Run provided examples and verify expected output
4. **Navigation Test**: Execute a simple navigation task with Nav2

## Troubleshooting

### Common Issues
- **GPU Memory**: Ensure sufficient VRAM for Isaac Sim (8GB+ recommended)
- **Permissions**: Check Docker permissions for Isaac containers
- **ROS Environment**: Verify ROS 2 environment is properly sourced

## Next Steps

After completing this quickstart guide, continue with the detailed chapters:

- [Isaac Sim & Synthetic Data](./isaac-sim) - Comprehensive simulation and data generation
- [Isaac ROS Perception](./isaac-ros) - Hardware-accelerated perception pipelines
- [Nav2 for Humanoid Navigation](./nav2-navigation) - Path planning and navigation