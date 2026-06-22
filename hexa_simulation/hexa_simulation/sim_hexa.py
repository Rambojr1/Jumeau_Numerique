import math

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState


class HexaSimulator(Node):
    def __init__(self):
        super().__init__('sim_hexa')
        self.publisher = self.create_publisher(JointState, '/joint_states', 10)
        self.timer = self.create_timer(0.05, self.publish_joint_states)
        self.start_time = self.get_clock().now()
        self.joint_names = [
            f'leg_{index}_{joint}_joint'
            for index in range(1, 7)
            for joint in ('coxa', 'femur', 'tibia')
        ]

    def publish_joint_states(self):
        elapsed = (self.get_clock().now() - self.start_time).nanoseconds * 1e-9
        joint_state = JointState()
        joint_state.header.stamp = self.get_clock().now().to_msg()
        joint_state.name = list(self.joint_names)
        joint_state.position = []

        for leg_index in range(1, 7):
            phase = 0.0 if leg_index % 2 == 0 else math.pi
            coxa = 0.2 * math.sin(elapsed + phase)
            femur = 0.35 * math.sin(elapsed + phase + math.pi / 2.0)
            tibia = -0.45 * math.sin(elapsed + phase)
            joint_state.position.extend([coxa, femur, tibia])

        self.publisher.publish(joint_state)


def main(args=None):
    rclpy.init(args=args)
    node = HexaSimulator()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
