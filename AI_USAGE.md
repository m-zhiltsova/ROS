# Декларация использования ИИ

## PR01

ИИ использовался для генерации скриптов автоматизации сбора данных и настройки окружения distrobox.

## PR02

| Модель | Инструмент / среда | Компонент | Характер помощи | Как проверено |
|---|---|---|---|---|
| Qwen3.8-27B | opencode (CLI-агент) | пакет `turtle_bringup` (описания в `package.xml`/`setup.py`), workflow `ci.yml`, `README.md`, `evidence/pr02/` | Разбор условия ПР02 и лекции, доработка метаданных пакета и CI, выполнение опыта в контейнере `ros2-lyrical` с фиксацией фактических выводов, написание `commands.md`, `types.md`, `report.json` | Локальный прогон `check_practice.py PR02 --submission .`; повторная сборка `turtle_bringup` в контейнере; повтор всех команд опыта в трёх терминалах; движение черепахи подтверждено `ros2 topic echo /turtle1/pose` до/после команды |

## PR03

| Модель | Инструмент / среда | Компонент | Характер помощи | Как проверено |
|---|---|---|---|---|
| Qwen3.8-27B | opencode (CLI-агент) | `src/patrol` (метаданные `package.xml`/`setup.py`), `src/turtle_bringup` (flake8-исправления), workflow `ci.yml`, `README.md`, `evidence/pr03/` | Разбор условия ПР03 и лекции 03, исправление flake8-ошибок (порядок импортов, E302, E501), перенастройка CI на полный цикл build+test и `check_practice.py PR03`, выполнение опыта в контейнере `ros2-lyrical` (сбой без remap, исправление с remap, замер `topic hz`), написание `demo.md`, `tests.txt`, `report.json` | `colcon test` по workspace (12 tests, 0 failures) и `pytest` пакета patrol; повтор всех команд опыта в контейнере; движение и остановка черепахи подтверждены `ros2 topic echo /turtle1/pose`; локальный прогон `check_practice.py PR03 --submission .` |

## PR04

| Модель | Инструмент / среда | Компонент | Характер помощи | Как проверено |
|---|---|---|---|---|
| Qwen3.8-27B | opencode (CLI-агент) | `src/patrol` (параметры, on/post-set callbacks, `validate_parameters` в `command_logic.py`, `test_parameter_logic.py`), workflow `ci.yml`, `README.md`, `evidence/pr04/`, побочная ветка `pr04-no-validation` | Разбор условия ПР04 и лекции 04, реализация параметров и пересоздания таймера, чистые тесты валидации, дефектный коммит на отдельной ветке, выполнение опыта в контейнере `ros2-lyrical` (смена 10→5 Гц, отклонения, сбой на нуле, возврат проверки, `/clear` и `action list`), написание `parameters.md`, `tests.txt`, `report.json` | `colcon test` по workspace (23 tests, 0 failures) и `pytest` (17 passed); повтор всех команд `ros2 param set/get` и `topic hz` в контейнере; воспроизведение сбоя на ветке и его отклонение на main; локальный прогон `check_practice.py PR04 --submission .` |

Дополнение 16.11.2026 (коммит `7e00f1a4`): mypy-тест ограничен каталогом
собственного пакета (`test_mypy.py` в `patrol` и `turtle_bringup`), чтобы
команда из инструкции `python3 -m pytest src/patrol/test` проходила и из
корня workspace; проверено pytest из корня и из пакета, `colcon test`
(23 tests, 0 failures) и полный живой прогон параметров в контейнере.

## PR05

| Модель | Инструмент / среда | Компонент | Характер помощи | Как проверено |
|---|---|---|---|---|
| Qwen3.8-27B | opencode (CLI-агент) | `src/course_bringup` (launch `patrol.launch.py`, нода `pose_relay`, `qos_config.py`, тесты), `config/qos-overrides.yaml`, `setup.cfg`, `.gitignore`, workflow `ci.yml`, `README.md`, `evidence/pr05/` | Разбор условия ПР05 и лекции 05, реализация launch с аргументами/namespace/remaps/IfCondition-recorder, нода relay с best-effort-издателем и настраиваемым probe-подписчиком, выполнение опыта в контейнере `ros2-lyrical` (дефект reliable-подписчика, исправление, запись MCAP, replay с override, проверка record:=true), написание `qos-before.txt`, `qos-after.txt`, `tests.txt`, `report.json` | `colcon test` по workspace (32 tests, 0 failures) и `pytest` (8 passed); повтор всех команд `ros2 launch/echo/bag` в контейнере с фиксацией фактических выводов и кодов возврата; локальный прогон `check_practice.py PR05 --submission .` |

## PR06

| Модель | Инструмент / среда | Компонент | Характер помощи | Как проверено |
|---|---|---|---|---|
| Qwen3.8-27B | opencode (CLI-агент) | `src/course_description` (xacro-модель, launch, `test_frames.py`), workflow `ci.yml`, `README.md`, `evidence/pr06/` | Разбор условия ПР06 и лекции 06, Xacro-описание Ackermann-робота по размерам course-kit SDF (макросы колеса/сенсора, параметризация, инерции по формулам), launch `robot_state_publisher`, структурный тест дерева (родители, связность, физичность инерций), опыт в контейнере `ros2-lyrical` (tf2_echo, QoS `/tf_static`, view_frames), дефект-ветка `pr06-lidar-parent` и её фиксация, написание `frames.md`, `model-check.txt`, `tf-qos.txt`, `tf2-echo.txt`, `defect-demo.txt`, `report.json` | `colcon test` по workspace (41 tests, 0 failures) и `pytest` (8 passed); повтор всех команд `xacro/check_urdf/ros2 launch/tf2_echo/topic echo` в контейнере с фиксацией фактических выводов; локальный прогон `check_practice.py PR06 --submission .` |
