import logging

from django.core.management import BaseCommand

VERBOSITY_LOGGING_LEVELS = {
    0: logging.ERROR,
    1: logging.WARNING,
    2: logging.INFO,
    3: logging.DEBUG,
}

class LoggingBaseCommand(BaseCommand):
    """A replacement for BaseCommand, supporting logging and verbosity handling out of the box."""

    def __init__(self, *args, **kwargs):
        self.log = logging.getLogger(__name__)

        super().__init__(*args, **kwargs)


    def execute(self, *args, **options):
        # Override BaseCommand.execute to handle logging/verbosity options
        log_level = VERBOSITY_LOGGING_LEVELS[options["verbosity"]]
        self.log.setLevel(log_level)

        super().execute(*args, **options)
