"""Конфигурация: создание логгера из Python-словаря (dict)."""

from prettylog.logger import Logger


def load_from_dict(config: dict) -> Logger:
    """Создаёт Logger из конфигурационного словаря.

    Реестры форматтеров и хендлеров задаются внутри функции.

    Args:
        config: Словарь конфигурации. Пример::

            {
                "name": "myapp",
                "level": "INFO",
                "handlers": [
                    {"type": "console", "formatter": "text"},
                    {
                        "type": "file",
                        "filename": "app.log",
                        "formatter": "json",
                        "max_bytes": 1048576,
                    },
                ],
            }

    Returns:
        Настроенный экземпляр Logger.

    Raises:
        ValueError: Если указан неизвестный тип хендлера или форматтера.
    """
    ...
