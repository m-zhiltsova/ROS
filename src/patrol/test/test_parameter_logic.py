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

from patrol.command_logic import validate_parameters


def test_default_set_accepted():
    """Default values are accepted."""
    ok, reason = validate_parameters(10.0, 0.5, 0.3)
    assert ok
    assert reason == ''


def test_frequency_change_to_5_accepted():
    """A normal 10 -> 5 Hz change is accepted."""
    ok, reason = validate_parameters(5.0, 0.5, 0.3)
    assert ok


def test_zero_frequency_rejected():
    """publish_hz = 0 is rejected."""
    ok, reason = validate_parameters(0.0, 0.5, 0.3)
    assert not ok
    assert 'publish_hz' in reason


def test_negative_frequency_rejected():
    """A negative publish_hz is rejected."""
    ok, reason = validate_parameters(-2.0, 0.5, 0.3)
    assert not ok
    assert 'publish_hz' in reason


def test_frequency_above_limit_rejected():
    """publish_hz above 30 Hz is rejected."""
    ok, reason = validate_parameters(31.0, 0.5, 0.3)
    assert not ok
    assert 'publish_hz' in reason


def test_nan_frequency_rejected():
    """A NaN publish_hz is rejected."""
    ok, reason = validate_parameters(float('nan'), 0.5, 0.3)
    assert not ok
    assert 'finite' in reason


def test_infinity_speed_rejected():
    """Infinity linear_speed is rejected."""
    ok, reason = validate_parameters(10.0, float('inf'), 0.3)
    assert not ok
    assert 'finite' in reason


def test_speed_above_limit_rejected():
    """linear_speed above 1 m/s is rejected."""
    ok, reason = validate_parameters(10.0, 1.5, 0.3)
    assert not ok
    assert 'linear_speed' in reason


def test_speed_negative_rejected():
    """Negative linear_speed is rejected."""
    ok, reason = validate_parameters(10.0, -0.1, 0.3)
    assert not ok
    assert 'linear_speed' in reason


def test_turn_below_limit_rejected():
    """turn_rate below -1 rad/s is rejected."""
    ok, reason = validate_parameters(10.0, 0.5, -1.5)
    assert not ok
    assert 'turn_rate' in reason


def test_boundary_values_accepted():
    """Boundary values 1/30 Hz, 0/1 m/s, -1/1 rad/s are accepted."""
    assert validate_parameters(1.0, 0.0, -1.0)[0]
    assert validate_parameters(30.0, 1.0, 1.0)[0]
