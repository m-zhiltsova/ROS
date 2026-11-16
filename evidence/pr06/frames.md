# ПР06. Дерево систем координат (course_ackermann)

Описание: `src/course_description/urdf/vehicle.urdf.xacro`, размеры — из
`.course-kit/v1/models/course_ackermann/model.sdf`. Разворот:
`xacro vehicle.urdf.xacro > /tmp/vehicle.urdf`, проверка — `check_urdf`
(результат в `model-check.txt`): дерево связано, корень — `base_link`,
циклов нет.

Изображение: `view_frames.pdf` (tf2_tools view_frames) — то же дерево,
которое видит tf2-граф.

## Звенья и сочленения

| Сочленение | Тип | Родитель | Потомок | xyz (м) | rpy (рад) | Кто публикует |
|---|---|---|---|---|---|---|
| `camera_joint` | fixed | `base_link` | `camera_link` | 0.28 0 0.38 | 0 0 0 | `robot_state_publisher` → `/tf_static` |
| `lidar_joint` | fixed | `base_link` | `lidar_link` | 0.28 0 0.38 | 0 0 0 | `robot_state_publisher` → `/tf_static` |
| `imu_joint` | fixed | `base_link` | `imu_link` | 0.28 0 0.38 | 0 0 0 | `robot_state_publisher` → `/tf_static` |
| `front_left_wheel_joint` | continuous | `base_link` | `front_left_wheel` | 0.40 0.31 0 | 1.5708 0 0 | через `/tf` — только при публикациях `joint_states` |
| `front_right_wheel_joint` | continuous | `base_link` | `front_right_wheel` | 0.40 −0.31 0 | 1.5708 0 0 | через `/tf` — только при публикациях `joint_states` |
| `rear_left_wheel_joint` | continuous | `base_link` | `rear_left_wheel` | −0.40 0.31 0 | 1.5708 0 0 | через `/tf` — только при публикациях `joint_states` |
| `rear_right_wheel_joint` | continuous | `base_link` | `rear_right_wheel` | −0.40 −0.31 0 | 1.5708 0 0 | через `/tf` — только при публикациях `joint_states` |

Координаты колёс заданы через Xacro-переменные: `x = ±wheelbase/2`
(`wheelbase = 0.8`), `y = ±track/2` (`track = 0.62`), радиус `0.12`.

## Ожидаемые преобразования (проверено tf2_echo, запуск rsp)

Выписки фактических выводов — в `tf2-echo.txt`.

- `tf2_echo base_link lidar_link` → Translation `[0.280, 0.000, 0.380]`,
  поворот единичный;
- `tf2_echo base_link camera_link` → `[0.280, 0.000, 0.380]`;
- `tf2_echo base_link imu_link` → `[0.280, 0.000, 0.380]`;
- `tf2_echo base_link front_left_wheel` → «frame does not exist», пока
  никто не публикует `joint_states` (continuous-сочленения — подвижные,
  их значения не могут вытекать из URDF).

## Дефект (ветка `pr06-lidar-parent`)

В отдельной ветке `lidar_joint` указывает `parent = camera_link` при том же
`origin`. `check_urdf` такую модель принимает (дерево связано), но лидар
оказывается в точке `(0.28+0.28, 0, 0.38+0.38) = (0.56, 0, 0.76)` вместо
`(0.28, 0, 0.38)` — видно в `tf2_echo base_link lidar_link`. Тест
`test_sensor_joints_are_fixed_to_base_link` падает именно на этом смене
родителя: числа описания проверяет тест, а не `check_urdf`.
