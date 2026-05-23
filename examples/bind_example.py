#!/usr/bin/env python3
"""Пример 3: Использование bind() для контекстного логирования.

Проверка: PYTHONPATH=src python examples/bind_example.py
Ожидаемый результат: строки с дополнительными полями user_id и ip
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from prettylog import get_logger


def main() -> None:
    logger = get_logger("api", level="INFO")

    print("=== Обычное логирование ===")
    logger.info("Сервер получил запрос")

    print("\n=== Логирование с контекстом через bind() ===")
    user_logger = logger.bind(user_id=42, ip="192.168.1.1")
    user_logger.info("Пользователь авторизовался")
    user_logger.warning("Попытка доступа к запрещённому ресурсу")

    print("\n=== Ещё один bind с дополнительными полями ===")
    admin_logger = user_logger.bind(role="admin")
    admin_logger.info("Админ открыл панель управления")

    print("\n=== Исходный логгер не изменился ===")
    logger.info("Обычное сообщение без контекста")

    print("\n=== bind с JSON форматтером ===")
    from prettylog import Logger, LogLevel, ConsoleHandler
    from prettylog.formatters import JsonFormatter

    json_logger = Logger(
        name="json_api",
        level=LogLevel.INFO,
        handlers=[ConsoleHandler(formatter=JsonFormatter())],
    )
    request_logger = json_logger.bind(request_id="abc-123")
    request_logger.info("Обработка запроса начата")


if __name__ == "__main__":
    main()
