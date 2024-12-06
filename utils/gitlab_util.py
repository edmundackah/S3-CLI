import sys
import typer
import gitlab


def get_active_projects(subgroup_id: int, gitlab_url: str, private_token: str):
    """
    Fetch all active (non-archived) project names in a subgroup and its nested subgroups.

    Args:
        subgroup_id (int): ID of the subgroup to fetch projects from.
        gitlab_url (str): URL of the GitLab instance.
        private_token (str): Personal access token with appropriate permissions.

    Returns:
        set: A set of active (non-archived) project names.
    """
    try:
        # Initialise GitLab connection
        gl = gitlab.Gitlab(gitlab_url, private_token=private_token)
        subgroup = gl.groups.get(subgroup_id)

        active_projects = set()
        projects = subgroup.projects.list(all=True, include_subgroups=True, archived=False)

        for project in projects:
            active_projects.add(project.name)

        return active_projects
    except Exception as e:
        typer.secho(f"An error occurred: {e}", fg=typer.colors.RED)
        sys.exit(1)