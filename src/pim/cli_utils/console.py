from rich.console import Console
import logging

logger = logging.getLogger("pim")

_console = None
_debug_mode = None


# Shared console instance for the application
# This allows for consistent styling and configuration across different modules
# It can be initialized with no_color=True to disable color output if needed
def init_console(no_color=False, debug=False):
    global _console, _debug_mode
    _console = Console(no_color=no_color)
    _debug_mode = debug


def get_console():
    if _console is None:
        logging.error("Console not initialized. Call init_console() first.")
        raise RuntimeError("Console not initialized. Call init_console() first.")
    return _console


def get_debug_mode():
    if _debug_mode is None:
        logging.error("Debug mode not initialized. Call init_console() first.")
        raise RuntimeError("Debug mode not initialized. Call init_console() first.")
    return _debug_mode
