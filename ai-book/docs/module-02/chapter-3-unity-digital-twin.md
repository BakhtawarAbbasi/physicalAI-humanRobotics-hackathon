---
sidebar_position: 3
title: 'Chapter 3 - Unity Digital Twin'
description: 'Learn about visualizing simulated robot state in real-time using Unity to create a digital twin that mirrors the Gazebo simulation'
---

# Chapter 3 - Unity Digital Twin

## Introduction to Unity Digital Twin

A digital twin is a virtual replica of a physical system that enables real-time monitoring, analysis, and visualization. In robotics, a digital twin provides a visual representation of the robot's state in the simulation environment, allowing developers to observe robot behavior, debug issues, and validate control algorithms. Unity, with its powerful 3D rendering capabilities and real-time performance, serves as an excellent platform for creating digital twins of robotic systems.

## Unity Digital Twin Architecture

### System Overview
The Unity digital twin system consists of three main components:

1. **Gazebo Simulation**: Provides physics-based simulation and sensor data
2. **ROS 2 Bridge**: Facilitates communication between Gazebo and Unity
3. **Unity Visualization**: Real-time 3D visualization of robot state

### Data Flow Architecture
```
Gazebo Simulation → ROS 2 Topics → Bridge → Unity → 3D Visualization
     ↑                                    ↓
Real-world Physics ← Unity Commands ← Bridge ← 3D Interaction
```

## Setting Up Unity for Robotics

### Prerequisites
1. Unity 2022.3 LTS or later
2. Unity Robotics Package (URP)
3. ROS 2 Humble Hawksbill
4. ROS# Unity package or custom bridge implementation
5. .NET Framework 4.x compatibility

### Installation Steps
1. Download and install Unity Hub
2. Install Unity 2022.3 LTS through Unity Hub
3. Create a new 3D project
4. Import the Unity Robotics Package from the Unity Asset Store or Package Manager
5. Install ROS# or similar ROS 2 bridge package

### Unity Project Structure
For a robotics digital twin project, organize your Unity project as follows:

```
Assets/
├── Scripts/
│   ├── ROSBridge/
│   ├── RobotControllers/
│   ├── Visualization/
│   └── Utilities/
├── Models/
│   ├── Robot/
│   ├── Environment/
│   └── Sensors/
├── Materials/
├── Scenes/
└── Prefabs/
```

## Creating Robot Models in Unity

### Importing Robot Models
Unity can import robot models in various formats:

- **FBX**: Most common format for 3D models
- **OBJ**: Simple geometry format
- **STL**: Common for CAD models
- **URDF**: Can be converted to Unity format

### Robot Model Structure
When importing a robot model, ensure the hierarchy reflects the URDF structure:

```
Robot (Root)
├── BaseLink
├── Link1
│   └── Joint1
├── Link2
│   └── Joint2
└── Sensors
    ├── Camera
    ├── LiDAR
    └── IMU
```

### Joint Configuration
Configure Unity joints to match the physical constraints of your robot:

```csharp
// Example Unity joint configuration
public class RobotJoint : MonoBehaviour
{
    public ConfigurableJoint joint;
    public float minAngle = -90f;
    public float maxAngle = 90f;
    public float maxForce = 1000f;

    void Start()
    {
        ConfigureJoint();
    }

    void ConfigureJoint()
    {
        // Set joint limits
        joint.lowAngularXLimit = minAngle * Mathf.Deg2Rad;
        joint.highAngularXLimit = maxAngle * Mathf.Deg2Rad;

        // Set motor properties
        joint.angularXDrive = new JointDrive
        {
            positionSpring = 1000f,
            positionDamper = 100f,
            maximumForce = maxForce
        };
    }

    public void SetTargetRotation(float angle)
    {
        joint.targetRotation = Quaternion.AngleAxis(angle, Vector3.right);
    }
}
```

## ROS 2 Integration

### Setting Up the ROS Bridge
The ROS bridge enables communication between ROS 2 nodes and Unity:

