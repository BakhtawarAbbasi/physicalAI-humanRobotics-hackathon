# Quickstart Guide: Module 1 — The Robotic Nervous System (ROS 2)

## Prerequisites

1. **Node.js**: Version 18.x or higher
2. **Python**: Version 3.8 or higher
3. **ROS 2**: Humble Hawksbill (or compatible version) installed
4. **Git**: For version control

## Setup Instructions

### 1. Clone and Initialize the Repository

```bash
git clone [repository-url]
cd [repository-name]
npm install
```

### 2. Install ROS 2 Dependencies

```bash
# Verify ROS 2 installation
source /opt/ros/humble/setup.bash  # Adjust for your ROS 2 distribution
ros2 --version
```

### 3. Install Python Dependencies

```bash
pip3 install rclpy
pip3 install rosgraph
```

### 4. Start the Documentation Server

```bash
npm start
```

The documentation will be available at `http://localhost:3000`.

## Running Examples

### Chapter 1: ROS 2 Fundamentals

1. Navigate to the examples directory:
```bash
cd docs/examples/ros2_basics/
```

2. Run the publisher example:
```bash
python3 publisher_subscriber.py --role publisher
```

3. In a separate terminal, run the subscriber:
```bash
python3 publisher_subscriber.py --role subscriber
```

### Chapter 2: Agent-to-ROS Bridge

1. Navigate to the agent examples:
```bash
cd docs/examples/agent_bridge/
```

2. Run the agent node:
```bash
python3 agent_node.py
```

3. Test command validation:
```bash
python3 command_validator.py
```

### Chapter 3: URDF Modeling

1. Navigate to the URDF examples:
```bash
cd docs/examples/urdf_examples/
```

2. Validate the humanoid model:
```bash
python3 model_validator.py simple_humanoid.urdf
```

## Building for Production

```bash
npm run build
```

The static site will be generated in the `build/` directory and can be deployed to GitHub Pages.

## Troubleshooting

- **ROS 2 not found**: Ensure ROS 2 environment is sourced (`source /opt/ros/humble/setup.bash`)
- **Python packages missing**: Install with `pip3 install rclpy`
- **Docusaurus build errors**: Check Node.js version compatibility
- **Examples not running**: Verify Python version and ROS 2 installation