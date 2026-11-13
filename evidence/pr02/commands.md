# ПР02. Команды и наблюдения

Среда: distrobox, контейнер `ros2-lyrical` (образ `osrf/ros`, ROS 2 Lyrical,
Ubuntu), `/home/lila` на хосте смонтирован в контейнере как `/work`.
Корень workspace = корень репозитория: `/work/ros_labs/ROS`
(`/home/lila/ros_labs/ROS` на хосте). Домен: `ROS_DOMAIN_ID=16`.

Каждый терминал начинал с:

```bash
source /opt/ros/lyrical/setup.bash
export ROS_DOMAIN_ID=16
cd /work/ros_labs/ROS        # из корня workspace
```

Для терминалов запуска/сборки дополнительно: `source install/setup.bash`.

## 1. Три Linux-команды

| Точная команда | Назначение | Мой результат |
|---|---|---|
| `pwd` | Показать каталог, в котором сейчас оболочка | `/work/ros_labs/ROS` — подтвердил, что работаю из корня workspace; на хосте тот же путь — `/home/lila/ros_labs/ROS` |
| `mkdir -p evidence/pr02` | Создать каталог для результатов, включая вложенные; не ошибиться, если каталог уже есть | код возврата 0, каталог `evidence/pr02/` существует, сюда сохраняются `build*.txt`, `commands.md`, `types.md`, `report.json` |
| `cat evidence/pr02/build.txt` | Прочитать содержимое файла целиком | `Starting >>> turtle_bringup` / `Finished <<< turtle_bringup [1.98s]` / `Summary: 1 package finished [2.10s]` |

### Чем `>` отличается от `|`

- `>` перенаправляет stdout **в файл**, заменяя прежнее содержимое. С добавлением
  `2>&1` stderr попадает туда же. Использовал:
  `colcon build --symlink-install --packages-select turtle_bringup 2>&1 | tee evidence/pr02/build.txt`
  — здесь и то и другое: `|` ведёт stdout конвейера в `tee`, а `tee` одновременно
  показывает вывод в терминале и записывает его в файл.
- `|` (pipe) передаёт stdout **следующей команде** конвейера, файл при этом не
  создаётся. Например, `set -o pipefail` сохраняет ненулевой статус `colcon`
  при ошибке, даже если `tee` в конце конвейера завершился успешно.

### Чем `source` отличается от запуска новой программы

- `source /opt/ros/lyrical/setup.bash` выполняет скрипт **в текущей оболочке**:
  переменные (`PATH`, `AMENT_PREFIX_PATH`, `ROS_DISTRO`) остаются в этом
  терминале. Вывод `printenv ROS_DISTRO ROS_DOMAIN_ID` после source и export:
  `lyrical` / `16`.
- Запуск новой программы (`ros2 run ...`, `colcon build`) создаёт отдельный
  процесс с собственным окружением; изменения переменных внутри него не влияют
  на текущий терминал. Чтобы настройка дошла до дочерних процессов, её нужно
  задать через `export` (как `export ROS_DOMAIN_ID=16`).

## 2. Пакет и сборка

Пакет `turtle_bringup` создавался командой из условия:

```bash
ros2 pkg create --build-type ament_python --license Apache-2.0 \
  turtle_bringup --dependencies launch launch_ros turtlesim
```

1. Пустой пакет (без launch) собран, лог — `evidence/pr02/build-empty.txt`.
   После `source install/setup.bash`:

   ```bash
   ros2 pkg prefix turtle_bringup
   # /work/ros_labs/ROS/install/turtle_bringup
   ```

   Путь ведёт в `install` workspace (у turtlesim, установленного в системе, —
   `/opt/ros/lyrical`). Пустой пакет найден, но нод не появилось: сборка и
   `source` не запускают процессы.
2. После добавления `launch/sim.launch.py` и записи в `data_files` в `setup.py`
   пакет пересобран, лог — `evidence/pr02/build.txt`. Установленный ресурс
   на месте:

   ```bash
   ls "$(ros2 pkg prefix turtle_bringup)/share/turtle_bringup/launch"
   # sim.launch.py
   ```

## 3. Запуск, проверка графа, остановка

Терминал A:

```bash
ros2 launch turtle_bringup sim.launch.py
```

Открылось одно окно turtlesim. Терминал B:

```bash
ros2 node list --no-daemon --spin-time 2
# /turtlesim

ros2 topic list -t
# /parameter_events [rcl_interfaces/msg/ParameterEvent]
# /rosout [rcl_interfaces/msg/Log]
# /turtle1/cmd_vel [geometry_msgs/msg/Twist]
# /turtle1/color_sensor [turtlesim_msgs/msg/Color]
# /turtle1/pose [turtlesim_msgs/msg/Pose]
```

Остановка: `Ctrl+C` в терминале A (SIGINT). Конец лога launch:

```
[WARNING] [launch]: user interrupted with ctrl-c (SIGINT)
[INFO] [turtlesim_node-1]: sending signal 'SIGINT' to process[turtlesim_node-1]
[INFO] [turtlesim_node-1]: process has finished cleanly [pid 108642]
```

