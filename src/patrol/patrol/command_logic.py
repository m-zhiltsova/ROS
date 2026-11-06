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


def compute_command(latest_pose):
    """Return a Twist based on the last pose, or zero if no pose yet."""
    command = Twist()
    if latest_pose is None:
        command.linear.x = 0.0
        command.angular.z = 0.0
    else:
        command.linear.x = 0.5
        command.angular.z = 0.3
    return command
