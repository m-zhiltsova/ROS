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

## ПР03. Первая нода: поза и команда

Пакет `patrol` содержит ноду `/patrol`: подписка на `/turtle1/pose`
(`turtlesim_msgs/msg/Pose`), таймер 0,1 с и издатель `geometry_msgs/msg/Twist`
в относительный `cmd_vel`. До первой позы публикуется нулевая команда, после —
`linear.x = 0.5`, `angular.z = 0.3`. Выбор команды вынесен в чистую функцию
`patrol/command_logic.py` и покрыт pytest-тестами.

### Сборка и тесты

```bash
source /opt/ros/lyrical/setup.bash
colcon build --symlink-install
source install/setup.bash
python3 -m pytest src/patrol/test
```

### Запуск

```bash
# Терминал A: симулятор
ros2 launch turtle_bringup sim.launch.py

# Терминал B: нода patrol (относительный cmd_vel не связан с /turtle1/cmd_vel)
ros2 run patrol patrol

# Исправление связи через remap:
ros2 run patrol patrol --ros-args -r cmd_vel:=/turtle1/cmd_vel

# Проверки
ros2 node info /patrol
ros2 topic info /turtle1/cmd_vel --verbose
ros2 topic hz /turtle1/cmd_vel
```

После остановки ноды `Ctrl+C` дождитесь остановки turtlesim: исчезновение
процесса издателя — не команда торможения.

### CI

`.github/workflows/ci.yml`: полная сборка `colcon build --symlink-install`,
`colcon test` + `colcon test-result` и `check_practice.py PR03 --submission .`
с зафиксированным course-kit `v1-w10`.

ИИ использовался для генерации скриптов автоматизации сбора данных и настройки окружения distrobox.
