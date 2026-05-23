#!/usr/bin/env python3
"""Пример 4: Демонстрация ротации логов.

Проверка: PYTHONPATH=src python examples/rotation_example.py
Ожидаемый результат: app.log + app.log.1 + app.log.2 после записи 1000 строк
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from prettylog import Logger, LogLevel, FileHandler
from prettylog.formatters import TextFormatter


def main() -> None:
    log_file = "rotation_test.log"
    max_bytes = 512

    for f in [log_file, f"{log_file}.1", f"{log_file}.2"]:
        if os.path.exists(f):
            os.remove(f)

    logger = Logger(
        name="rotator",
        level=LogLevel.DEBUG,
        handlers=[
            FileHandler(
                filename=log_file,
                formatter=TextFormatter(),
                max_bytes=max_bytes,
                backup_count=2,
            )
        ],
    )

    print(f"=== Записываем 1000 строк (max_bytes={max_bytes}) ===")
    for i in range(1000):
        logger.info(f"Сообщение номер {i:04d}: " + "x" * 50)

    print("\n=== Результат ротации ===")
    for f in [f"{log_file}.2", f"{log_file}.1", log_file]:
        if os.path.exists(f):
            size = os.path.getsize(f)
            lines = sum(1 for _ in open(f, encoding="utf-8"))
            print(f"  {f}: {size} bytes, {lines} lines")
        else:
            print(f"  {f}: не существует")

    for f in [log_file, f"{log_file}.1", f"{log_file}.2"]:
        if os.path.exists(f):
            os.remove(f)

    print("\nРотация работает!")


if __name__ == "__main__":
    main()
