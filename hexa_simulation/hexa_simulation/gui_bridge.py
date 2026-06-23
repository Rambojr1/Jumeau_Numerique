#!/usr/bin/env python3
"""
Bridge qui écoute les commandes du GUI (/joint_states du joint_state_publisher_gui)
et les republish sur /hexapode/joint_commands pour que sim_hexa les traite.
"""

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState


class GUIBridge(Node):
    def __init__(self):
        super().__init__('gui_bridge')
        self.publisher = self.create_publisher(JointState, '/hexapode/joint_commands', 10)
        self.create_subscription(JointState, '/joint_states', self._on_joint_states, 10)

    def _on_joint_states(self, msg: JointState):
        """Republish /joint_states du GUI sur /hexapode/joint_commands."""
        # Ignorer les messages sans positions
        if not msg.position:
            return
        # Republish tel quel
        self.publisher.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    node = GUIBridge()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
