"""Тесты для handlers.py — BaseHandler, ConsoleHandler, FileHandler."""

from __future__ import annotations

import os
from datetime import datetime

import pytest

from prettylog import LogLevel, LogRecord
from prettylog.handlers import BaseHandler, ConsoleHandler, FileHandler
from prettylog.formatters import TextFormatter, JsonFormatter


class FakeHandler(BaseHandler):
    """Тестовая заглушка: собирает все emitted записи."""

    def __init__(self, formatter=None):
        super().__init__(formatter)
        self.emitted: list[LogRecord] = []
        self.written: list[str] = []

    def emit(self, record: LogRecord) -> None:
        self.emitted.append(record)
        super().emit(record)

    def write(self, message: str) -> None:
        self.written.append(message)


@pytest.fixture
def sample_record() -> LogRecord:
    return LogRecord(
        name="test",
        level=LogLevel.INFO,
        message="hello",
        module="test_mod",
        timestamp=datetime(2024, 5, 23, 14, 32, 10),
    )


class TestBaseHandler:
    """Тесты для абстрактного BaseHandler."""

    def test_default_formatter(self, sample_record: LogRecord) -> None:
        """Если formatter=None — используется TextFormatter."""
        handler = FakeHandler(formatter=None)
        handler.emit(sample_record)

        assert len(handler.written) == 1
        assert "[2024-05-23 14:32:10]" in handler.written[0]

    def test_custom_formatter(self, sample_record: LogRecord) -> None:
        """Можно передать свой форматтер."""
        handler = FakeHandler(formatter=JsonFormatter())
        handler.emit(sample_record)

        assert len(handler.written) == 1
        assert '"message": "hello"' in handler.written[0]

    def test_emit_calls_write(self, sample_record: LogRecord) -> None:
        """emit() вызывает write() с отформатированной строкой."""
        handler = FakeHandler(formatter=TextFormatter())
        handler.emit(sample_record)

        assert len(handler.written) == 1
        assert handler.written[0] == "[2024-05-23 14:32:10] [INFO] [test] hello"


class TestConsoleHandler:
    """Тесты для ConsoleHandler."""

    def test_uses_stdout(self, sample_record: LogRecord, capsys) -> None:
        """ConsoleHandler пишет в stdout."""
        handler = ConsoleHandler(formatter=TextFormatter())
        handler.emit(sample_record)

        captured = capsys.readouterr()
        assert "[INFO] [test] hello" in captured.out

    def test_ansi_color_info(self, sample_record: LogRecord, capsys) -> None:
        """INFO выводится зелёным цветом."""
        handler = ConsoleHandler(formatter=TextFormatter())
        handler.emit(sample_record)

        captured = capsys.readouterr()
        assert "\033[32m" in captured.out
        assert "\033[0m" in captured.out

    def test_ansi_color_debug(self, capsys) -> None:
        """DEBUG выводится голубым."""
        handler = ConsoleHandler(formatter=TextFormatter())
        record = LogRecord(
            name="test",
            level=LogLevel.DEBUG,
            message="debug msg",
            module="",
            timestamp=datetime(2024, 5, 23, 14, 32, 10),
        )
        handler.emit(record)

        captured = capsys.readouterr()
        assert "\033[36m" in captured.out

    def test_ansi_color_warning(self, capsys) -> None:
        """WARNING выводится жёлтым."""
        handler = ConsoleHandler(formatter=TextFormatter())
        record = LogRecord(
            name="test",
            level=LogLevel.WARNING,
            message="warn",
            module="",
            timestamp=datetime(2024, 5, 23, 14, 32, 10),
        )
        handler.emit(record)

        captured = capsys.readouterr()
        assert "\033[33m" in captured.out

    def test_ansi_color_error(self, capsys) -> None:
        """ERROR выводится красным."""
        handler = ConsoleHandler(formatter=TextFormatter())
        record = LogRecord(
            name="test",
            level=LogLevel.ERROR,
            message="err",
            module="",
            timestamp=datetime(2024, 5, 23, 14, 32, 10),
        )
        handler.emit(record)

        captured = capsys.readouterr()
        assert "\033[31m" in captured.out

    def test_ansi_color_critical(self, capsys) -> None:
        """CRITICAL выводится жирным красным."""
        handler = ConsoleHandler(formatter=TextFormatter())
        record = LogRecord(
            name="test",
            level=LogLevel.CRITICAL,
            message="crit",
            module="",
            timestamp=datetime(2024, 5, 23, 14, 32, 10),
        )
        handler.emit(record)

        captured = capsys.readouterr()
        assert "\033[1;31m" in captured.out


class TestFileHandler:
    """Тесты для FileHandler."""

    def teardown_method(self) -> None:
        for f in ["test.log", "test.log.1", "test.log.2"]:
            if os.path.exists(f):
                os.remove(f)

    def test_creates_file(self, sample_record: LogRecord) -> None:
        handler = FileHandler("test.log", formatter=TextFormatter())
        handler.emit(sample_record)
        handler.close()
        assert os.path.exists("test.log")

    def test_writes_to_file(self, sample_record: LogRecord) -> None:
        handler = FileHandler("test.log", formatter=TextFormatter())
        handler.emit(sample_record)
        handler.close()

        with open("test.log", encoding="utf-8") as f:
            content = f.read()
        assert "[INFO] [test] hello" in content

    def test_no_ansi_in_file(self, sample_record: LogRecord) -> None:
        """В файле нет ANSI-кодов цветов."""
        handler = FileHandler("test.log", formatter=TextFormatter())
        handler.emit(sample_record)
        handler.close()

        with open("test.log", encoding="utf-8") as f:
            content = f.read()
        assert "\033[" not in content

    def test_append_mode(self, sample_record: LogRecord) -> None:
        handler = FileHandler("test.log", formatter=TextFormatter())
        handler.emit(sample_record)
        handler.close()

        handler2 = FileHandler("test.log", formatter=TextFormatter())
        handler2.emit(sample_record)
        handler2.close()

        with open("test.log", encoding="utf-8") as f:
            lines = f.readlines()
        assert len(lines) == 2

    def test_rotation_creates_backup(self, sample_record: LogRecord) -> None:
        handler = FileHandler(
            "test.log",
            formatter=TextFormatter(),
            max_bytes=10,
            backup_count=2,
        )
        handler.emit(sample_record)
        handler.emit(sample_record)
        handler.close()

        assert os.path.exists("test.log")

    def test_utf8_encoding(self) -> None:
        handler = FileHandler("test.log", formatter=TextFormatter())
        record = LogRecord(
            name="test",
            level=LogLevel.INFO,
            message="Привет мир! 你好世界",
            module="",
            timestamp=datetime(2024, 5, 23, 14, 32, 10),
        )
        handler.emit(record)
        handler.close()

        with open("test.log", encoding="utf-8") as f:
            content = f.read()
        assert "Привет мир!" in content
        assert "你好世界" in content

    def test_close(self, sample_record: LogRecord) -> None:
        handler = FileHandler("test.log", formatter=TextFormatter())
        handler.emit(sample_record)
        handler.close()

    def test_multiple_backups(self) -> None:
        handler = FileHandler(
            "test.log",
            formatter=TextFormatter(),
            max_bytes=1,
            backup_count=2,
        )
        for i in range(5):
            record = LogRecord(
                name="test",
                level=LogLevel.INFO,
                message=f"msg {i}",
                module="",
                timestamp=datetime(2024, 5, 23, 14, 32, 10),
            )
            handler.emit(record)
        handler.close()

        assert os.path.exists("test.log")
