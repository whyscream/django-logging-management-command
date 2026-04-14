import logging

import pytest
from django.core.management import call_command, BaseCommand

from django_logging_management_command.command import VerbosityCommandMixin


class VerbosityTestCommand(VerbosityCommandMixin, BaseCommand):
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
    return VerbosityTestCommand()


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


def test_default_logger_name(cmd, caplog):
    # the logger is named after the module ('file name') defining the command class.
    assert cmd.log.name == "django.command.test_verbosity"

    call_command(cmd)
    for record in caplog.records:
        assert record.name == "django.command.test_verbosity"


def test_custom_logger_name(caplog):
    class CustomLoggerNameCommand(VerbosityTestCommand):
        logger_name = "django.command.my_custom_logger_name"

    cmd = CustomLoggerNameCommand()
    assert cmd.log.name == "django.command.my_custom_logger_name"

    call_command(cmd)
    for record in caplog.records:
        assert record.name == "django.command.my_custom_logger_name"
