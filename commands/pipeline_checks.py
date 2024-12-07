import os

import typer

from utils.gitlab_util import get_gitlab_subgroups


def check_team_folder(path: str, gitlab_url: str, private_token: str, group_id: int):
    # Check if the path exists
    if not os.path.exists(path):
        typer.secho("The specified path does not exist.", fg=typer.colors.RED)
        raise typer.Exit(1)

    # Fetch subgroup names from GitLab
    typer.secho("Fetching subgroup names from GitLab...", fg=typer.colors.BLUE)
    subgroups = get_gitlab_subgroups(gitlab_url, private_token, group_id)
    typer.secho(f"Found subgroups: {', '.join(subgroups)}", fg=typer.colors.GREEN)

    # Validate folder names
    invalid_folders = []
    for folder in os.listdir(path):
        folder_path = os.path.join(path, folder)
        if os.path.isdir(folder_path) and folder not in subgroups:
            invalid_folders.append(folder)

    if invalid_folders:
        typer.secho(
            f"The following folder names are invalid: {', '.join(invalid_folders)}",
            fg=typer.colors.RED,
        )
        typer.secho(
            "Folder names must match valid GitLab subgroups or nested subgroups. "
            "Please rename the invalid folders to match the subgroup names in GitLab.",
            fg=typer.colors.YELLOW,
        )
        raise typer.Exit(1)

    typer.secho("All folder names are valid!", fg=typer.colors.GREEN)