```csharp
// Example ROS bridge setup
using ROS2;
using UnityEngine;

public class ROSBridgeManager : MonoBehaviour
{
    private ROS2UnityComponent ros2Unity;
    private bool rosConnected = false;

    void Start()
    {
        ros2Unity = GetComponent<ROS2UnityComponent>();
        ros2Unity.Initialize();
    }

    void Update()
    {
        if (ros2Unity.Ok())
        {
            if (!rosConnected)
            {
                rosConnected = true;
                SetupSubscribers();
            }
        }
    }

    void SetupSubscribers()
    {
        // Subscribe to robot state topics
        ros2Unity.CreateSubscription<JointState>("/joint_states", JointStateCallback);
        ros2Unity.CreateSubscription<Odometry>("/odom", OdometryCallback);

        // Subscribe to sensor topics
        ros2Unity.CreateSubscription<LaserScan>("/lidar/scan", LaserScanCallback);
    }

    void JointStateCallback(JointState msg)
    {
        // Process joint state message and update Unity models
        UpdateRobotJoints(msg);
    }

    void OdometryCallback(Odometry msg)
    {
        // Process odometry message and update robot position
        UpdateRobotPosition(msg);
    }

    void LaserScanCallback(LaserScan msg)
    {
        // Process laser scan data for visualization
        UpdateLidarVisualization(msg);
    }
}
```

### Joint State Synchronization
Synchronize robot joint states between Gazebo and Unity:

```csharp
// Joint state processing
public class JointStateProcessor : MonoBehaviour
{
    public Dictionary<string, Transform> jointMap = new Dictionary<string, Transform>();

    public void UpdateRobotJoints(JointState jointState)
    {
        for (int i = 0; i < jointState.name.Count; i++)
        {
            string jointName = jointState.name[i];
            if (jointMap.ContainsKey(jointName))
            {
                Transform jointTransform = jointMap[jointName];
                float jointAngle = (float)jointState.position[i];

                // Apply rotation based on joint type
                jointTransform.localRotation = Quaternion.Euler(0, 0, jointAngle * Mathf.Rad2Deg);
            }
        }
    }

    public void InitializeJointMap()
    {
        // Map joint names to transforms in the Unity scene
        Transform[] allChildren = GetComponentsInChildren<Transform>();
        foreach (Transform child in allChildren)
        {
            if (child.name.StartsWith("joint_"))
            {
                jointMap[child.name] = child;
            }
        }
    }
}
```

## Real-time Synchronization

### Transform Synchronization
Synchronize transforms between ROS 2 and Unity in real-time:

```csharp
// Transform synchronization
public class TransformSynchronizer : MonoBehaviour
{
    public string tfFrameName = "base_link";
    private ROS2UnityComponent ros2Unity;
    private TransformStamped currentTransform;

    void Start()
    {
        ros2Unity = GetComponent<ROS2UnityComponent>();
    }

    void Update()
    {
        if (currentTransform != null)
        {
            // Update Unity transform from ROS transform
            transform.position = new Vector3(
                (float)currentTransform.transform.translation.x,
                (float)currentTransform.transform.translation.z, // Note: Unity Y-up vs ROS Z-up
                (float)currentTransform.transform.translation.y
            );

            transform.rotation = new Quaternion(
                (float)currentTransform.transform.rotation.x,
                (float)currentTransform.transform.rotation.z,
                (float)currentTransform.transform.rotation.y,
                (float)currentTransform.transform.rotation.w
            );
        }
    }

    public void UpdateTransform(TransformStamped newTransform)
    {
        currentTransform = newTransform;
    }
}
```

### Sensor Data Visualization
Visualize sensor data in Unity:

