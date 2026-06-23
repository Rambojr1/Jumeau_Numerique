import math

import rclpy
import rclpy.parameter
from rclpy.node import Node
from sensor_msgs.msg import JointState
from std_srvs.srv import Trigger
from trajectory_msgs.msg import JointTrajectory


# Limites angulaires par type d'articulation (rad)
JOINT_LIMITS = {
    'coxa':  (-0.785, 0.785),
    'femur': (-1.000, 1.000),
    'tibia': (-1.500, 1.500),
}

JOINT_NAMES = [
    f'leg_{i}_{j}_joint'
    for i in range(1, 7)
    for j in ('coxa', 'femur', 'tibia')
]


class HexaSimulator(Node):
    """Noeud ROS 2 qui :
    - écoute /hexapode/joint_commands  : position cible immédiate (interpolée)
    - écoute /hexapode/trajectory      : séquence de waypoints exécutés l'un
      après l'autre ; passe au suivant quand le robot a atteint le courant.
    - publie l'état sur /joint_states à 50 Hz.

    Paramètres ROS :
        joint_speed         (float, défaut 1.0)   : vitesse max en rad/s.
        trajectory_mode     (bool,  défaut False) : positions directes (pas
            d'interpolation), utile si l'appelant gère déjà la fluidité.
        loop_trajectory     (bool,  défaut False) : reboucle indéfiniment sur
            la séquence reçue.
        waypoint_threshold  (float, défaut 0.02)  : seuil en rad pour
            considérer un waypoint comme atteint.

    Champ velocity du message joint_commands :
        Si fourni et > 0, remplace joint_speed pour ce joint.
    """

    def __init__(self):
        super().__init__('sim_hexa')

        self.declare_parameter('joint_speed',        1.0)
        self.declare_parameter('trajectory_mode',     False)
        self.declare_parameter('loop_trajectory',     False)
        self.declare_parameter('waypoint_threshold',  0.02)

        self.current  = {name: 0.0 for name in JOINT_NAMES}
        self.target   = {name: 0.0 for name in JOINT_NAMES}
        self._cmd_velocity: dict[str, float | None] = {name: None for name in JOINT_NAMES}

        # File de waypoints pour /hexapode/trajectory
        self._waypoints: list[dict[str, float]] = []
        self._wp_index: int = 0

        self.publisher = self.create_publisher(JointState, '/joint_states', 10)
        self.create_subscription(
            JointState,
            '/hexapode/joint_commands',
            self._on_command,
            10,
        )
        self.create_subscription(
            JointTrajectory,
            '/hexapode/trajectory',
            self._on_trajectory,
            10,
        )
        self.create_service(Trigger, '/hexapode/stop', self._on_stop_service)

        # Topics pour configurer vitesse et boucle au runtime
        self.create_subscription(JointState, '/hexapode/set_speed', self._on_set_speed, 10)
        self.create_subscription(JointState, '/hexapode/set_loop', self._on_set_loop, 10)

        self._last_time = self.get_clock().now()
        self.create_timer(0.02, self._update)  # 50 Hz

    # ------------------------------------------------------------------

    def _clamp(self, name: str, value: float) -> float:
        joint_type = name.split('_')[2]  # coxa | femur | tibia
        lo, hi = JOINT_LIMITS[joint_type]
        return max(lo, min(hi, value))

    def _on_command(self, msg: JointState):
        """Commande immédiate : interrompt la séquence en cours si active."""
        self._waypoints = []
        velocities = list(msg.velocity) if msg.velocity else []
        for i, name in enumerate(msg.name):
            if name not in self.target:
                continue
            if i < len(msg.position):
                self.target[name] = self._clamp(name, msg.position[i])
            if i < len(velocities) and velocities[i] > 0.0:
                self._cmd_velocity[name] = float(velocities[i])
            else:
                self._cmd_velocity[name] = None
        if self.get_parameter('trajectory_mode').value:
            for name in self.target:
                self.current[name] = self.target[name]

    def _on_trajectory(self, msg: JointTrajectory):
        """Charge une séquence de waypoints et démarre l'exécution."""
        self._waypoints = []
        for point in msg.points:
            wp = {
                name: self._clamp(name, float(pos))
                for name, pos in zip(msg.joint_names, point.positions)
                if name in self.target
            }
            if wp:
                self._waypoints.append(wp)
        self._wp_index = 0
        if self._waypoints:
            self._apply_waypoint(0)

    def _apply_waypoint(self, idx: int):
        for name, pos in self._waypoints[idx].items():
            self.target[name] = pos
            self._cmd_velocity[name] = None

    def _waypoint_reached(self) -> bool:
        if not self._waypoints:
            return False
        threshold = float(self.get_parameter('waypoint_threshold').value)
        wp = self._waypoints[self._wp_index]
        return all(abs(self.current[name] - pos) <= threshold for name, pos in wp.items())

    def _on_stop_service(self, request: Trigger.Request, response: Trigger.Response) -> Trigger.Response:
        """Arrête la séquence en cours et fige le robot à sa position actuelle."""
        self._waypoints = []
        self._wp_index = 0
        # Les joints restent à leur position courante
        for name in JOINT_NAMES:
            self.target[name] = self.current[name]
            self._cmd_velocity[name] = None
        response.success = True
        response.message = 'Robot stopped and held at current position'
        return response

    def _on_set_speed(self, msg: JointState):
        """Change la vitesse de déplacement.
        Publication sur /hexapode/set_speed avec position[0] = nouvelle vitesse.
        """
        if msg.position and len(msg.position) > 0:
            new_speed = float(msg.position[0])
            self.set_parameters([rclpy.parameter.Parameter('joint_speed', rclpy.Parameter.Type.DOUBLE, new_speed)])
            self.get_logger().info(f'Vitesse mise à jour : {new_speed} rad/s')

    def _on_set_loop(self, msg: JointState):
        """Active/désactive la boucle des séquences.
        Publication sur /hexapode/set_loop avec position[0] = 1.0 (actif) ou 0.0 (inactif).
        """
        if msg.position and len(msg.position) > 0:
            should_loop = float(msg.position[0]) > 0.5
            self.set_parameters([rclpy.parameter.Parameter('loop_trajectory', rclpy.Parameter.Type.BOOL, should_loop)])
            self.get_logger().info(f'Boucle : {"activée" if should_loop else "désactivée"}')

    def _update(self):
        now = self.get_clock().now()
        dt = (now - self._last_time).nanoseconds * 1e-9
        self._last_time = now

        # Avancer l'interpolation (sauf en mode direct)
        if not self.get_parameter('trajectory_mode').value:
            global_speed = float(self.get_parameter('joint_speed').value)
            for name in JOINT_NAMES:
                speed = self._cmd_velocity[name] or global_speed
                max_step = speed * dt
                diff = self.target[name] - self.current[name]
                if abs(diff) <= max_step:
                    self.current[name] = self.target[name]
                else:
                    self.current[name] += math.copysign(max_step, diff)

        # Passer au waypoint suivant si le courant est atteint
        if self._waypoints and self._waypoint_reached():
            next_idx = self._wp_index + 1
            if next_idx < len(self._waypoints):
                self._wp_index = next_idx
                self._apply_waypoint(self._wp_index)
            elif self.get_parameter('loop_trajectory').value:
                self._wp_index = 0
                self._apply_waypoint(0)
            else:
                self._waypoints = []  # séquence terminée

        msg = JointState()
        msg.header.stamp = now.to_msg()
        msg.name = list(JOINT_NAMES)
        msg.position = [self.current[n] for n in JOINT_NAMES]
        self.publisher.publish(msg)


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
