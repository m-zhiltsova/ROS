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

"""Launch the whole course system: turtlesim, patrol and pose relay."""

from launch import LaunchDescription
from launch.actions import (
    DeclareLaunchArgument,
    ExecuteProcess,
    LogInfo,
)
from launch.conditions import IfCondition
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node


def generate_launch_description():
    """One command: sim + patrol + pose relay in a namespace, optional MCAP."""
    namespace = LaunchConfiguration('namespace')
    record = LaunchConfiguration('record')
    bag_dir = LaunchConfiguration('bag_dir')
    subscriber_reliability = LaunchConfiguration('subscriber_reliability')
    sensor_pose_topic = PathJoinSubstitution([
        '/', namespace, 'sensor_pose'])

    return LaunchDescription([
        DeclareLaunchArgument(
            'namespace', default_value='robot_a',
            description='Namespace of the robot system'),
        DeclareLaunchArgument(
            'record', default_value='false',
            description='Record sensor_pose to MCAP while the system runs'),
        DeclareLaunchArgument(
            'bag_dir', default_value='bag',
            description='Output directory of the MCAP recorder'),
        DeclareLaunchArgument(
            'subscriber_reliability', default_value='best_effort',
            description='Probe subscriber reliability: '
                        'reliable | best_effort'),

        LogInfo(
            msg=['System in /', namespace,
                 ' (probe: ', subscriber_reliability,
                 ', record: ', record, ')']),

        Node(
            package='turtlesim',
            executable='turtlesim_node',
            output='screen',
        ),

        Node(
            package='patrol',
            executable='patrol',
            name='patrol',
            namespace=namespace,
            remappings=[('cmd_vel', '/turtle1/cmd_vel')],
            output='screen',
        ),

        Node(
            package='course_bringup',
            executable='pose_relay',
            name='pose_relay',
            namespace=namespace,
            parameters=[{'subscriber_reliability': subscriber_reliability}],
            remappings=[('turtle1/pose', '/turtle1/pose')],
            output='screen',
        ),

        ExecuteProcess(
            cmd=['ros2', 'bag', 'record', '-s', 'mcap', '-o', bag_dir,
                 '--topics', sensor_pose_topic],
            condition=IfCondition(record),
            output='screen',
        ),
    ])
