import logging

from django.core.management import BaseCommand

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

    def __init__(self, *args, **kwargs):
        logger_name = self.logger_name or self.get_default_logger_name()
        self.log = logging.getLogger(logger_name)

        super().__init__(*args, **kwargs)

    @classmethod
    def get_default_logger_name(cls):
        return f"django.command.{cls.__module__}"

    def execute(self, *args, **options):
        # Override BaseCommand.execute to handle logging/verbosity options
        log_level = VERBOSITY_LOGGING_LEVELS[options["verbosity"]]
        self.log.setLevel(log_level)

        super().execute(*args, **options)
