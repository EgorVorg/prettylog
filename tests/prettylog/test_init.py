"""Тесты для __init__.py — get_logger и экспорты."""

from __future__ import annotations

from prettylog import (
    ConsoleHandler,
    FileHandler,
    JsonFormatter,
    LogLevel,
    LogRecord,
    Logger,
    TextFormatter,
    get_logger,
    load_from_dict,
)


class TestExports:
    """Тесты что все публичные символы экспортированы."""

    def test_get_logger_exported(self) -> None:
        assert callable(get_logger)

    def test_logger_class_exported(self) -> None:
        assert Logger is not None

    def test_loglevel_exported(self) -> None:
        assert LogLevel is not None

    def test_logrecord_exported(self) -> None:
        assert LogRecord is not None

    def test_console_handler_exported(self) -> None:
        assert ConsoleHandler is not None

    def test_file_handler_exported(self) -> None:
        assert FileHandler is not None

    def test_text_formatter_exported(self) -> None:
        assert TextFormatter is not None

    def test_json_formatter_exported(self) -> None:
        assert JsonFormatter is not None

    def test_load_from_dict_exported(self) -> None:
        assert callable(load_from_dict)


class TestGetLogger:
    """Тесты для get_logger()."""

    def test_default_logger(self, capsys) -> None:
        logger = get_logger()
        assert logger.name == "root"
        assert logger.level == LogLevel.INFO

    def test_custom_name(self) -> None:
        logger = get_logger(name="myapp")
        assert logger.name == "myapp"

    def test_custom_level_string(self) -> None:
        logger = get_logger(level="DEBUG")
        assert logger.level == LogLevel.DEBUG

    def test_custom_level_lowercase(self) -> None:
        logger = get_logger(level="debug")
        assert logger.level == LogLevel.DEBUG

    def test_default_handlers(self, capsys) -> None:
        logger = get_logger(level="INFO")
        logger.info("hello default")

        captured = capsys.readouterr()
        assert "hello default" in captured.out
        assert "\033[32m" in captured.out

    def test_no_handlers_raises(self) -> None:
        logger = get_logger(name="empty", handlers=[])
        logger.info("no handlers")

    def test_custom_handlers(self) -> None:
        from tests.prettylog.test_handlers import FakeHandler

        handler = FakeHandler()
        logger = get_logger(name="custom", handlers=[handler])
        logger.info("custom handler")

        assert len(handler.emitted) == 1