```csharp
// LiDAR visualization
public class LidarVisualizer : MonoBehaviour
{
    public LineRenderer lineRenderer;
    public int maxPoints = 1000;
    private List<Vector3> lidarPoints = new List<Vector3>();

    void Start()
    {
        if (lineRenderer == null)
        {
            lineRenderer = gameObject.AddComponent<LineRenderer>();
            lineRenderer.positionCount = maxPoints;
            lineRenderer.startWidth = 0.01f;
            lineRenderer.endWidth = 0.01f;
        }
    }

    public void UpdateLidarVisualization(LaserScan scan)
    {
        lidarPoints.Clear();

        for (int i = 0; i < scan.ranges.Count; i++)
        {
            float angle = (float)(scan.angle_min + i * scan.angle_increment);
            float distance = (float)scan.ranges[i];

            if (distance >= scan.range_min && distance <= scan.range_max)
            {
                Vector3 point = new Vector3(
                    distance * Mathf.Cos(angle),
                    0.1f, // Height above ground
                    distance * Mathf.Sin(angle)
                );

                lidarPoints.Add(point);
            }
        }

        UpdateLineRenderer();
    }

    void UpdateLineRenderer()
    {
        for (int i = 0; i < lidarPoints.Count && i < maxPoints; i++)
        {
            lineRenderer.SetPosition(i, lidarPoints[i]);
        }

        lineRenderer.positionCount = lidarPoints.Count;
    }
}
```

## Practical Example: Unity Digital Twin Implementation

### Complete Unity Scene Setup
Let's create a complete Unity scene for the digital twin:

1. **Create Robot Prefab**: Import your robot model as a prefab
2. **Add ROS Bridge Component**: Attach the ROS bridge to a GameObject
3. **Configure Subscribers**: Set up topic subscriptions for robot state
4. **Add Visualization Elements**: Create visualizers for sensors

### Unity Digital Twin Script
```csharp
// Complete Unity digital twin controller
using ROS2;
using UnityEngine;
using System.Collections.Generic;

public class UnityDigitalTwin : MonoBehaviour
{
    [Header("Robot Configuration")]
    public GameObject robotPrefab;
    public string robotNamespace = "humanoid_robot";

    [Header("ROS Configuration")]
    public string rosMasterUri = "http://localhost:11311";
    public float updateRate = 30f; // Hz

    private GameObject robotInstance;
    private ROS2UnityComponent ros2Unity;
    private JointStateProcessor jointProcessor;
    private TransformSynchronizer transformSync;
    private LidarVisualizer lidarVisualizer;

    void Start()
    {
        InitializeROS();
        SpawnRobot();
        SetupSubscriptions();
    }

    void InitializeROS()
    {
        ros2Unity = GetComponent<ROS2UnityComponent>();
        ros2Unity.Initialize();
    }

    void SpawnRobot()
    {
        robotInstance = Instantiate(robotPrefab, Vector3.zero, Quaternion.identity);

        // Get components from robot instance
        jointProcessor = robotInstance.GetComponent<JointStateProcessor>();
        transformSync = robotInstance.GetComponent<TransformSynchronizer>();

        // Initialize joint mapping
        jointProcessor.InitializeJointMap();
    }

    void SetupSubscriptions()
    {
        InvokeRepeating("SubscribeToTopics", 1f, 1f / updateRate);
    }

    void SubscribeToTopics()
    {
        if (ros2Unity.Ok())
        {
            // Subscribe to joint states
            var jointSub = ros2Unity.CreateSubscription<JointState>($"{robotNamespace}/joint_states", JointStateCallback);

            // Subscribe to odometry
            var odomSub = ros2Unity.CreateSubscription<Odometry>($"{robotNamespace}/odom", OdometryCallback);

            // Subscribe to LiDAR data
            var lidarSub = ros2Unity.CreateSubscription<LaserScan>($"{robotNamespace}/lidar/scan", LaserScanCallback);
        }
    }

    void JointStateCallback(JointState msg)
    {
        if (jointProcessor != null)
        {
            jointProcessor.UpdateRobotJoints(msg);
        }
    }

    void OdometryCallback(Odometry msg)
    {
        if (transformSync != null)
        {
            // Update robot position and orientation from odometry
            Vector3 position = new Vector3(
                (float)msg.pose.pose.position.x,
                (float)msg.pose.pose.position.z,
                (float)msg.pose.pose.position.y
            );

            Quaternion rotation = new Quaternion(
                (float)msg.pose.pose.orientation.x,
                (float)msg.pose.pose.orientation.z,
                (float)msg.pose.pose.orientation.y,
                (float)msg.pose.pose.orientation.w
            );

            transformSync.transform.position = position;
            transformSync.transform.rotation = rotation;
        }
    }

    void LaserScanCallback(LaserScan msg)
    {
        if (lidarVisualizer != null)
        {
            lidarVisualizer.UpdateLidarVisualization(msg);
        }
    }

    void OnDestroy()
    {
        if (ros2Unity != null)
        {
            ros2Unity.Shutdown();
        }
    }
}
```

