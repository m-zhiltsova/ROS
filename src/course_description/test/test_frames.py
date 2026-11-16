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

"""Structural checks of the expanded vehicle description (course PR06)."""

from pathlib import Path
import xml.etree.ElementTree as ET

import xacro

XACRO_PATH = Path(__file__).resolve().parent.parent / 'urdf' / 'vehicle.urdf.xacro'

FIXED_JOINTS = ('camera_joint', 'lidar_joint', 'imu_joint')
WHEEL_JOINTS = (
    'front_left_wheel_joint',
    'front_right_wheel_joint',
    'rear_left_wheel_joint',
    'rear_right_wheel_joint',
)


def _robot():
    """Expand the Xacro file and return the root URDF element."""
    document = xacro.process_file(str(XACRO_PATH))
    return ET.fromstring(document.toxml())


def _joint(robot, name):
    """Find a joint element by name and fail with a clear message."""
    for joint in robot.findall('joint'):
        if joint.get('name') == name:
            return joint
    raise AssertionError('joint {} not found'.format(name))


def _parent(joint):
    """Return the parent link name of a joint element."""
    parent = joint.find('parent')
    assert parent is not None
    return parent.get('link')


def test_sensor_joints_are_fixed_to_base_link():
    """Camera, lidar and IMU are fixed directly to base_link."""
    robot = _robot()
    for name in FIXED_JOINTS:
        joint = _joint(robot, name)
        assert joint.get('type') == 'fixed', name
        assert _parent(joint) == 'base_link', name


def test_wheel_joints_are_continuous():
    """All four wheels roll with continuous joints."""
    robot = _robot()
    for name in WHEEL_JOINTS:
        joint = _joint(robot, name)
        assert joint.get('type') == 'continuous', name
        assert _parent(joint) == 'base_link', name


def test_tree_is_connected():
    """Every link is reachable from base_link through the joints."""
    robot = _robot()
    links = {link.get('name') for link in robot.findall('link')}
    neighbours = {}
    for joint in robot.findall('joint'):
        parent = _parent(joint)
        child = joint.find('child')
        assert child is not None
        child_link = child.get('link')
        neighbours.setdefault(parent, set()).add(child_link)
        neighbours.setdefault(child_link, set()).add(parent)
    seen = {'base_link'}
    stack = ['base_link']
    while stack:
        node = stack.pop()
        for neighbour in neighbours.get(node, ()):
            if neighbour not in seen:
                seen.add(neighbour)
                stack.append(neighbour)
    assert seen == links, 'unreachable links: {}'.format(sorted(links - seen))


def test_inertias_are_physically_plausible():
    """Masses are positive and inertia tensors obey the triangle rules."""
    for inertial in _robot().iter('inertial'):
        mass = inertial.find('mass')
        assert mass is not None
        assert float(mass.get('value')) > 0
        inertia = inertial.find('inertia')
        assert inertia is not None
        ixx = float(inertia.get('ixx'))
        iyy = float(inertia.get('iyy'))
        izz = float(inertia.get('izz'))
        assert ixx > 0 and iyy > 0 and izz > 0
        assert ixx + iyy >= izz
        assert ixx + izz >= iyy
        assert iyy + izz >= ixx
