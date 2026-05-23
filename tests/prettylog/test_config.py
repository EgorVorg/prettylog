"""Тесты для config.py — load_from_dict."""

from __future__ import annotations

import os

import pytest

from prettylog import load_from_dict
from prettylog.handlers import ConsoleHandler, FileHandler
from prettylog.logger import LogLevel


class TestLoadFromDict:
    """Тесты для load_from_dict."""

    def test_basic_config(self, capsys) -> None:
        config = {
            "name": "test_app",
            "level": "INFO",
            "handlers": [{"type": "console", "formatter": "text"}],
        }
        logger = load_from_dict(config)
        assert logger.name == "test_app"
        assert logger.level == LogLevel.INFO
        assert len(logger.handlers) == 1
        assert isinstance(logger.handlers[0], ConsoleHandler)

    def test_default_name(self) -> None:
        config = {"level": "DEBUG", "handlers": [{"type": "console"}]}
        logger = load_from_dict(config)
        assert logger.name == "root"

    def test_default_level(self) -> None:
        config = {"handlers": [{"type": "console"}]}
        logger = load_from_dict(config)
        assert logger.level == LogLevel.INFO

    def test_default_formatter(self, capsys) -> None:
        config = {"handlers": [{"type": "console"}]}
        logger = load_from_dict(config)
        logger.info("test")

    def test_json_formatter(self, capsys) -> None:
        config = {"handlers": [{"type": "console", "formatter": "json"}]}
        logger = load_from_dict(config)
        logger.info("json test")

        captured = capsys.readouterr()
        assert '"message": "json test"' in captured.out

    def test_file_handler(self) -> None:
        log_file = "_test_config.log"
        if os.path.exists(log_file):
            os.remove(log_file)

        config = {
            "name": "file_test",
            "level": "DEBUG",
            "handlers": [
                {
                    "type": "file",
                    "filename": log_file,
                    "formatter": "text",
                    "max_bytes": 1024,
                }
            ],
        }
        logger = load_from_dict(config)
        assert len(logger.handlers) == 1
        assert isinstance(logger.handlers[0], FileHandler)
        logger.info("from config")
        assert os.path.exists(log_file)
        os.remove(log_file)

    def test_multiple_handlers(self) -> None:
        log_file = "_test_multi.log"
        for f in [log_file, f"{log_file}.1"]:
            if os.path.exists(f):
                os.remove(f)

        config = {
            "name": "multi",
            "level": "INFO",
            "handlers": [
                {"type": "console", "formatter": "text"},
                {"type": "file", "filename": log_file, "formatter": "json"},
            ],
        }
        logger = load_from_dict(config)
        assert len(logger.handlers) == 2
        assert isinstance(logger.handlers[0], ConsoleHandler)
        assert isinstance(logger.handlers[1], FileHandler)
        logger.info("multi handler test")
        assert os.path.exists(log_file)

        for f in [log_file, f"{log_file}.1"]:
            if os.path.exists(f):
                os.remove(f)

    def test_all_levels(self) -> None:
        for level_name in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]:
            config = {"level": level_name, "handlers": [{"type": "console"}]}
            logger = load_from_dict(config)
            assert logger.level == LogLevel[level_name]

    def test_unknown_handler_type(self) -> None:
        config = {"handlers": [{"type": "unknown"}]}
        with pytest.raises(ValueError, match="handler"):
            load_from_dict(config)

    def test_unknown_formatter_type(self) -> None:
        config = {"handlers": [{"type": "console", "formatter": "xml"}]}
        with pytest.raises(ValueError, match="formatter"):
            load_from_dict(config)

    def test_file_handler_with_defaults(self) -> None:
        log_file = "_test_defaults.log"
        if os.path.exists(log_file):
            os.remove(log_file)

        config = {"handlers": [{"type": "file", "filename": log_file}]}
        logger = load_from_dict(config)
        assert isinstance(logger.handlers[0], FileHandler)
        logger.info("default params")
        assert os.path.exists(log_file)
        os.remove(log_file)

    def test_logger_is_usable(self, capsys) -> None:
        config = {
            "name": "usable",
            "level": "DEBUG",
            "handlers": [{"type": "console", "formatter": "text"}],
        }
        logger = load_from_dict(config)
        logger.debug("debug msg")
        logger.info("info msg")
        logger.warning("warn msg")
        logger.error("err msg")
        logger.critical("crit msg")

        captured = capsys.readouterr()
        assert "debug msg" in captured.out
        assert "info msg" in captured.out
        assert "warn msg" in captured.out
        assert "err msg" in captured.out
        assert "crit msg" in captured.out
