# Лабораторные работы по Робототехнике

Личный репозиторий для практических работ курса «Робототехника · ROS 2».
Среда: distrobox + контейнер `ros2-lyrical` (ROS 2 Lyrical), `ROS_DOMAIN_ID=16`.

## ПР02. Терминал, пакет и запуск turtlesim

Пакет `turtle_bringup` содержит launch-файл `sim.launch.py`, который запускает
установленную ноду `turtlesim_node`. Собственной ноды в пакете пока нет.

### Сборка

```bash
source /opt/ros/lyrical/setup.bash
cd $(git rev-parse --show-toplevel)
colcon build --symlink-install --packages-select turtle_bringup \
  2>&1 | tee evidence/pr02/build.txt
```

### Запуск и проверка графа

```bash
# Терминал A
source /opt/ros/lyrical/setup.bash
source install/setup.bash
export ROS_DOMAIN_ID=16
ros2 launch turtle_bringup sim.launch.py

# Терминал B
source /opt/ros/lyrical/setup.bash
source install/setup.bash
export ROS_DOMAIN_ID=16
ros2 node list --no-daemon --spin-time 2

# Команда движения в /turtle1/cmd_vel
ros2 topic pub --once /turtle1/cmd_vel geometry_msgs/msg/Twist \
  '{linear: {x: 1.0}, angular: {z: 0.5}}'
```

Остановить: `Ctrl+C` в терминале A — запущенный launch завершает turtlesim.

### CI

`.github/workflows/ci.yml`: сборка `turtle_bringup`, проверка установленного
`sim.launch.py` и `check_practice.py PR02 --submission .` с зафиксированным
course-kit `v1-w10`.

ИИ использовался для генерации скриптов автоматизации сбора данных и настройки окружения distrobox.
