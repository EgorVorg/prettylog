"""Тесты для logger.py — LogLevel, LogRecord, Logger."""

from __future__ import annotations

from datetime import datetime

import pytest

from prettylog import LogLevel, LogRecord
from prettylog.logger import Logger


class FakeHandler:
    """Тестовая заглушка-хендлер: собирает все emitted записи."""

    def __init__(self):
        self.emitted: list[LogRecord] = []
        self.written: list[str] = []

    def emit(self, record: LogRecord) -> None:
        self.emitted.append(record)

    def write(self, message: str) -> None:
        self.written.append(message)


class TestLogLevel:
    """Тесты для LogLevel IntEnum."""

    def test_values(self) -> None:
        assert LogLevel.DEBUG == 10
        assert LogLevel.INFO == 20
        assert LogLevel.WARNING == 30
        assert LogLevel.ERROR == 40
        assert LogLevel.CRITICAL == 50

    def test_comparison(self) -> None:
        assert LogLevel.DEBUG < LogLevel.INFO
        assert LogLevel.INFO < LogLevel.WARNING
        assert LogLevel.WARNING < LogLevel.ERROR
        assert LogLevel.ERROR < LogLevel.CRITICAL

    def test_from_string_lowercase(self) -> None:
        assert LogLevel.from_string("debug") == LogLevel.DEBUG
        assert LogLevel.from_string("info") == LogLevel.INFO
        assert LogLevel.from_string("warning") == LogLevel.WARNING
        assert LogLevel.from_string("error") == LogLevel.ERROR
        assert LogLevel.from_string("critical") == LogLevel.CRITICAL

    def test_from_string_uppercase(self) -> None:
        assert LogLevel.from_string("DEBUG") == LogLevel.DEBUG
        assert LogLevel.from_string("INFO") == LogLevel.INFO

    def test_from_string_mixed_case(self) -> None:
        assert LogLevel.from_string("Debug") == LogLevel.DEBUG
        assert LogLevel.from_string("InFo") == LogLevel.INFO

    def test_from_string_invalid(self) -> None:
        with pytest.raises(ValueError, match="UNKNOWN"):
            LogLevel.from_string("UNKNOWN")

        with pytest.raises(ValueError):
            LogLevel.from_string("")

    def test_ordering(self) -> None:
        assert LogLevel.INFO > LogLevel.DEBUG
        assert LogLevel.CRITICAL >= LogLevel.ERROR
        assert LogLevel.DEBUG <= LogLevel.INFO


class TestLogRecord:
    """Тесты для LogRecord dataclass."""

    def test_creation(self) -> None:
        record = LogRecord(
            name="test",
            level=LogLevel.INFO,
            message="hello",
            module="test_module",
            timestamp=datetime(2024, 5, 23, 14, 32, 10),
        )
        assert record.name == "test"
        assert record.level == LogLevel.INFO
        assert record.message == "hello"
        assert record.module == "test_module"
        assert record.timestamp.year == 2024

    def test_default_extra(self) -> None:
        record = LogRecord(
            name="test",
            level=LogLevel.INFO,
            message="hello",
            module="",
            timestamp=datetime.now(),
        )
        assert record.extra == {}

    def test_custom_extra(self) -> None:
        record = LogRecord(
            name="test",
            level=LogLevel.INFO,
            message="hello",
            module="",
            timestamp=datetime.now(),
            extra={"key": "value"},
        )
        assert record.extra == {"key": "value"}


