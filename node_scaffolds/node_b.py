"""Node B: subscribes to Node A, tags the message, and republishes it.

Copy this file into your package before you edit it:

    cp node_scaffolds/node_b.py ros2_ws/src/lab04_pub_sub/lab04_pub_sub/

Fill in every TODO. See the ROS 2 Python Nodes Reference for the method
signatures and worked examples:
https://mems-intro-to-robotics.github.io/guides/ros2_python_nodes_reference/
"""

import os

import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class PubSubNodeB(Node):
    def __init__(self):
        super().__init__('node_b')

        # TODO: Set your NetID so it appears in the relayed message.
        # Option A (simplest): replace 'your_netid' below with your actual NetID.
        # Option B: export NETID in the container and leave the fallback alone.
        self.netid = os.getenv("NETID", "your_netid").strip()

        # TODO: Create a subscriber to '/topic_a_to_b'
        # - Message type: String
        # - Callback: self._on_msg
        # - Queue size: 10
        self.sub = None  # Replace with create_subscription(...)

        # TODO: Create a publisher to '/topic_b_to_c'
        # - Message type: String
        # - Queue size: 10
        self.pub = None  # Replace with create_publisher(...)

        self.get_logger().info("Node B has started. Listening and relaying...")

    def _on_msg(self, msg: String):
        self.get_logger().info(f'Heard from A: "{msg.data}"')

        new_msg = String()
        # TODO: Build the outgoing message and assign it to new_msg.data.
        # It must carry your NetID, e.g.:
        # new_msg.data = f'{msg.data} -- processed by Node B ({self.netid})'

        # TODO: Publish new_msg to '/topic_b_to_c'
        # self.pub.____(new_msg)

        self.get_logger().info(f'Relaying to C: "{new_msg.data}"')


# TODO: Write the main function boilerplate
# - Initialize rclpy
# - Create the node
# - Call rclpy.spin(node) to keep it alive
# - Destroy the node and shut down when done