## Unity-ROS Bridge Implementation

### Bridge Configuration
Create a bridge configuration file to define topic mappings:

```json
// bridge_config.json
{
  "bridges": [
    {
      "type": "publisher",
      "ros_type_name": "sensor_msgs/msg/JointState",
      "unity_topic_name": "/joint_states",
      "qos": {
        "history": "keep_last",
        "depth": 10,
        "reliability": "reliable",
        "durability": "volatile"
      }
    },
    {
      "type": "publisher",
      "ros_type_name": "nav_msgs/msg/Odometry",
      "unity_topic_name": "/odom",
      "qos": {
        "history": "keep_last",
        "depth": 10,
        "reliability": "reliable",
        "durability": "volatile"
      }
    },
    {
      "type": "publisher",
      "ros_type_name": "sensor_msgs/msg/LaserScan",
      "unity_topic_name": "/lidar/scan",
      "qos": {
        "history": "keep_last",
        "depth": 10,
        "reliability": "reliable",
        "durability": "volatile"
      }
    }
  ]
}
```

### Bridge Script Implementation
```python
# ros2_unity_bridge.py
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
from nav_msgs.msg import Odometry
from sensor_msgs.msg import LaserScan
import json
import asyncio
import websockets

class ROS2UnityBridge(Node):
    def __init__(self):
        super().__init__('unity_bridge')

        # Create subscribers for robot data
        self.joint_state_sub = self.create_subscription(
            JointState,
            '/joint_states',
            self.joint_state_callback,
            10
        )

        self.odom_sub = self.create_subscription(
            Odometry,
            '/odom',
            self.odom_callback,
            10
        )

        self.lidar_sub = self.create_subscription(
            LaserScan,
            '/lidar/scan',
            self.lidar_callback,
            10
        )

        # WebSocket server for Unity communication
        self.websocket_server = None
        self.connected_clients = set()

        # Start WebSocket server
        self.start_websocket_server()

    def joint_state_callback(self, msg):
        # Convert JointState message to JSON and send to Unity
        joint_data = {
            'type': 'joint_state',
            'name': list(msg.name),
            'position': [float(p) for p in msg.position],
            'velocity': [float(v) for v in msg.velocity],
            'effort': [float(e) for e in msg.effort],
            'timestamp': float(msg.header.stamp.sec) + float(msg.header.stamp.nanosec) / 1e9
        }

        self.broadcast_to_unity(joint_data)

    def odom_callback(self, msg):
        # Convert Odometry message to JSON and send to Unity
        odom_data = {
            'type': 'odometry',
            'position': {
                'x': float(msg.pose.pose.position.x),
                'y': float(msg.pose.pose.position.y),
                'z': float(msg.pose.pose.position.z)
            },
            'orientation': {
                'x': float(msg.pose.pose.orientation.x),
                'y': float(msg.pose.pose.orientation.y),
                'z': float(msg.pose.pose.orientation.z),
                'w': float(msg.pose.pose.orientation.w)
            },
            'linear_velocity': {
                'x': float(msg.twist.twist.linear.x),
                'y': float(msg.twist.twist.linear.y),
                'z': float(msg.twist.twist.linear.z)
            },
            'angular_velocity': {
                'x': float(msg.twist.twist.angular.x),
                'y': float(msg.twist.twist.angular.y),
                'z': float(msg.twist.twist.angular.z)
            },
            'timestamp': float(msg.header.stamp.sec) + float(msg.header.stamp.nanosec) / 1e9
        }

        self.broadcast_to_unity(odom_data)

    def lidar_callback(self, msg):
        # Convert LaserScan message to JSON and send to Unity
        lidar_data = {
            'type': 'lidar_scan',
            'angle_min': float(msg.angle_min),
            'angle_max': float(msg.angle_max),
            'angle_increment': float(msg.angle_increment),
            'time_increment': float(msg.time_increment),
            'scan_time': float(msg.scan_time),
            'range_min': float(msg.range_min),
            'range_max': float(msg.range_max),
            'ranges': [float(r) if not float('inf') else 30.0 for r in msg.ranges],  # Limit to max range
            'timestamp': float(msg.header.stamp.sec) + float(msg.header.stamp.nanosec) / 1e9
        }

        self.broadcast_to_unity(lidar_data)

    async def websocket_handler(self, websocket, path):
        # Register client
        self.connected_clients.add(websocket)
        self.get_logger().info(f'Unity client connected: {websocket.remote_address}')

        try:
            # Keep connection alive
            async for message in websocket:
                # Handle messages from Unity (if any)
                pass
        except websockets.exceptions.ConnectionClosed:
            pass
        finally:
            # Unregister client
            self.connected_clients.discard(websocket)
            self.get_logger().info(f'Unity client disconnected: {websocket.remote_address}')

    def start_websocket_server(self):
        # Start WebSocket server in a separate thread
        import threading
        server_thread = threading.Thread(target=self.run_websocket_server)
        server_thread.daemon = True
        server_thread.start()

    def run_websocket_server(self):
        # Run the WebSocket server
        start_server = websockets.serve(self.websocket_handler, "localhost", 8765)
        asyncio.run(start_server)

    async def broadcast_to_unity(self, data):
        # Send data to all connected Unity clients
        if self.connected_clients:
            message = json.dumps(data)
            disconnected_clients = []

            for client in self.connected_clients:
                try:
                    await client.send(message)
                except websockets.exceptions.ConnectionClosed:
                    disconnected_clients.append(client)

            # Remove disconnected clients
            for client in disconnected_clients:
                self.connected_clients.discard(client)

    def broadcast_to_unity(self, data):
        # Synchronous wrapper for ROS callbacks
        asyncio.run(self.broadcast_async(data))

    async def broadcast_async(self, data):
        await self.broadcast_to_unity(data)

def main(args=None):
    rclpy.init(args=args)
    bridge = ROS2UnityBridge()

    try:
        rclpy.spin(bridge)
    except KeyboardInterrupt:
        pass
    finally:
        bridge.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
```

