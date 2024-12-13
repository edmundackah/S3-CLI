from enum import Enum
from pathlib import Path

import typer

from utils.file_picker import get_resource_path


class VersionIncrement(str, Enum):
    MAJOR = "MAJOR"
    MINOR = "MINOR"
    PATCH = "PATCH"


def get_app_version():
    """Reads the version number from the .version file in the resources folder."""
    version_file_path = Path(get_resource_path("resources/.version"))

    if not version_file_path.exists():
        typer.secho("Warning: .version file is missing in the resources folder.", fg=typer.colors.YELLOW)
        raise typer.Exit(code=1)

    with version_file_path.open("r") as file:
        version = file.read().strip()

    if not version:
        typer.secho("Error: No version number set in the .version file.", fg=typer.colors.RED)
        raise typer.Exit(code=1)

    typer.secho(f"{version}")


def bump_app_version(part: VersionIncrement):
    """
    Bumps the version number in the .version file.

    Args:
        part (VersionIncrement): The part of the version to bump (MAJOR, MINOR, or PATCH).
    """
    version_file_path = Path(get_resource_path("resources/.version"))

    if not version_file_path.exists():
        typer.secho("Error: .version file is missing in the resources folder.", fg=typer.colors.RED)
        raise typer.Exit(code=1)

    with version_file_path.open("r") as file:
        version = file.read().strip()

    if not version:
        typer.secho("Error: No version number set in the .version file.", fg=typer.colors.RED)
        raise typer.Exit(code=1)

    # Parse version
    try:
        major, minor, patch = map(int, version.split("."))
    except ValueError:
        typer.secho("Error: Invalid version format. Expected MAJOR.MINOR.PATCH.", fg=typer.colors.RED)
        raise typer.Exit(code=1)

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

    typer.secho(f"Version bumped to: {new_version}", fg=typer.colors.GREEN)