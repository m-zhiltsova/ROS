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

"""Tests of the QoS profile mapping used by pose_relay."""

from course_bringup.qos_config import (
    reliability_policy,
    SENSOR_PUBLISHER_QOS,
)
import pytest
from rclpy.qos import QoSReliabilityPolicy


def test_reliable_maps_to_reliable_policy():
    """The launch value reliable maps to the RELIABLE policy."""
    assert reliability_policy('reliable') is QoSReliabilityPolicy.RELIABLE


def test_best_effort_maps_to_best_effort_policy():
    """The launch value best_effort maps to the BEST_EFFORT policy."""
    assert reliability_policy('best_effort') is \
        QoSReliabilityPolicy.BEST_EFFORT


def test_unknown_reliability_rejected():
    """Any other value is rejected with a ValueError."""
    with pytest.raises(ValueError):
        reliability_policy('reliably')


def test_sensor_publisher_profile_is_best_effort():
    """The sensor stream is published best effort, keep_last, depth 10."""
    assert SENSOR_PUBLISHER_QOS.reliability is \
        QoSReliabilityPolicy.BEST_EFFORT
    assert SENSOR_PUBLISHER_QOS.depth == 10
