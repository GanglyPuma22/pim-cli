import logging
from pathlib import Path


class RelativePathFilter(logging.Filter):
    """
    A logging filter to add a 'relpath' attribute to log records.
    The path is relative to the project's 'src' directory, so that log
    paths start with 'pim/...' instead of a full absolute path.
    """

    def __init__(self, name=""):
        super().__init__(name)
        self.pim_root = None
        try:
            # This logic assumes this file is located at 'src/pim/util/logging_filter.py'.
            # It finds the 'src' directory to create relative paths from there.
            pim_root_path = Path(__file__).resolve().parents[1]
            if pim_root_path.name == "pim":
                self.pim_root = pim_root_path
        except IndexError:
            # If the file structure is different, this will fail gracefully.
            # We'll fall back to using the full pathname in that case.
            pass

    def filter(self, record):
        """Adds the 'relpath' attribute to the log record."""
        pathname = record.pathname
        if self.pim_root:
            full_path = Path(pathname).resolve()
            if full_path.is_relative_to(self.pim_root):
                pathname = str(full_path.relative_to(self.pim_root))
        record.relpath = pathname
        return True
