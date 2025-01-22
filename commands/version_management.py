from enum import Enum
from pathlib import Path

import typer

from utils.file_picker import get_resource_path
from utils.log_util import AnsiColor, log


class VersionIncrement(str, Enum):
    MAJOR = "MAJOR"
    MINOR = "MINOR"
    PATCH = "PATCH"


def get_app_version():
    """Reads the version number from the .version file in the resources folder."""
    version_file_path = Path(get_resource_path("resources/.version"))

    if not version_file_path.exists():
        log(".version file is missing in the resources folder.", AnsiColor.RED, 1)

    with version_file_path.open("r") as file:
        version = file.read().strip()

    if not version:
        log("No version number set in the .version file.", AnsiColor.RED, 1)

    typer.secho(f"{version}")


def bump_app_version(part: VersionIncrement):
    """
    Bumps the version number in the .version file.

    Args:
        part (VersionIncrement): The part of the version to bump (MAJOR, MINOR, or PATCH).
    """
    version_file_path = Path(get_resource_path("resources/.version"))

    if not version_file_path.exists():
        log(".version file is missing in the resources folder.", AnsiColor.RED, 1)

    with version_file_path.open("r") as file:
        version = file.read().strip()

    if not version:
        log("No version number set in the .version file.", AnsiColor.RED, 1)

    # Parse version
    try:
        major, minor, patch = map(int, version.split("."))
    except ValueError:
        log("Invalid version format. Expected MAJOR.MINOR.PATCH.", AnsiColor.RED, 1)

    # Bump the specified part
    if part == VersionIncrement.MAJOR:
        major += 1
        minor = 0
        patch = 0
    elif part == VersionIncrement.MINOR:
        minor += 1
        patch = 0
    elif part == VersionIncrement.PATCH:
        patch += 1

    # Update the version
    new_version = f"{major}.{minor}.{patch}"
    with version_file_path.open("w") as file:
        file.write(new_version)

    log(f"Version bumped to: {new_version}", AnsiColor.GREEN)