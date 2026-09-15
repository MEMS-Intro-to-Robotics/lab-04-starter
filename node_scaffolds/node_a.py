"""Node A: publishes a String message on a timer.

Copy this file into your package before you edit it:

    cp node_scaffolds/node_a.py ros2_ws/src/lab04_pub_sub/lab04_pub_sub/

Fill in every TODO. See the ROS 2 Python Nodes Reference for the method
signatures and worked examples:
https://mems-intro-to-robotics.github.io/guides/ros2_python_nodes_reference/
"""

import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class PubNodeA(Node):
    def __init__(self):
        super().__init__('node_a')

        # TODO: Create a publisher for String messages
        # - Topic: '/topic_a_to_b'
        # - Message type: String
        # - Queue size: 10
        self.pub = None   # Replace None with your publisher

        # TODO: Create a timer that calls self.timer_callback every 2.0 seconds
        self.timer = None  # Replace None with your timer

        self.get_logger().info("Node A has started. Publishing...")

    def timer_callback(self):
        msg = String()
        msg.data = "Hello from Node A!"

        # TODO: Publish msg using your publisher
        # self.pub.____(msg)

        self.get_logger().info(f'Publishing: "{msg.data}"')


# TODO: Write the main function boilerplate
# - Initialize rclpy
# - Create the node
# - Call rclpy.spin(node) to keep it alive
# - Destroy the node and shut down when done
