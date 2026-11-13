# ПР03. Демонстрация ноды patrol

Среда: distrobox, контейнер `ros2-lyrical` (ROS 2 Lyrical), `ROS_DOMAIN_ID=16`.
Корень workspace = корень репозитория. Каждый терминал начинал с:

```bash
source /opt/ros/lyrical/setup.bash
source install/setup.bash   # после colcon build
export ROS_DOMAIN_ID=16
cd /work/ros_labs/ROS
```

## 1. Сборка и тесты

```bash
colcon build --symlink-install
python3 -m pytest src/patrol/test   # из каталога пакета, см. tests.txt
colcon test --event-handlers console_direct+
colcon test-result --verbose        # 12 tests, 0 errors, 0 failures, 2 skipped
```

Нода `patrol` (файл `patrol/patrol.py`):

- подписка `self.pose_sub` на `/turtle1/pose` (`turtlesim_msgs/msg/Pose`) —
  callback `on_pose` **только сохраняет** сообщение в поле `self.latest_pose`;
- таймер 0,1 с вызывает `tick`, который публикует `compute_command(latest_pose)`;
- издатель — в **относительный** топик `cmd_vel`;
- чистая функция `compute_command` (`patrol/command_logic.py`): без позы —
  нулевая команда, с позой — `linear.x = 0.5`, `angular.z = 0.3`.

## 2. Роли init, spin, callback и Ctrl+C

- `rclpy.init(args=args)` — инициализация контекста ROS для процесса (создаёт
  граф, DDS-домен из `ROS_DOMAIN_ID`); без него нода не может ни публиковать,
  ни подписываться.
- `rclpy.spin(node)` — запуск исполнительного цикла: executor ждёт события
  (сообщение по подписке, истечение таймера) и вызывает соответствующий
  callback. Пока `spin` крутится, нода «живёт»: callback `on_pose` обновляет
  `latest_pose`, таймер каждые 0,1 с вызывает `tick` и публикует команду.
  Само сообщение callback не шлёт — оно лишь готовит данные, публикацию делает
  `tick`.
- `Ctrl+C` — SIGINT превращается в `KeyboardInterrupt` внутри `main`; блок
  `finally` вызывает `node.destroy_node()` (убирает конечные точки из графа) и
  `rclpy.try_shutdown()` (закрывает контекст), процесс завершается штатно.

## 3. Запуск и сбой: относительный `cmd_vel` не связан с симулятором

Терминал A: `ros2 launch turtle_bringup sim.launch.py` (тurtlesim запущен,
начальная поза x=5.544, y=5.544, theta=0.0). Терминал B:

```bash
ros2 run patrol patrol
```

Нода в графе:

```
ros2 node list --no-daemon --spin-time 2
# /patrol
# /turtlesim

ros2 node info /patrol
# /patrol
#   Subscribers:
#     /turtle1/pose: turtlesim_msgs/msg/Pose
#   Publishers:
#     /cmd_vel: geometry_msgs/msg/Twist
#     ...
```

Относительное имя `cmd_vel` у ноды в корне графа разрешается в `/cmd_vel` —
не в `/turtle1/cmd_vel`. Сравнение конечных точек:

```
ros2 topic info /cmd_vel --verbose
# Type: geometry_msgs/msg/Twist
# Publisher count: 1          # Node name: patrol
# Subscription count: 0

ros2 topic info /turtle1/cmd_vel --verbose
# Type: geometry_msgs/msg/Twist
# Publisher count: 0
# Subscription count: 1       # Node name: turtlesim
```

Издатель `patrol` публикует (10 Гц), но у его топика нет подписчиков, а
подписка turtlesim ждёт другой топик. Поза черепахи за несколько секунд не
изменилась:

```
ros2 topic echo /turtle1/pose --once   # дважды, с интервалом 3 с
# x: 5.544444561004639  y: 5.544444561004639  theta: 0.0
# linear_velocity: 0.0  angular_velocity: 0.0
```

Ноду остановил `Ctrl+C`; `ros2 node list` снова показал только `/turtlesim`.

## 4. Исправление через remap

Запуск с тем же кодом, но с переопределением имени:

```bash
ros2 run patrol patrol --ros-args -r cmd_vel:=/turtle1/cmd_vel
```

```
ros2 topic info /turtle1/cmd_vel --verbose
# Type: geometry_msgs/msg/Twist
# Publisher count: 1          # Node name: patrol
# Subscription count: 1       # Node name: turtlesim
```

Издание и подписка сопоставились (тип и QoS совпали ещё на прошлом шаге,
добавилось только имя). Черепаха движется:

```
ros2 topic echo /turtle1/pose --once
# x: 7.095289707183838  y: 6.610907554626465  theta: 1.2000000476837158
# linear_velocity: 0.5  angular_velocity: 0.30000001192092896
```

## 5. Измерение реальной частоты команды (10 с)

```bash
timeout 10 ros2 topic hz /turtle1/cmd_vel
# average rate: 9.999 ... 10.000
#   min: 0.100s max: 0.100s std dev: 0.00021s window: 89
```

Средняя частота ≈ 10 Гц, период 0,100 с — совпадает с таймером 0,1 с.
(Строка `failed to initialize wait set ...` в конце — артефакт завершения
`ros2 topic hz` по таймауту, не ошибка ноды.)

## 6. Остановка ноды и остановка черепахи

Ноду остановил `Ctrl+C` (SIGINT → `destroy_node()` + `try_shutdown()`).
Исчезновение процесса издателя — не команда торможения: дождись, пока
черепашка остановится, и проверь позу:

```
ros2 topic echo /turtle1/pose --once   # несколько раз с интервалом 1 с
# x: 6.977123260498047  y: 6.366278171539307  theta: 1.0368146896362305
# linear_velocity: 0.0  angular_velocity: 0.0
```

После потери издателя скорости обнулились и поза перестала меняться —
черепашка остановилась (повторно проверил через 3 с: та же поза). В этой
версии turtlesim скорость сбрасывается, когда издатель `cmd_vel`
исчезает/перестаёт присылать команды, но остановка не мгновенна: в
проверке после `Ctrl+C` нужно именно подождать и убедиться, что
`linear_velocity` и `angular_velocity` равны нулю, а не просто увидеть, что
нода исчезла из `node list`.

Завершил launch `Ctrl+C`: `turtlesim_node` завершился штатно,
`ros2 node list --no-daemon --spin-time 2` вернул пустой список.
