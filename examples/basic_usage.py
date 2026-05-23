#!/usr/bin/env python3
"""Пример 1: Базовое логирование с разными уровнями.

Проверка: python examples/basic_usage.py
Ожидаемый результат: 5 строк в консоли с разными цветами.
DEBUG не выводится (уровень INFO).
"""

from prettylog import get_logger


def main() -> None:
    # Создаём логгер с уровнем INFO
    logger = get_logger("app", level="INFO")

    print("=== Базовое логирование (уровень INFO) ===")
    logger.debug("Отладочная информация — НЕ выведется")
    logger.info("Сервер стартовал на порту 8080")
    logger.warning("Мало памяти: 85% использовано")
    logger.error("Не удалось подключиться к БД")
    logger.critical("Критическая ошибка — выход")

    # Создаём логгер с уровнем DEBUG
    print("\n=== Логирование с уровнем DEBUG ===")
    debug_logger = get_logger("debug_app", level="DEBUG")
    debug_logger.debug("Теперь отладка ВИДНА")
    debug_logger.info("Информация")

    # Проверка всех уровней
    print("\n=== Все уровни подряд ===")
    all_logger = get_logger("levels", level="DEBUG")
    all_logger.debug("DEBUG сообщение")
    all_logger.info("INFO сообщение")
    all_logger.warning("WARNING сообщение")
    all_logger.error("ERROR сообщение")
    all_logger.critical("CRITICAL сообщение")


if __name__ == "__main__":
    main()
