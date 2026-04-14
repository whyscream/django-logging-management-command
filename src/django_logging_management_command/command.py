import logging
from typing import Any

VERBOSITY_LOGGING_LEVELS = {
    0: logging.ERROR,
    1: logging.WARNING,
    2: logging.INFO,
    3: logging.DEBUG,
}

class VerbosityCommandMixin:
    """A mixin for BaseCommand, supporting logging and verbosity handling out of the box."""
    logger_name: str = None
    """The name of the logger. Override to give this logger a custom name"""

    verbosity_loggers: list[str] = []

    def __init__(self, *args, **kwargs):
        logger_name = self.logger_name or self.get_default_logger_name()
        self.log = logging.getLogger(logger_name)
        self.verbosity_loggers.append(logger_name)

        super().__init__(*args, **kwargs)

    @classmethod
    def get_default_logger_name(cls):
        return f"django.command.{cls.__module__}"

    def execute(self, *args, **options) -> Any:
        # Override BaseCommand.execute to handle logging/verbosity options
        log_level = VERBOSITY_LOGGING_LEVELS[options["verbosity"]]

        original_log_levels = {}
        for logger_name in self.verbosity_loggers:
            # Capture original log level
            logger = logging.getLogger(logger_name)
            original_log_levels[logger_name] = logger.getEffectiveLevel()
            # Set the new level from verbosity
            logger.setLevel(log_level)

        output = super().execute(*args, **options)

        for logger_name, log_level in original_log_levels.items():
            # Restore the original log levels
            logging.getLogger(logger_name).setLevel(log_level)

        return output
