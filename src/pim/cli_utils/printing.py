import logging
import sys
import traceback
from pim.cli_utils.console import get_console, get_debug_mode

logger = logging.getLogger("pim")


def debug(message):
    logger.debug(message)


def info(message, style=None):
    logger.info(message)
    get_console().print(message, style=style)


def success(message):
    logger.info(message)
    get_console().print(f"[bold green]Success:[/] {message}")


def warning(message):
    logger.warning(message)
    get_console().print(f"[bold yellow]Warning:[/] {message}")


def handle_cli_error(error, exit_code=1, message=None):
    console = get_console()
    debug = get_debug_mode()

    # Use custom message if provided, otherwise use str(error)
    final_message = message or str(error)

    # Print user-friendly error
    console.print(f"[bold red]Error:[/] {final_message}")

    # Log the error
    logger.error(final_message)

    # Optional: show traceback if debug is on
    if debug:
        tb = "".join(
            traceback.format_exception(type(error), error, error.__traceback__)
        )
        console.print("[red]Traceback:[/]")
        console.print(tb)
        logger.debug(tb)

    sys.exit(exit_code)
