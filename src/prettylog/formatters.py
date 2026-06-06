"""Форматтеры: преобразуют LogRecord в строку (текст или JSON)."""

from __future__ import annotations

import json
from abc import ABC, abstractmethod


class BaseFormatter(ABC):
    """Абстрактный базовый класс для форматтеров.

    Форматтер знает *в каком формате* выводить, но не знает *куда* писать.
    """

    @abstractmethod
    def format(self, record: LogRecord) -> str:
        """Преобразует LogRecord в строку.

        Args:
            record: Запись лога для форматирования.

        Returns:
            Готовая строка для вывода.
        """


class TextFormatter(BaseFormatter):
    """Текстовый форматтер с человекочитаемым выводом.

    Формат: [2024-05-23 14:32:10] [INFO] [app] Server started
    Дополнительные поля: [2024-05-23 14:32:10] [INFO] [app] Login | user_id=42
    """

    def format(self, record: LogRecord) -> str:
        """Форматирует запись в текстовую строку."""
        # Подсказка 1: отформатируй timestamp в виде "YYYY-MM-DD HH:MM:SS"
        timestamp_str = record.timestamp.strftime("%Y-%m-%d %H:%M:%S")

        # Подсказка 2: базовая часть строки
        # Формат: [2024-05-23 14:32:10] [INFO] [app] Сообщение
        base = (
            f"[{timestamp_str}] [{record.level.name}] [{record.name}] {record.message}"
        )

        # TODO: Допиши обработку extra-полей
        # Подсказка 3: если record.extra не пустой — добавь через " | "
        # Пример: [2024-05-23 14:32:10] [INFO] [app] Login | user_id=42 ip=127.0.0.1
        # Используй: " ".join(f"{k}={v}" for k, v in record.extra.items())
        if record.extra:
            parts = []
            for key, value in record.extra.items():
                part = str(key) + "=" + str(value)  # "user_id=42"
                parts.append(part)  # кладем в список
            extra_parts = " ".join(parts)  # склеиваем
            base = base + " | " + extra_parts

        return base


class JsonFormatter(BaseFormatter):
    """JSON-форматтер для машинной обработки логов.

    Формат: {"timestamp": "2024-05-23T14:32:10", "level": "INFO",
             "logger": "app", "message": "...", "extra": {}}
    """

    def format(self, record: LogRecord) -> str:
        """Форматирует запись в JSON-строку."""
        # TODO: Создай словарь с полями записи
        # Подсказка 1: ключи должны быть "timestamp", "level", "logger", "message", "extra"
        # Подсказка 2: timestamp форматируй через .isoformat()
        # Подсказка 3: используй json.dumps() для преобразования словаря в строку
        # Подсказка 4: не забудь импортировать json в начале файла
        data = {
            "timestamp": record.timestamp.isoformat(),
            "level": record.level.name,
            "logger": record.name,
            "message": record.message,
            "extra": record.extra,
        }
        return json.dumps(data, ensure_ascii=False)
