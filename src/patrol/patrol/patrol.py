import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim_msgs.msg import Pose
from patrol.command_logic import compute_command


class Patrol(Node):
    def __init__(self):
        super().__init__('patrol')
        self.latest_pose = None

        # Подписка на позу
        self.pose_sub = self.create_subscription(
            Pose,
            '/turtle1/pose',
            self.on_pose,
            10
        )

        # Издатель команды
        self.publisher = self.create_publisher(Twist, 'cmd_vel', 10)

        # Таймер 0.1 с
        self.timer = self.create_timer(0.1, self.tick)

    def on_pose(self, message):
        self.latest_pose = message

    def tick(self):
        self.publisher.publish(compute_command(self.latest_pose))

def main(args=None):
    rclpy.init(args=args)
    node = Patrol()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.try_shutdown()


if __name__ == '__main__':
    main()
