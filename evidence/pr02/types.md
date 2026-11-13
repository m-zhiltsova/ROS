# ПР02. Типы сообщений и топики

## Два основных топика turtlesim

| Топик | Тип | Назначение |
|---|---|---|
| `/turtle1/cmd_vel` | `geometry_msgs/msg/Twist` | Команда скорости: куда и как двигаться черепахе. Тurtlesim — подписчик |
| `/turtle1/pose` | `turtlesim_msgs/msg/Pose` (Lyrical; в Jazzy — `turtlesim/msg/Pose`) | Поза черепахи: координаты, угол, текущие скорости. Turtlesim — издатель |

Тип позы определён фактом из среды:

```bash
ros2 topic type /turtle1/pose
# turtlesim_msgs/msg/Pose
```

Дополнительно в графе: `/turtle1/color_sensor` (`turtlesim_msgs/msg/Color`),
`/parameter_events`, `/rosout`.

## `geometry_msgs/msg/Twist` (вывод `ros2 interface show`)

```
# This expresses velocity in free space broken into its linear and angular parts.

Vector3  linear
    float64 x
    float64 y
    float64 z
Vector3  angular
    float64 x
    float64 y
    float64 z
```

Назначение полей:

- `linear` — линейная скорость, м/с:
  - `linear.x` — вперёд/назад (в опыте `1.0` — движение вперёд);
  - `linear.y` — вбок (в turtlesim не используется, оставлено `0.0`);
  - `linear.z` — вверх/вниз (в 2D-симуляции не используется).
- `angular` — угловая скорость, рад/с:
  - `angular.z` — поворот вокруг вертикальной оси (yaw); в turtlesim
    положительное значение — против часовой стрелки (в опыте `0.5`, черепашка
    пошла по дуге, `theta` росло);
  - `angular.x`/`angular.y` — крен/тангаж, в 2D-симуляции не используются.

## `turtlesim_msgs/msg/Pose` (по фактическому выводу `echo`)

```
x: 5.544444561004639
y: 5.544444561004639
theta: 0.0
linear_velocity: 0.0
angular_velocity: 0.0
```

- `x`, `y` — координаты черепахи в мире turtlesim, м;
- `theta` — ориентация, рад (0 — вправо вдоль +X, положительное — против
  часовой стрелки);
- `linear_velocity`, `angular_velocity` — текущие скорость и угловая скорость.

## QoS (из `ros2 topic info /turtle1/cmd_vel --verbose`)

Обе стороны топика `RELIABLE`, `VOLATILE`: у издателя CLI `KEEP_LAST (10)`,
у подписки turtlesim `KEEP_LAST (7)` — профили совместимы, доставка возможна.
Type hash топика: `RIHS01_9c45bf16fe0983d80e3cfe750d6835843d265a9a6c46bd2e609fcddde6fb8d2a`
— одинаков и у `/cmd_vel` (в опыте со сбоем), и у `/turtle1/cmd_vel`: тип не
мешал доставке, мешало другое полное имя.
