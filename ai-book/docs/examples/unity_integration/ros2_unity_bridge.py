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