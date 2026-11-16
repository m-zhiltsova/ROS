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

"""Relay the turtle pose to sensor_pose and probe it with a configured QoS."""

from course_bringup.qos_config import (
    reliability_policy,
    SENSOR_DEPTH,
    SENSOR_PUBLISHER_QOS,
)
import rclpy
from rclpy.node import Node, SetParametersResult
from rclpy.qos import QoSHistoryPolicy, QoSProfile, QoSReliabilityPolicy
from turtlesim_msgs.msg import Pose


class PoseRelay(Node):
    """Forward the turtle pose to sensor_pose and probe it with a set QoS."""

    def __init__(self):
        """Create the input subscription, publisher and the QoS probe."""
        super().__init__('pose_relay')
        self.declare_parameter('subscriber_reliability', 'best_effort')
        self.received_count = 0
        self.input_sub = self.create_subscription(
            Pose, 'turtle1/pose', self.on_pose, self.input_qos())
        self.publisher = self.create_publisher(
            Pose, 'sensor_pose', SENSOR_PUBLISHER_QOS)
        self.probe_sub = self.create_probe()
        self.status_timer = self.create_timer(1.0, self.log_status)
        self.add_on_set_parameters_callback(self.validate_reliability)
        self.add_post_set_parameters_callback(self.apply_reliability)

    def input_qos(self):
        """Profile for the turtle pose input: the simulator's default QoS."""
        return QoSProfile(
            reliability=QoSReliabilityPolicy.RELIABLE,
            history=QoSHistoryPolicy.KEEP_LAST,
            depth=10)

    def create_probe(self):
        """Create the probe subscription with the configured reliability."""
        reliability = self.get_parameter('subscriber_reliability').value
        profile = QoSProfile(
            reliability=reliability_policy(reliability),
            history=QoSHistoryPolicy.KEEP_LAST,
            depth=SENSOR_DEPTH)
        return self.create_subscription(
            Pose, 'sensor_pose', self.on_probe, profile)

    def on_pose(self, message):
        """Republish the turtle pose as sensor_pose (best effort)."""
        self.publisher.publish(message)

    def on_probe(self, message):
        """Count the messages delivered to the probe subscription."""
        self.received_count += 1

    def log_status(self):
        """Log the probe delivery counter once per second."""
        self.get_logger().info(
            'sensor_pose probe: {} messages delivered'.format(
                self.received_count))

    def validate_reliability(self, updates):
        """Reject a proposed reliability that the probe cannot use."""
        for param in updates:
            if param.name == 'subscriber_reliability':
                try:
                    reliability_policy(param.value)
                except ValueError as exc:
                    return SetParametersResult(
                        successful=False, reason=str(exc))
        return SetParametersResult(successful=True, reason='')

    def apply_reliability(self, updates):
        """Recreate the probe subscription after an accepted change."""
        if any(p.name == 'subscriber_reliability' for p in updates):
            self.probe_sub.destroy_subscription()
            self.probe_sub = self.create_probe()


def main(args=None):
    """Run the pose_relay node."""
    rclpy.init(args=args)
    node = PoseRelay()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.try_shutdown()


if __name__ == '__main__':
    main()
