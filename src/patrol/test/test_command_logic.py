import pytest
from patrol.command_logic import compute_command

class DummyPose:
    pass

def test_no_pose():
    cmd = compute_command(None)
    assert cmd.linear.x == 0.0
    assert cmd.angular.z == 0.0

def test_with_pose():
    cmd = compute_command(DummyPose())
    assert cmd.linear.x == 0.5
    assert cmd.angular.z == 0.3
