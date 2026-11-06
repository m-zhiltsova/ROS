# Copyright 2026 Жильцова Марина
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

from patrol.command_logic import compute_command


class DummyPose:
    """Stub Pose for testing."""


def test_no_pose():
    """No pose → zero command."""
    cmd = compute_command(None)
    assert cmd.linear.x == 0.0
    assert cmd.angular.z == 0.0


def test_with_pose():
    """With pose → non-zero command."""
    cmd = compute_command(DummyPose())
    assert cmd.linear.x == 0.5
    assert cmd.angular.z == 0.3
