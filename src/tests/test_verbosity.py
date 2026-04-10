import logging

import pytest
from django.core.management import call_command

from django_logging_management_command.command import LoggingBaseCommand


class LoggingTestCommand(LoggingBaseCommand):
    def handle(self, *args, **options):
        self.log.debug("Log message at DEBUG level")
        self.log.info("Log message at INFO level")
        self.log.warning("Log message at WARNING level")
        self.log.error("Log message at ERROR level")
        self.log.critical("Log message at CRITICAL level")
        try:
            raise RuntimeError("Log message from test exception")
        except RuntimeError as exc:
            self.log.exception(exc)


@pytest.fixture
def cmd():
    return LoggingTestCommand()


def test_default_verbosity(cmd, caplog):
    with caplog.at_level(logging.NOTSET):
        call_command(cmd)

    assert cmd.log.getEffectiveLevel() == logging.WARNING

    for record in caplog.records:
        assert record.levelno >= logging.WARNING

    assert "Log message at DEBUG level" not in caplog.text
    assert "Log message at INFO level" not in caplog.text
    assert "Log message at WARNING level" in caplog.text
    assert "Log message at ERROR level" in caplog.text
    assert "Log message at CRITICAL level" in caplog.text
    assert "Log message from test exception" in caplog.text


@pytest.mark.parametrize("verbosity, log_level, log_record_count", (
        (0, logging.ERROR, 3),
        (1, logging.WARNING, 4),
        (2, logging.INFO, 5),
        (3, logging.DEBUG, 6),
))
def test_set_specific_verbosity(cmd, caplog, verbosity, log_level, log_record_count):
    with caplog.at_level(logging.NOTSET):
        call_command(cmd, verbosity=verbosity)

    assert cmd.log.getEffectiveLevel() == log_level

    for record in caplog.records:
        assert record.levelno >= log_level

    assert len(caplog.records) == log_record_count, f"The test command should emit {log_record_count} messages at level {log_level}"