class TestLogger:
    """Тесты для Logger."""

    def test_init(self) -> None:
        handler = FakeHandler()
        logger = Logger(name="mylogger", level=LogLevel.INFO, handlers=[handler])

        assert logger.name == "mylogger"
        assert logger.level == LogLevel.INFO
        assert len(logger.handlers) == 1

    def test_debug_logs(self) -> None:
        handler = FakeHandler()
        logger = Logger(name="test", level=LogLevel.DEBUG, handlers=[handler])
        logger.debug("debug msg")

        assert len(handler.emitted) == 1
        assert handler.emitted[0].message == "debug msg"
        assert handler.emitted[0].level == LogLevel.DEBUG

    def test_info_logs(self) -> None:
        handler = FakeHandler()
        logger = Logger(name="test", level=LogLevel.DEBUG, handlers=[handler])
        logger.info("info msg")

        assert len(handler.emitted) == 1
        assert handler.emitted[0].message == "info msg"
        assert handler.emitted[0].level == LogLevel.INFO

    def test_warning_logs(self) -> None:
        handler = FakeHandler()
        logger = Logger(name="test", level=LogLevel.DEBUG, handlers=[handler])
        logger.warning("warn msg")

        assert len(handler.emitted) == 1
        assert handler.emitted[0].level == LogLevel.WARNING

    def test_error_logs(self) -> None:
        handler = FakeHandler()
        logger = Logger(name="test", level=LogLevel.DEBUG, handlers=[handler])
        logger.error("err msg")

        assert handler.emitted[0].level == LogLevel.ERROR

    def test_critical_logs(self) -> None:
        handler = FakeHandler()
        logger = Logger(name="test", level=LogLevel.DEBUG, handlers=[handler])
        logger.critical("crit msg")

        assert handler.emitted[0].level == LogLevel.CRITICAL

    def test_level_filtering(self) -> None:
        """DEBUG не проходит при уровне INFO."""
        handler = FakeHandler()
        logger = Logger(name="test", level=LogLevel.INFO, handlers=[handler])

        logger.debug("filtered")
        assert len(handler.emitted) == 0

        logger.info("passed")
        assert len(handler.emitted) == 1

    def test_multiple_handlers(self) -> None:
        """Запись отправляется всем хендлерам."""
        h1 = FakeHandler()
        h2 = FakeHandler()
        logger = Logger(name="test", level=LogLevel.DEBUG, handlers=[h1, h2])

        logger.info("broadcast")

        assert len(h1.emitted) == 1
        assert len(h2.emitted) == 1
        assert h1.emitted[0].message == "broadcast"
        assert h2.emitted[0].message == "broadcast"

    def test_log_record_timestamp(self) -> None:
        """В LogRecord проставляется timestamp."""
        handler = FakeHandler()
        logger = Logger(name="test", level=LogLevel.DEBUG, handlers=[handler])

        before = datetime.now()
        logger.info("check timestamp")
        after = datetime.now()

        record = handler.emitted[0]
        assert before <= record.timestamp <= after

    def test_logger_name_in_record(self) -> None:
        """В LogRecord попадает имя логгера."""
        handler = FakeHandler()
        logger = Logger(name="myapp", level=LogLevel.DEBUG, handlers=[handler])
        logger.info("test")

        assert handler.emitted[0].name == "myapp"

    def test_extra_from_logger(self) -> None:
        """Extra из логгера мержится в запись."""
        handler = FakeHandler()
        logger = Logger(
            name="test",
            level=LogLevel.DEBUG,
            handlers=[handler],
            extra={"app": "web"},
        )
        logger.info("msg")

        assert handler.emitted[0].extra.get("app") == "web"

    def test_bind_returns_new_logger(self) -> None:
        """bind() возвращает новый логгер, исходный не меняется."""
        handler = FakeHandler()
        logger = Logger(name="test", level=LogLevel.DEBUG, handlers=[handler])
        bound = logger.bind(user_id=42)

        assert bound is not logger
        assert logger.extra == {}

    def test_bind_preserves_level(self) -> None:
        """bind() сохраняет уровень исходного логгера."""
        handler = FakeHandler()
        logger = Logger(name="test", level=LogLevel.INFO, handlers=[handler])
        bound = logger.bind(user_id=42)

        assert bound.level == LogLevel.INFO

    def test_bind_preserves_handlers(self) -> None:
        """bind() сохраняет хендлеры исходного логгера."""
        handler = FakeHandler()
        logger = Logger(name="test", level=LogLevel.DEBUG, handlers=[handler])
        bound = logger.bind(user_id=42)

        assert len(bound.handlers) == 1

    def test_bind_extra_merged(self) -> None:
        """bind() мержит extra: исходное + новое."""
        handler = FakeHandler()
        logger = Logger(
            name="test",
            level=LogLevel.DEBUG,
            handlers=[handler],
            extra={"app": "web"},
        )
        bound = logger.bind(user_id=42)

        assert bound.extra == {"app": "web", "user_id": 42}

    def test_bind_chain(self) -> None:
        """bind() можно чейнить."""
        handler = FakeHandler()
        logger = Logger(name="test", level=LogLevel.DEBUG, handlers=[handler])
        l2 = logger.bind(a=1)
        l3 = l2.bind(b=2)

        assert l3.extra == {"a": 1, "b": 2}
        assert l2.extra == {"a": 1}

    def test_extra_override(self) -> None:
        """Новый extra перезаписывает старое при конфликте ключей."""
        handler = FakeHandler()
        logger = Logger(
            name="test",
            level=LogLevel.DEBUG,
            handlers=[handler],
            extra={"key": "old"},
        )
        bound = logger.bind(key="new")

        assert bound.extra["key"] == "new"
