"""Хендлеры: куда писать логи (консоль, файл, и т.д.)."""

from abc import ABC, abstractmethod
from typing import TextIO

from prettylog.formatters import BaseFormatter
from prettylog.logger import LogRecord


class BaseHandler(ABC):
    """Абстрактный базовый класс для всех хендлеров.

    Хендлер знает *куда* писать, но не знает *в каком формате*.
    Форматирование делегируется форматтеру через композицию.
    """

    def __init__(self, formatter: BaseFormatter | None = None) -> None:
        """
        Args:
            formatter: Форматтер для преобразования записи в строку.
                       Если None — используется TextFormatter() по умолчанию.
        """
        ...

    def emit(self, record: LogRecord) -> None:
        """Шаблонный метод: форматирует запись и пишет куда нужно.

        Порядок:
        1. formatted = self.formatter.format(record)
        2. self.write(formatted)
        """
        ...

    @abstractmethod
    def write(self, message: str) -> None:
        """Записать отформатированное сообщение в целевой поток.

        Должен быть переопределён в подклассах.
        """


class ConsoleHandler(BaseHandler):
    """Пишет логи в stdout с ANSI-цветами по уровню."""

    # ANSI-коды цветов по уровням
    _COLORS: dict[int, str] = {
        10: "\033[36m",  # DEBUG — cyan
        20: "\033[32m",  # INFO — green
        30: "\033[33m",  # WARNING — yellow
        40: "\033[31m",  # ERROR — red
        50: "\033[1;31m",  # CRITICAL — bold red
    }
    _RESET = "\033[0m"

    def __init__(self, formatter: BaseFormatter | None = None) -> None:
        """
        Args:
            formatter: Форматтер. По умолчанию TextFormatter().

        Если установлен colorama — вызываем init() для кроссплатформенности.
        """
        ...

    def emit(self, record: LogRecord) -> None:
        """Форматирует, оборачивает в цвет уровня и пишет в stdout."""
        ...

    def write(self, message: str) -> None:
        """Пишет строку в stdout с переносом и сбросом буфера."""
        ...


class FileHandler(BaseHandler):
    """Пишет логи в файл с ротацией по размеру.

    Ротация: когда файл достигает max_bytes, он переименовывается
    в filename.1, предыдущий .1 → .2, и т.д. до backup_count.
    """

    def __init__(
        self,
        filename: str,
        formatter: BaseFormatter | None = None,
        max_bytes: int = 1_048_576,
        backup_count: int = 2,
    ) -> None:
        """
        Args:
            filename: Путь к файлу логов.
            formatter: Форматтер. По умолчанию TextFormatter().
            max_bytes: Максимальный размер файла в байтах перед ротацией.
            backup_count: Сколько резервных копий хранить.
        """
        ...

    def _open(self) -> TextIO:
        """Открывает файл в режиме append с кодировкой utf-8."""
        ...

    def _should_rotate(self) -> bool:
        """Проверить, нужна ли ротация (файл >= max_bytes)."""
        ...

    def _rotate(self) -> None:
        """Выполнить ротацию файлов:

        1. Удалить самый старый backup (filename.{backup_count}).
        2. Сдвинуть существующие backup'ы: .N → .{N+1}.
        3. Переименовать текущий файл → .1.
        4. Открыть новый пустой файл.
        """
        ...

    def write(self, message: str) -> None:
        """Проверяет необходимость ротации и пишет в файл (без цветов)."""
        ...

    def close(self) -> None:
        """Закрывает файловый дескриптор."""
        ...

    def __del__(self) -> None:
        """Подстраховка: закрыть файл при уничтожении хендлера."""
        ...
