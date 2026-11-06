# Copyright 2026 Zhiltsova Marina
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from geometry_msgs.msg import Twist
from patrol.command_logic import compute_command
import rclpy
from rclpy.node import Node
from turtlesim_msgs.msg import Pose


class Patrol(Node):
    """Node that mirrors turtle motion by publishing Twist commands."""

    def __init__(self):
        """Create publisher, subscription and timer."""
        super().__init__('patrol')
        self.latest_pose = None
        self.pose_sub = self.create_subscription(
            Pose, '/turtle1/pose', self.on_pose, 10)
        self.publisher = self.create_publisher(Twist, 'cmd_vel', 10)
        self.timer = self.create_timer(0.1, self.tick)

    def on_pose(self, message):
        """Store the latest Pose message."""
        self.latest_pose = message

    def tick(self):
        """Publish a command computed from the last pose."""
        self.publisher.publish(compute_command(self.latest_pose))


def main(args=None):
    """Run the patrol node."""
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
