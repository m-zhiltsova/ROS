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

import math

from geometry_msgs.msg import Twist

MIN_PUBLISH_HZ = 1.0
MAX_PUBLISH_HZ = 30.0
MIN_LINEAR_SPEED = 0.0
MAX_LINEAR_SPEED = 1.0
MIN_TURN_RATE = -1.0
MAX_TURN_RATE = 1.0


def compute_command(latest_pose, linear_speed=0.5, turn_rate=0.3):
    """Return a Twist based on the last pose, or zero if no pose yet."""
    command = Twist()
    if latest_pose is None:
        command.linear.x = 0.0
        command.angular.z = 0.0
    else:
        command.linear.x = linear_speed
        command.angular.z = turn_rate
    return command


def validate_parameters(publish_hz, linear_speed, turn_rate):
    """Check a proposed parameter set; return (ok, reason)."""
    for value in (publish_hz, linear_speed, turn_rate):
        if not math.isfinite(value):
            return (False, 'parameter must be a finite number')
    if not MIN_PUBLISH_HZ <= publish_hz <= MAX_PUBLISH_HZ:
        return (
            False,
            'publish_hz must be within [1, 30] Hz, got {}'.format(publish_hz),
        )
    if not MIN_LINEAR_SPEED <= linear_speed <= MAX_LINEAR_SPEED:
        return (
            False,
            'linear_speed must be within [0, 1] m/s, got {}'.format(linear_speed),
        )
    if not MIN_TURN_RATE <= turn_rate <= MAX_TURN_RATE:
        return (
            False,
            'turn_rate must be within [-1, 1] rad/s, got {}'.format(turn_rate),
        )
    return (True, '')
