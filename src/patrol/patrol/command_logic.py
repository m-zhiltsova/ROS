from geometry_msgs.msg import Twist

def compute_command(latest_pose):
    """
    Возвращает Twist на основе последней позы.
    Если поза отсутствует — нулевая команда.
    """
    command = Twist()
    if latest_pose is None:
        command.linear.x = 0.0
        command.angular.z = 0.0
    else:
        command.linear.x = 0.5
        command.angular.z = 0.3
    return command
