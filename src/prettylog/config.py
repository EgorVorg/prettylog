"""Конфигурация: создание логгера из Python-словаря (dict)."""

from prettylog.formatters import JsonFormatter, TextFormatter
from prettylog.handlers import ConsoleHandler, FileHandler
from prettylog.logger import LogLevel, Logger


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
    # Шаг 1: Реестры (словари: имя → класс)

    formatter_registry = {
        "text": TextFormatter, #Без (): ссылка на класс, а не экземпляры, объект потом создается
        "json": JsonFormatter,
    }

    handler_registry = {
        "console": ConsoleHandler,
        "file": FileHandler,
    }

    # Шаг 2: Извлекаем параметры из словаря config
    # TODO: получи name (по умолчанию "root"), level, и список handlers_config
    # Подсказка: config.get("name", "root"), config.get("level", "INFO")
    #            config["handlers"] — это список словарей

    # config — словарь, который передали в функцию
    # .get() — метод «достать значение»
    # "name" — ключ, который ищем в словаре
    # "root" — значение по умолчанию — вернется, если ключа нет


    name = config.get("name", "root")
    level_string = config.get("level", "INFO")
    handlers_config = config.get("handlers", [])

    # Шаг 3: Конвертируем уровень

    level = LogLevel.from_string(level_string) # Строка "INFO" в LogLevel.INFO

    # Шаг 4: Собираем хендлеры
    handlers = []
    for handler_conf in handlers_config:
        handler_type = handler_conf.get("type") #достаем тип хендлера и имя форматтера
        formatter_name = handler_conf.get("formatter", "text")

        # защита от опечаток
        if handler_type not in handler_registry:
            raise ValueError(f"Неизвестный хендлер: {handler_type}")

        if formatter_name not in formatter_registry:
            raise ValueError(f"Неизвестный форматтер: {formatter_name}")
        
        # TODO: достань класс форматтера и создай экземпляр: formatter = FormatterClass()
        formatter_class = formatter_registry[formatter_name]
        formatter = formatter_class()

        # TODO: достань класс хендлера и создай экземпляр
        #        Если handler_type == "file" — передай filename из handler_conf
        #        В остальных случаях — handler_class(formatter=formatter)
        handler_class = handler_registry[handler_type]

        if handler_type == "file":
            filename = handler_conf.get("filename", "app.log") # либо ругаться с ошибкой
            max_bytes = handler_conf.get("max_bytes", 1_048_576)
            handler = handler_class(
                filename=filename,
                formatter=formatter,
                max_bytes=max_bytes,
            )
        else:
            handler = handler_class(formatter=formatter)

        handlers.append(handler)

    # Шаг 5: Создаём и возвращаем Logger
    # TODO: верни Logger(name=name, level=level, handlers=handlers)
    return Logger(
        name=name,
        level=level,
        handlers=handlers,
    )
