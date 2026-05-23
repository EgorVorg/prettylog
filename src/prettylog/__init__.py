"""prettylog — простая библиотека логирования с нуля.

Пример использования::

    from prettylog import get_logger

    logger = get_logger("myapp", level="INFO")
    logger.info("Привет, мир!")
    logger.debug("Это не выведется — уровень INFO выше DEBUG")

    # Привязка дополнительных полей
    user_logger = logger.bind(user_id=42)
    user_logger.info("Пользователь вошёл")  # в выводе будет user_id=42

    # Конфигурация через dict
    from prettylog import load_from_dict

    cfg = {
        "level": "DEBUG",
        "handlers": [
            {"type": "console", "formatter": "text"},
            {"type": "file", "filename": "app.log", "formatter": "json"},
        ],
    }
    logger = load_from_dict(cfg)
"""

from prettylog.config import load_from_dict
from prettylog.formatters import JsonFormatter, TextFormatter
from prettylog.handlers import ConsoleHandler, FileHandler
from prettylog.logger import LogLevel, LogRecord, Logger

__all__ = [
    "get_logger",
    "Logger",
    "LogLevel",
    "LogRecord",
    "ConsoleHandler",
    "FileHandler",
    "TextFormatter",
    "JsonFormatter",
    "load_from_dict",
]


def get_logger(
    name: str = "root",
    level: str = "INFO",
    handlers: list | None = None,
) -> Logger:
    """Фабричная функция для быстрого создания логгера.

    Если хендлеры не указаны — создаёт ConsoleHandler с TextFormatter.

    Args:
        name: Имя логгера.
        level: Уровень логирования (строка, например "INFO" или "debug").
        handlers: Список хендлеров. None → один ConsoleHandler.

    Returns:
        Настроенный экземпляр Logger.
    """
    ...
