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

"""Launch robot_state_publisher with the course Ackermann description."""

import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, LogInfo
from launch.substitutions import Command, LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    """Publish robot_description from the Xacro file and run the publisher."""
    description_dir = os.path.join(
        get_package_share_directory('course_description'), 'urdf')
    default_xacro = os.path.join(description_dir, 'vehicle.urdf.xacro')

    return LaunchDescription([
        DeclareLaunchArgument(
            'robot_description_file', default_value=default_xacro,
            description='Path to the Xacro file of the robot description'),
        LogInfo(
            msg=['Using robot description: ',
                 LaunchConfiguration('robot_description_file')]),
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            parameters=[{
                'robot_description': Command(
                    ['xacro ', LaunchConfiguration('robot_description_file')]),
            }],
        ),
    ])
