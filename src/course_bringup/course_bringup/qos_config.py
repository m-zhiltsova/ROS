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

"""QoS profile helpers for the sensor stream (course practice PR05)."""

from rclpy.qos import QoSHistoryPolicy, QoSProfile, QoSReliabilityPolicy

SENSOR_DEPTH = 10

SENSOR_PUBLISHER_QOS = QoSProfile(
    reliability=QoSReliabilityPolicy.BEST_EFFORT,
    history=QoSHistoryPolicy.KEEP_LAST,
    depth=SENSOR_DEPTH,
)

ALLOWED_RELIABILITY = ('reliable', 'best_effort')


def reliability_policy(name):
    """Return the QoSReliabilityPolicy for a launch value; raise otherwise."""
    if name == 'reliable':
        return QoSReliabilityPolicy.RELIABLE
    if name == 'best_effort':
        return QoSReliabilityPolicy.BEST_EFFORT
    raise ValueError(
        'reliability must be one of {}, got {!r}'.format(
            ALLOWED_RELIABILITY, name))
