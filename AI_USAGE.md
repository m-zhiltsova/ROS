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