## Running the Unity Digital Twin

### Prerequisites
1. Ensure Gazebo simulation is running with sensor data
2. Verify ROS 2 nodes are publishing robot state data
3. Confirm Unity project has ROS bridge properly configured
4. Make sure network connectivity exists between Unity and ROS 2

### Execution Steps
1. Start the Gazebo simulation:
   ```bash
   # Launch Gazebo with your robot
   ros2 launch your_package robot_spawn.launch.py
   ```

2. Start the ROS-Unity bridge:
   ```bash
   # Run the bridge node
   ros2 run your_package ros2_unity_bridge.py
   ```

3. Launch Unity and run the digital twin scene:
   - Open the Unity project
   - Load the digital twin scene
   - Press Play to start the visualization

4. Monitor synchronization:
   ```bash
   # Check ROS topics are active
   ros2 topic list | grep -E "(joint_states|odom|scan)"

   # Monitor data rates
   ros2 topic hz /joint_states
   ```

### Unity Scene Configuration
In Unity, configure the scene properly:

1. **Set up the camera**: Position the main camera for optimal viewing
2. **Configure lighting**: Use realistic lighting that matches the Gazebo environment
3. **Add coordinate system visualization**: Show axes to understand robot orientation
4. **Implement user controls**: Allow users to navigate the 3D space

