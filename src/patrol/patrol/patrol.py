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
from patrol.command_logic import compute_command, validate_parameters
import rclpy
from rclpy.node import Node, SetParametersResult
from turtlesim_msgs.msg import Pose


class Patrol(Node):
    """Node that mirrors turtle motion by publishing Twist commands."""

    def __init__(self):
        """Create publisher, subscription, timer and parameters."""
        super().__init__('patrol')
        self.declare_parameter('publish_hz', 10.0)
        self.declare_parameter('linear_speed', 0.5)
        self.declare_parameter('turn_rate', 0.3)
        self.publish_hz = self.get_parameter('publish_hz').value
        self.linear_speed = self.get_parameter('linear_speed').value
        self.turn_rate = self.get_parameter('turn_rate').value
        self.latest_pose = None
        self.pose_sub = self.create_subscription(
            Pose, '/turtle1/pose', self.on_pose, 10)
        self.publisher = self.create_publisher(Twist, 'cmd_vel', 10)
        self.timer = self.create_timer(1.0 / self.publish_hz, self.tick)
        # TEMPORARILY DISABLED for defect reproduction (PR04, side branch)
        # self.add_on_set_parameters_callback(self.validate)
        self.add_post_set_parameters_callback(self.apply)

    def on_pose(self, message):
        """Store the latest Pose message."""
        self.latest_pose = message

    def tick(self):
        """Publish a command computed from the last pose."""
        command = compute_command(
            self.latest_pose, self.linear_speed, self.turn_rate)
        self.publisher.publish(command)

    def validate(self, updates):
        """Reject a proposed set before it changes any state."""
        proposed = {
            'publish_hz': self.get_parameter('publish_hz').value,
            'linear_speed': self.get_parameter('linear_speed').value,
            'turn_rate': self.get_parameter('turn_rate').value,
        }
        proposed.update({param.name: param.value for param in updates})
        ok, reason = validate_parameters(
            proposed['publish_hz'],
            proposed['linear_speed'],
            proposed['turn_rate'])
        return SetParametersResult(successful=ok, reason=reason)

    def apply(self, updates):
        """Apply an accepted set: fields and, if needed, a new timer."""
        old_hz = self.publish_hz
        self.publish_hz = self.get_parameter('publish_hz').value
        self.linear_speed = self.get_parameter('linear_speed').value
        self.turn_rate = self.get_parameter('turn_rate').value
        if self.publish_hz != old_hz:
            self.timer.cancel()
            self.destroy_timer(self.timer)
            self.timer = self.create_timer(1.0 / self.publish_hz, self.tick)


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