Процесс `turtlesim_node` завершился, `ros2 node list --no-daemon --spin-time 2`
вернул пустой список: запущенный launch завершает своих дочерних процессов.

## 4. Команда и движение

Тип позы и начальные координаты (терминал C):

```bash
ros2 topic type /turtle1/pose
# turtlesim_msgs/msg/Pose

ros2 topic echo /turtle1/pose --once
# x: 5.544444561004639
# y: 5.544444561004639
# theta: 0.0
# linear_velocity: 0.0
# angular_velocity: 0.0
```

(В этой версии turtlesim точка спавна в данном запуске — (5.544, 5.544, 0.0);
лодж: `Spawning turtle [turtle1] at x=[5.544445], y=[5.544445], theta=[0.000000]`.)

Ожидание: `linear.x = 1.0` — движение вперёд, `angular.z = 0.5` — поворот
против часовой стрелки; черепаха должна пройти дугу вправо-наверх (theta
растёт). Факт, через ~2 с после одной публикации:

```bash
ros2 topic pub --once /turtle1/cmd_vel geometry_msgs/msg/Twist \
  '{linear: {x: 1.0}, angular: {z: 0.5}}'

ros2 topic echo /turtle1/pose --once
# x: 6.509308815002441
# y: 5.796990871429443
# theta: 0.5040000081062317
# linear_velocity: 0.0
# angular_velocity: 0.0
```

Направление совпало с ожиданием: x и y выросли, theta стал положительным
(дуга против часовой). Повторный echo через 2 с показал ту же позу — одна
публикация не задаёт бесконечное движение: без новых команд turtlesim
останавливается (скорости в позе — 0).

## 5. Сбой и исправление (до / сбой / после)

**До (только launch, издателей нет):** `/cmd_vel` отсутствует в
`ros2 topic list -t`; у `/turtle1/cmd_vel` — `Publisher count: 0`,
`Subscription count: 1` (подписка turtlesim).

**Сбой.** В терминале B запущен издатель с неверным именем:

```bash
ros2 topic pub --rate 1 --wait-matching-subscriptions 0 \
  /cmd_vel geometry_msgs/msg/Twist '{linear: {x: 1.0}, angular: {z: 0.5}}'
```

`--wait-matching-subscriptions 0` разрешает публиковать без подписчиков
(с `--once` команда в таком топике ждала бы подписчика вечно, поэтому опыт
ведётся непрерывной публикацией). Пока издатель работал, в терминале C:

```bash
ros2 topic info /cmd_vel --verbose
# Type: geometry_msgs/msg/Twist
# Publisher count: 1          # Node name: _ros2cli_109276
# Subscription count: 0

ros2 topic info /turtle1/cmd_vel --verbose
# Type: geometry_msgs/msg/Twist
# Publisher count: 0
# Subscription count: 1       # Node name: turtlesim
```

Издатель виден в графе, но подписчика turtlesim у топика `/cmd_vel` нет, а у
`turtlesim` подписка — только на `/turtle1/cmd_vel`. Поза не изменилась за
наблюдаемое время — движение не произошло.

**После.** Издатель остановлен (`Ctrl+C`), изменено **только** имя топика —
`/cmd_vel` → `/turtle1/cmd_vel`; скорость и домен не тронуты:

```bash
ros2 topic pub --rate 1 --wait-matching-subscriptions 0 \
  /turtle1/cmd_vel geometry_msgs/msg/Twist '{linear: {x: 1.0}, angular: {z: 0.5}}'

ros2 topic info /turtle1/cmd_vel --verbose
# Type: geometry_msgs/msg/Twist
# Publisher count: 1          # Node name: _ros2cli_109596
# Subscription count: 1       # Node name: turtlesim
```

Черепаха поехала: в `echo /turtle1/pose` скорости `linear_velocity: 1.0`,
`angular_velocity: 0.5`, координаты менялись от echo к echo. Издатель
остановлен, отправлен нулевой Twist (`'{}'`), черепаха остановилась
(финальная поза: x=7.114, y=8.774, theta=2.229, скорости 0).

## 6. Почему правильного типа сообщения недостаточно

Обнаружение в DDS сопоставляет конечные точки по трём признакам: **полное имя
топика, тип и QoS**. У обоих топиков тип одинаков — `geometry_msgs/msg/Twist`
(одинаков даже type hash `RIHS01_9c45bf16...` в выводе `--verbose`), и QoS
совместим (RELIABLE). Но `/cmd_vel` и `/turtle1/cmd_vel` — разные полные имена,
поэтому издатель на `/cmd_vel` не находит ни одного подписчика
(`Subscription count: 0`), и сообщения никуда не доставляются, даже издатель
«на месте». `ros2 topic list`/`info` показывают только **обнаруженные**
конечные точки; **доставка** происходит только между издателем и подписчиком,
сопоставленными по всем трём признакам. Обнаружение — необходимое, но не
достаточное условие связи.
