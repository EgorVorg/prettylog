#!/usr/bin/env python3
"""Пример 2: Создание логгера из конфигурационного словаря.

Проверка: PYTHONPATH=src python examples/config_example.py
Ожидаемый результат: цветные строки в консоли + JSON-логи в app.log
"""

import os
import sys

# Добавляем src в путь чтобы импортировать prettylog
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from prettylog import load_from_dict


def main() -> None:
    log_file = "app.log"
    for f in [log_file, f"{log_file}.1", f"{log_file}.2"]:
        if os.path.exists(f):
            os.remove(f)

    config = {
        "name": "config_app",
        "level": "DEBUG",
        "handlers": [
            {"type": "console", "formatter": "text"},
            {
                "type": "file",
                "filename": log_file,
                "formatter": "json",
                "max_bytes": 1024,
            },
        ],
    }

    logger = load_from_dict(config)

    print("=== Логгер из конфигурации ===")
    logger.info("Привет из конфигурированного логгера!")
    logger.debug("Отладочное сообщение в JSON")
    logger.warning("Предупреждение тоже в JSON")

    print(f"\n=== Содержимое {log_file} ===")
    if os.path.exists(log_file):
        with open(log_file, encoding="utf-8") as f:
            print(f.read())

    for f in [log_file, f"{log_file}.1", f"{log_file}.2"]:
        if os.path.exists(f):
            os.remove(f)


if __name__ == "__main__":
    main()
