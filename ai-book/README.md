# AI/Spec-Driven Technical Book

This website is built using [Docusaurus](https://docusaurus.io/), a modern static website generator. This repository contains an AI/Spec-Driven Technical Book with integrated RAG chatbot, focusing on Physical AI and humanoid robotics.

## Module 1 - The Robotic Nervous System (ROS 2)

This module introduces ROS 2 as the middleware (robotic nervous system) for humanoid robots, enabling students to control simulated robots and bridge AI agents to physical actions.

### Chapters

1. **ROS 2 Fundamentals** - Learn the core concepts of ROS 2 architecture including nodes, topics, services, and actions
2. **Bridging Python Agents to ROS Controllers** - Connect Python AI agents to ROS 2 using rclpy to create an end-to-end pipeline
3. **Humanoid Robot Description with URDF** - Create a simple humanoid robot model using URDF structure with links, joints, and sensors

### Prerequisites

- ROS 2 Humble Hawksbill (or later) installed
- Python 3.8+ with rclpy library
- Node.js for Docusaurus documentation

### Running Examples

The examples are located in the `docs/examples/` directory and can be run with appropriate ROS 2 setup.

## Module 2 - The Digital Twin (Gazebo & Unity)

This module provides comprehensive documentation and examples for creating a digital twin system using Gazebo physics simulation and Unity visualization. The digital twin enables realistic robotics simulation with physics-based interactions and real-time 3D visualization.

### Chapters

1. **Gazebo Physics Simulation** - Learn about physics-based simulation with gravity, collisions, and joints for humanoid robots
2. **Sensor Simulation** - Configure simulated sensors (LiDAR, cameras, IMUs) that publish realistic ROS 2 data based on the robot's position and environment
3. **Unity Digital Twin** - Visualize the simulated robot state in real-time using Unity, creating a digital twin that mirrors the Gazebo simulation

### Prerequisites

- ROS 2 Humble Hawksbill
- Gazebo Garden or compatible version
- Unity 2022.3 LTS
- Python 3.8+ for bridge scripts

### Running Examples

The examples are located in the `docs/examples/` directory under the `gazebo_configs/`, `sensor_configs/`, and `unity_integration/` subdirectories.

## Installation

```bash
yarn
```

## Local Development

```bash
yarn start
```

This command starts a local development server and opens up a browser window. Most changes are reflected live without having to restart the server.

## Build

```bash
yarn build
```

This command generates static content into the `build` directory and can be served using any static contents hosting service.

## Deployment

Using SSH:

```bash
USE_SSH=true yarn deploy
```

Not using SSH:

```bash
GIT_USER=<Your GitHub username> yarn deploy
```

If you are using GitHub pages for hosting, this command is a convenient way to build the website and push to the `gh-pages` branch.

## Contributing

This project follows spec-driven development principles. All changes should be aligned with the project specifications before implementation.
