"""Тесты для formatters.py — TextFormatter, JsonFormatter."""

from __future__ import annotations

import json
from datetime import datetime

import pytest

from prettylog import LogLevel, LogRecord
from prettylog.formatters import JsonFormatter, TextFormatter


@pytest.fixture
def sample_record() -> LogRecord:
    return LogRecord(
        name="myapp",
        level=LogLevel.INFO,
        message="Server started",
        module="server",
        timestamp=datetime(2024, 5, 23, 14, 32, 10),
    )


class TestTextFormatter:
    """Тесты для TextFormatter."""

    def test_basic_format(self, sample_record: LogRecord) -> None:
        formatter = TextFormatter()
        result = formatter.format(sample_record)
        assert result == "[2024-05-23 14:32:10] [INFO] [myapp] Server started"

    def test_timestamp_format(self, sample_record: LogRecord) -> None:
        formatter = TextFormatter()
        result = formatter.format(sample_record)
        assert "[2024-05-23 14:32:10]" in result

    def test_level_as_string(self, sample_record: LogRecord) -> None:
        formatter = TextFormatter()
        result = formatter.format(sample_record)
        assert "[INFO]" in result
        assert "[20]" not in result

    def test_all_levels(self) -> None:
        formatter = TextFormatter()
        for level in LogLevel:
            record = LogRecord(
                name="test",
                level=level,
                message="msg",
                module="",
                timestamp=datetime(2024, 5, 23, 14, 32, 10),
            )
            result = formatter.format(record)
            assert f"[{level.name}]" in result

    def test_extra_fields(self) -> None:
        formatter = TextFormatter()
        record = LogRecord(
            name="api",
            level=LogLevel.INFO,
            message="Request",
            module="",
            timestamp=datetime(2024, 5, 23, 14, 32, 10),
            extra={"user_id": "42", "ip": "127.0.0.1"},
        )
        result = formatter.format(record)
        assert "| user_id=42 ip=127.0.0.1" in result

    def test_extra_empty_dict_not_shown(self, sample_record: LogRecord) -> None:
        formatter = TextFormatter()
        result = formatter.format(sample_record)
        assert "|" not in result

    def test_extra_single_field(self) -> None:
        formatter = TextFormatter()
        record = LogRecord(
            name="api",
            level=LogLevel.INFO,
            message="Login",
            module="",
            timestamp=datetime(2024, 5, 23, 14, 32, 10),
            extra={"request_id": "abc-123"},
        )
        result = formatter.format(record)
        assert "| request_id=abc-123" in result

    def test_message_with_spaces(self) -> None:
        formatter = TextFormatter()
        record = LogRecord(
            name="app",
            level=LogLevel.INFO,
            message="User John Doe logged in",
            module="",
            timestamp=datetime(2024, 5, 23, 14, 32, 10),
        )
        result = formatter.format(record)
        assert result == "[2024-05-23 14:32:10] [INFO] [app] User John Doe logged in"


class TestJsonFormatter:
    """Тесты для JsonFormatter."""

    def test_valid_json(self, sample_record: LogRecord) -> None:
        formatter = JsonFormatter()
        result = formatter.format(sample_record)
        data = json.loads(result)
        assert isinstance(data, dict)

    def test_timestamp_iso(self, sample_record: LogRecord) -> None:
        formatter = JsonFormatter()
        result = formatter.format(sample_record)
        data = json.loads(result)
        assert data["timestamp"] == "2024-05-23T14:32:10"

    def test_level_as_string(self, sample_record: LogRecord) -> None:
        formatter = JsonFormatter()
        result = formatter.format(sample_record)
        data = json.loads(result)
        assert data["level"] == "INFO"

    def test_logger_name(self, sample_record: LogRecord) -> None:
        formatter = JsonFormatter()
        result = formatter.format(sample_record)
        data = json.loads(result)
        assert data["logger"] == "myapp"

    def test_message(self, sample_record: LogRecord) -> None:
        formatter = JsonFormatter()
        result = formatter.format(sample_record)
        data = json.loads(result)
        assert data["message"] == "Server started"

    def test_extra_empty(self, sample_record: LogRecord) -> None:
        formatter = JsonFormatter()
        result = formatter.format(sample_record)
        data = json.loads(result)
        assert data["extra"] == {}

    def test_extra_with_data(self) -> None:
        formatter = JsonFormatter()
        record = LogRecord(
            name="api",
            level=LogLevel.INFO,
            message="Request",
            module="",
            timestamp=datetime(2024, 5, 23, 14, 32, 10),
            extra={"user_id": 42, "ip": "127.0.0.1"},
        )
        result = formatter.format(record)
        data = json.loads(result)
        assert data["extra"]["user_id"] == 42
        assert data["extra"]["ip"] == "127.0.0.1"

    def test_unicode_in_message(self) -> None:
        formatter = JsonFormatter()
        record = LogRecord(
            name="app",
            level=LogLevel.INFO,
            message="Привет мир! 你好",
            module="",
            timestamp=datetime(2024, 5, 23, 14, 32, 10),
        )
        result = formatter.format(record)
        data = json.loads(result)
        assert data["message"] == "Привет мир! 你好"

    def test_all_levels_json(self) -> None:
        formatter = JsonFormatter()
        for level in LogLevel:
            record = LogRecord(
                name="test",
                level=level,
                message="msg",
                module="",
                timestamp=datetime(2024, 5, 23, 14, 32, 10),
            )
            result = formatter.format(record)
            data = json.loads(result)
            assert data["level"] == level.name

    def test_json_structure(self, sample_record: LogRecord) -> None:
        formatter = JsonFormatter()
        result = formatter.format(sample_record)
        data = json.loads(result)
        expected_keys = {"timestamp", "level", "logger", "message", "extra"}
        assert set(data.keys()) == expected_keys
