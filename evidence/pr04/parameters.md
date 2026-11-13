# ПР04. Параметры: команды и вывод

Среда: distrobox, контейнер `ros2-lyrical` (ROS 2 Lyrical), `ROS_DOMAIN_ID=16`.
Запуск ноды (терминал B), симулятор — через launch (терминал A):

```bash
ros2 launch turtle_bringup sim.launch.py
ros2 run patrol patrol --ros-args -r cmd_vel:=/turtle1/cmd_vel
```

Параметры объявлены в `__init__` со значениями по умолчанию:
`publish_hz = 10.0`, `linear_speed = 0.5`, `turn_rate = 0.3`.
Допустимые конечные значения: частота 1–30 Гц, скорость 0–1 м/с,
поворот −1–1 рад/с (проверка — чистая функция
`patrol.command_logic.validate_parameters`).

## 1. Исходное состояние

```bash
ros2 param get /patrol publish_hz
# Double value is: 10.0

timeout 4 ros2 topic hz /turtle1/cmd_vel
# average rate: 10.000
#   min: 0.100s max: 0.100s std dev: 0.00016s window: 9
```

## 2. Допустимая смена частоты 10 → 5 Гц

```bash
ros2 param set /patrol publish_hz 5.0
# Set parameter successful
ros2 param get /patrol publish_hz
# Double value is: 5.0

timeout 4 ros2 topic hz /turtle1/cmd_vel
# average rate: 5.000
#   min: 0.200s max: 0.200s std dev: 0.00025s window: 4
```

Поток стал 5 Гц (период 0,2 с) — таймер пересоздан с периодом
`1/publish_hz`. Частота не 15 Гц, значит старого таймера не осталось:
post-set callback выполнил `timer.cancel()` + `destroy_timer` и создал
один новый.

## 3. Смена скорости без пересоздания таймера

```bash
ros2 param set /patrol linear_speed 0.7
# Set parameter successful
ros2 param get /patrol linear_speed
# Double value is: 0.7

timeout 4 ros2 topic hz /turtle1/cmd_vel
# average rate: 5.001
#   min: 0.199s max: 0.200s std dev: 0.00033s window: 4

ros2 topic echo /turtle1/pose --once
# x: 3.3606038093566895
# y: 8.983250617980957
# theta: -2.438370704650879
# linear_velocity: 0.699999988079071
# angular_velocity: 0.30000001192092896
```

Скорость изменилась (0,7 м/с видно в позе), период потока не изменился —
`tick` читает актуальные поля, таймер трогать не нужно.

## 4. Недопустимые значения отклоняются

```bash
ros2 param set /patrol publish_hz 0.0
# Setting parameter failed: publish_hz must be within [1, 30] Hz, got 0.0
ros2 param get /patrol publish_hz
# Double value is: 5.0

ros2 param set /patrol publish_hz -5.0
# Setting parameter failed: publish_hz must be within [1, 30] Hz, got -5.0

ros2 param set /patrol linear_speed 2.0
# Setting parameter failed: linear_speed must be within [0, 1] m/s, got 2.0

ros2 param set /patrol turn_rate -1.5
# Setting parameter failed: turn_rate must be within [-1, 1] rad/s, got -1.5

ros2 param set /patrol publish_hz nan
# Setting parameter failed: Wrong parameter type, expected '3' got '4'

timeout 4 ros2 topic hz /turtle1/cmd_vel
# average rate: 5.001
#   min: 0.200s max: 0.200s std dev: 0.00023s window: 4
```

on-set callback проверяет набор **до** изменения состояния: значение
сохранилось (5.0 Гц), активный таймер продолжает работать, поток не
изменился. NaN через CLI передать нельзя (CLI шлёт строку, а параметр —
double); случай NaN покрыт чистым тестом `test_nan_frequency_rejected`
(см. `tests.txt`).

## 5. Сбой: проверка временно отключена

Отдельная ветка `pr04-no-validation` (коммит
`0a17a169f7e2b467de8d6d6d1701a17bbe466c89`) — строка
`self.add_on_set_parameters_callback(self.validate)` закомментирована,
post-set callback на месте. Нода пересобрана и запущена, затем та же
команда:

```bash
ros2 param set /patrol publish_hz 0.0
```

Результат — воспроизводимый отказ:

1. Запрос `ros2 param set` не получает ответа и висит (я оборвал его
   таймаутом);
2. в логе ноды:

   ```
   File ".../patrol.py", line 76, in apply
       self.timer = self.create_timer(1.0 / self.publish_hz, self.tick)
                                  ~~~~^~~~~~~~~~~~~~~~~
   ZeroDivisionError: division by zero
   [ros2run]: Process exited with failure 1
   ```

3. нода завершилась с кодом 1 и исчезла из графа
   (`ros2 node list` — только `/turtlesim`);
4. поток `/turtle1/cmd_vel` остановился (новых сообщений нет),
   черепаха вскоре остановилась (скорости в позе обнулились).

## 6. Возврат проверки: тот же тест

Ветка `main` (проверка включена), нода пересобрана и запущена заново.
Тот же запуск — `ros2 param set /patrol publish_hz 0.0`:

```bash
ros2 param set /patrol publish_hz 0.0
# Setting parameter failed: publish_hz must be within [1, 30] Hz, got 0.0

ros2 param get /patrol publish_hz
# Double value is: 10.0

ros2 node list --no-daemon --spin-time 2
# /patrol
# /turtlesim

timeout 4 ros2 topic hz /turtle1/cmd_vel
# average rate: 10.000
#   min: 0.100s max: 0.100s std dev: 0.00025s window: 9
```

Отклонение мгновенное, значение осталось прежним (10.0 Гц — значение по
умолчанию для новой ноды), нода жива, поток идёт со старой частотой.

## 7. Сервис и action turtlesim

```bash
ros2 service call /clear std_srvs/srv/Empty
# requester: making request: std_srvs.srv.Empty_Request()
#
# response:
# std_srvs.srv.Empty_Response()
```

Пустой ответ подтверждает завершение вызова: сервер протёр след (сама поза
черепашки сохраняется).

```bash
ros2 action list -t
# /turtle1/rotate_absolute [turtlesim_msgs/action/RotateAbsolute]
```

Отличие запроса и цели: запрос сервиса — короткое «вопрос-ответ», клиент
ждёт единственный ответ и связь сразу разрывается. Цель action живёт дольше:
клиент отправляет цель, получает прогресс (feedback) по мере выполнения и
итоговый результат, а при желании может отменить цель до завершения.

## 8. Остановка

Ноду остановил `Ctrl+C`, launch — `Ctrl+C`: `turtlesim_node` завершился
штатно, `ros2 node list --no-daemon --spin-time 2` вернул пустой список.
