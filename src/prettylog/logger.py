"""Ядро логгера: уровни, записи и основной класс Logger."""

from dataclasses import dataclass, field
from datetime import datetime
from enum import IntEnum

from prettylog.handlers import BaseHandler


class LogLevel(IntEnum):
    """Уровни логирования. Чем выше число — тем серьезнее сообщение."""

    DEBUG = 10
    INFO = 20
    WARNING = 30
    ERROR = 40
    CRITICAL = 50

    @classmethod # работает с целым классом cls, а не экземпляром LogLevel.INFO
    def from_string(cls, name: str) -> "LogLevel":
        """Преобразует строку в LogLevel (регистронезависимо).

        Args:
            name: Название уровня, например "info" или "ERROR".

        Raises:
            ValueError: Если передан неизвестный уровень.
        """
        name_upper = name.upper()
        if name_upper not in cls.__members__:
            raise ValueError(f"Unknown log level: {name}")
        return cls[name_upper] # cls["INFO"] вернет LogLevel.INFO


@dataclass # питон сам делает всякие иниты
class LogRecord: # конверт для одного сообщения лога
    """Одна запись лога — неизменяемая структура с данными."""

    name: str
    level: LogLevel
    message: str
    module: str
    timestamp: datetime
    extra: dict = field(default_factory=dict) # пустой словарь для каждого LogRecord


class Logger:
    """Основной класс логгера.

    Logger не знает, куда писать — он делегирует это хендлерам.
    Logger не знает, в каком формате — это задача форматтера.
    """

    def __init__(
        self,
        name: str,
        level: LogLevel,
        handlers: list[BaseHandler],
        extra: dict | None = None,
    ) -> None:
        """
        Args:
            name: Имя логгера (например, "app" или "db").
            level: Минимальный уровень для обработки сообщений.
            handlers: Список хендлеров, куда отправлять записи.
            extra: Дополнительные поля, прикреплённые к этому логгеру.
        """
        self.name = name
        self.level = level
        self.handlers = handlers
        self.extra = extra or {}

    def debug(self, msg: str) -> None:
        """Логирует сообщение уровнем DEBUG."""
        # TODO: вызвать _log() с правильным уровнем
        ...
        self._log(LogLevel.DEBUG, msg)

    def info(self, msg: str) -> None:
        """Логирует сообщение уровнем INFO."""
        # TODO: вызвать _log() с правильным уровнем
        ...
        self._log(LogLevel.INFO, msg)

    def warning(self, msg: str) -> None:
        """Логирует сообщение уровнем WARNING."""
        # TODO: вызвать _log() с правильным уровнем
        ...
        self._log(LogLevel.WARNING, msg)

    def error(self, msg: str) -> None:
        """Логирует сообщение уровнем ERROR."""
        # TODO: вызвать _log() с правильным уровнем
        ...
        self._log(LogLevel.ERROR, msg)

    def critical(self, msg: str) -> None:
        """Логирует сообщение уровнем CRITICAL."""
        # TODO: вызвать _log() с правильным уровнем
        ...
        self._log(LogLevel.CRITICAL, msg)

    def _log(self, level: LogLevel, msg: str) -> None: # _ — внутренний метод
        """Внутренний метод обработки сообщения.

        Порядок работы:
        1. Проверить, что level >= self.level (иначе молча выйти).
        2. Создать LogRecord с текущим timestamp.
        3. Смержить self.extra с полями записи.
        4. Отправить запись каждому хендлеру через handler.emit(record).
        """
        # Шаг 1: Фильтрация по уровню. Если уровень сообщения ниже минимального — выходим
        if level < self.level:
            return

        # Шаг 2: Создаём запись лога. Для имени модуля используем __name__ вызывающего.
        # Подсказка: inspect.stack() или просто захардкодить "module" пока
        import inspect

        frame = inspect.currentframe()
        module_name = "unknown"
        if frame and frame.f_back:
            module_name = frame.f_back.f_globals.get("__name__", "unknown")

        record = LogRecord(
            name=self.name,
            level=level,
            message=msg,
            module=module_name,
            timestamp=datetime.now(),
            # Создаём копию extra, чтобы не модифицировать оригинал
            extra=dict(self.extra),
        )

        # Шаг 3: Отправляем запись каждому хендлеру
        for handler in self.handlers:
            handler.emit(record)

    def bind(self, **kwargs: object) -> "Logger": # логгер с доп. данными, не трогает старый, как копия документа
        """Создаёт новый Logger с замёрженными extra-полями.

        Исходный логгер не модифицируется — чистая функция.

        Example:
            user_logger = logger.bind(user_id=42)
            user_logger.info("login")  # в extra будет user_id=42
        """
        # TODO: создать новый словарь extra, объединив self.extra и kwargs
        # Подсказка: сделай копию self.extra и обнови через .update(kwargs)
        # Затем создай новый Logger с теми же параметрами, но новым extra
        ...
        new_extra = dict(self.extra) # копирует старые экстра
        new_extra.update(kwargs) # добавляет новые. Хз что за kwargs, не понял

        # self.name = name в __init__ — ПРИНИМАЕМ параметр от юзера и КЛАДЕМ в объект
        # name=self.name при создании нового объекта — БЕРЕМ из текущего объекта и ПЕРЕДАЕМ как параметр

        # __init__ (конструктор):
            # сделай логгер с именем hui
            # name="hui" приходит в параметр
            # self.name = name — сохраняем hui внутрь
        # bind (копия):
            # у текущего логгера есть self.name = "hui"
            # берем self.name 
            # name=self.name — передаем в конструктор новому

        return Logger( # новый логгер
            name=self.name,
            level=self.level,
            handlers=self.handlers,
            extra=new_extra,
        )