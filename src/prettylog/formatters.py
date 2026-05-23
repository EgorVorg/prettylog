"""Форматтеры: преобразуют LogRecord в строку (текст или JSON)."""

from abc import ABC, abstractmethod

from prettylog.logger import LogRecord


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
        ...


class JsonFormatter(BaseFormatter):
    """JSON-форматтер для машинной обработки логов.

    Формат: {"timestamp": "2024-05-23T14:32:10", "level": "INFO",
             "logger": "app", "message": "...", "extra": {}}
    """

    def format(self, record: LogRecord) -> str:
        """Форматирует запись в JSON-строку."""
        ...
