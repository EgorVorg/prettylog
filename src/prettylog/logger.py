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

    @classmethod
    def from_string(cls, name: str) -> LogLevel:
        """Преобразует строку в LogLevel (регистронезависимо).

        Args:
            name: Название уровня, например "info" или "ERROR".

        Raises:
            ValueError: Если передан неизвестный уровень.
        """
        ...


@dataclass
class LogRecord:
    """Одна запись лога — неизменяемая структура с данными."""

    name: str
    level: LogLevel
    message: str
    module: str
    timestamp: datetime
    extra: dict = field(default_factory=dict)


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
        ...

    def debug(self, msg: str) -> None:
        """Логирует сообщение уровнем DEBUG."""
        ...

    def info(self, msg: str) -> None:
        """Логирует сообщение уровнем INFO."""
        ...

    def warning(self, msg: str) -> None:
        """Логирует сообщение уровнем WARNING."""
        ...

    def error(self, msg: str) -> None:
        """Логирует сообщение уровнем ERROR."""
        ...

    def critical(self, msg: str) -> None:
        """Логирует сообщение уровнем CRITICAL."""
        ...

    def _log(self, level: LogLevel, msg: str) -> None:
        """Внутренний метод обработки сообщения.

        Порядок работы:
        1. Проверить, что level >= self.level (иначе молча выйти).
        2. Создать LogRecord с текущим timestamp.
        3. Смержить self.extra с полями записи.
        4. Отправить запись каждому хендлеру через handler.emit(record).
        """
        ...

    def bind(self, **kwargs: object) -> "Logger":
        """Создаёт новый Logger с замёрженными extra-полями.

        Исходный логгер не модифицируется — чистая функция.

        Example:
            user_logger = logger.bind(user_id=42)
            user_logger.info("login")  # в extra будет user_id=42
        """
        ...
