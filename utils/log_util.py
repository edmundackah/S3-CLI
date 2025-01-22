from enum import Enum
import sys

class AnsiColor(Enum):
    RESET = '\033[0m'
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    BRIGHT_BLACK = '\033[90m'
    BRIGHT_RED = '\033[91m'
    BRIGHT_GREEN = '\033[92m'
    BRIGHT_YELLOW = '\033[93m'
    BRIGHT_BLUE = '\033[94m'
    BRIGHT_MAGENTA = '\033[95m'
    BRIGHT_CYAN = '\033[96m'
    BRIGHT_WHITE = '\033[97m'


def log(message: str, color: AnsiColor, exit_code: int = 0):
    """
    Prints a message in the specified color and exits with the given exit code.

    Args:
        message (str): The message to print.
        color (AnsiColor): The ANSI color to use for the message.
        exit_code (int, optional): The exit code to use when exiting. Defaults to 0.
    """
    print(f"{color.value}{message}{AnsiColor.RESET.value}")
    if exit_code != 0:
        sys.exit(exit_code)