## Verification and Troubleshooting

### Checking Synchronization
1. Verify that Unity robot moves in sync with Gazebo simulation
2. Confirm sensor data visualization matches Gazebo outputs
3. Check that joint angles and positions are synchronized
4. Validate that the digital twin responds to simulation changes in real-time

### Common Issues and Solutions
- **No connection to ROS**: Check network connectivity and ROS bridge status
- **Robot not moving**: Verify joint state topic subscription and message format
- **Delayed updates**: Adjust update rates and network configurations
- **Coordinate system mismatches**: Ensure proper coordinate transformations between ROS and Unity

## Advanced Features

### Multi-Robot Digital Twin
Extend the digital twin to support multiple robots:

```csharp
// Multi-robot digital twin manager
public class MultiRobotDigitalTwin : MonoBehaviour
{
    public GameObject robotPrefab;
    public List<string> robotNames = new List<string>();
    private Dictionary<string, GameObject> robotInstances = new Dictionary<string, GameObject>();

    void Start()
    {
        foreach (string robotName in robotNames)
        {
            SpawnRobot(robotName);
        }
    }

    void SpawnRobot(string robotName)
    {
        GameObject robot = Instantiate(robotPrefab);
        robot.name = robotName;
        robotInstances[robotName] = robot;

        // Subscribe to robot-specific topics
        SubscribeToRobotTopics(robotName);
    }

    void SubscribeToRobotTopics(string robotName)
    {
        // Subscribe to robot-specific topics
        ros2Unity.CreateSubscription<JointState>($"{robotName}/joint_states",
            (msg) => RobotJointStateCallback(robotName, msg));
    }

    void RobotJointStateCallback(string robotName, JointState msg)
    {
        if (robotInstances.ContainsKey(robotName))
        {
            var jointProcessor = robotInstances[robotName].GetComponent<JointStateProcessor>();
            if (jointProcessor != null)
            {
                jointProcessor.UpdateRobotJoints(msg);
            }
        }
    }
}
```

### Recording and Playback
Implement recording and playback functionality:

```csharp
// Robot state recorder
public class RobotStateRecorder : MonoBehaviour
{
    [System.Serializable]
    public class RobotState
    {
        public float timestamp;
        public Vector3 position;
        public Quaternion rotation;
        public List<float> jointPositions;
    }

    public List<RobotState> recordedStates = new List<RobotState>();
    public bool isRecording = false;
    public bool isPlaying = false;

    void Update()
    {
        if (isRecording)
        {
            RecordState();
        }
        else if (isPlaying)
        {
            PlaybackState();
        }
    }

    void RecordState()
    {
        RobotState state = new RobotState
        {
            timestamp = Time.time,
            position = transform.position,
            rotation = transform.rotation,
            jointPositions = GetCurrentJointPositions()
        };

        recordedStates.Add(state);
    }

    List<float> GetCurrentJointPositions()
    {
        // Get current joint positions from robot
        List<float> positions = new List<float>();
        // Implementation depends on your joint structure
        return positions;
    }

    void PlaybackState()
    {
        // Play back recorded states
        // Implementation for interpolating between recorded states
    }
}
```

## Summary

This chapter covered the fundamentals of creating a Unity-based digital twin for robotics simulation. You learned about:

- Unity digital twin architecture and system components
- Setting up Unity for robotics applications
- Creating robot models and joint configurations in Unity
- ROS 2 integration and bridge implementation
- Real-time synchronization of robot state
- Sensor data visualization in Unity
- Practical implementation of a complete digital twin system
- Advanced features like multi-robot support and recording

The Unity digital twin provides a powerful visualization layer that complements the physics simulation in Gazebo, enabling developers to observe and analyze robot behavior in a visually rich environment. This combination of accurate physics simulation and realistic visualization creates a comprehensive digital twin system for robotics development and testing.