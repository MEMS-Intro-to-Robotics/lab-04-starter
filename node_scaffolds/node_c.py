"""Node C: subscribes to Node B's output and logs the final message.

Copy this file into your package before you edit it:

    cp node_scaffolds/node_c.py ros2_ws/src/lab04_pub_sub/lab04_pub_sub/

Fill in every TODO. See the ROS 2 Python Nodes Reference for the method
signatures and worked examples:
https://mems-intro-to-robotics.github.io/guides/ros2_python_nodes_reference/
"""

import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class SubNodeC(Node):
    def __init__(self):
        super().__init__('node_c')

        # TODO: Create a subscriber to '/topic_b_to_c'
        # - Message type: String
        # - Callback: self._on_msg
        # - Queue size: 10
        self.sub = None  # Replace with create_subscription(...)

        self.get_logger().info("Node C has started. Listening...")

    def _on_msg(self, msg: String):
        self.get_logger().info(f'Final message received: "{msg.data}"')


# TODO: Write the main function boilerplate
# - Initialize rclpy
# - Create the node
# - Call rclpy.spin(node) to keep it alive
# - Destroy the node and shut down when done
