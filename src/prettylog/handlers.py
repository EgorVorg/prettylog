"""Хендлеры: куда писать логи (консоль, файл, и т.д.)."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TextIO
import os
import sys

from prettylog.formatters import BaseFormatter, TextFormatter


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
        if formatter is None:
            self.formatter = TextFormatter()
        else:
            self.formatter = formatter

    def emit(self, record: LogRecord) -> None:
        """Шаблонный метод: форматирует запись и пишет куда нужно.

        Порядок:
        1. formatted = self.formatter.format(record)
        2. self.write(formatted)
        """
        formatted = self.formatter.format(record)
        self.write(formatted)

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
        try:
            import colorama

            colorama.init()
        except ImportError:
            pass

        super().__init__(formatter)

    def emit(self, record: LogRecord) -> None:
        """Форматирует, оборачивает в цвет уровня и пишет в stdout."""
        color = self._COLORS.get(record.level.value, "")
        formatted = self.formatter.format(record)
        colored_message = f"{color}{formatted}{self._RESET}"
        self.write(colored_message)

    def write(self, message: str) -> None:
        """Пишет строку в stdout с переносом и сбросом буфера."""
        print(message, flush=True)


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
        self.filename = filename
        self.max_bytes = max_bytes
        self.backup_count = backup_count
        self._file = self._open()

        super().__init__(formatter)

    def _open(self) -> TextIO:
        """Открывает файл в режиме append с кодировкой utf-8."""
        return open(self.filename, "a", encoding="utf-8")

    def _should_rotate(self) -> bool:
        """Проверить, нужна ли ротация (файл >= max_bytes)."""
        if not os.path.exists(self.filename):
            return False
        return os.path.getsize(self.filename) >= self.max_bytes

    def _rotate(self) -> None:
        """Выполнить ротацию файлов:

        1. Удалить самый старый backup (filename.{backup_count}).
        2. Сдвинуть существующие backup'ы: .N → .{N+1}.
        3. Переименовать текущий файл → .1.
        4. Открыть новый пустой файл.
        """

        if self._file:
            self._file.close()

        oldest_backup = f"{self.filename}.{self.backup_count}"  # удаляем старый бекап
        if os.path.exists(oldest_backup):
            os.remove(oldest_backup)

        # туду сдвинуть существующие бекапы
        for i in range(self.backup_count - 1, 0, -1):
            old_backup_name = f"{self.filename}.{i}"
            new_backup_name = f"{self.filename}.{i + 1}"
            if os.path.exists(old_backup_name):
                os.rename(old_backup_name, new_backup_name)

        if os.path.exists(self.filename):
            os.rename(self.filename, f"{self.filename}.1")

        self._file = self._open()

    def write(self, message: str) -> None:
        """Проверяет необходимость ротации и пишет в файл (без цветов)."""
        if self._should_rotate():
            self._rotate()

        f = self._file
        f.write(message + "\n")
        f.flush()

    def close(self) -> None:
        """Закрывает файловый дескриптор."""
        if self._file and not self._file.closed:
            self._file.close()
            self._file = None

    def __del__(self) -> None:
        """Подстраховка: закрыть файл при уничтожении хендлера."""
        try:
            self.close()
        except Exception:
            pass
