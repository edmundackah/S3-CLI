import gitlab

from utils.log_util import log, AnsiColor


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
        gl = gitlab.Gitlab(gitlab_url, private_token=private_token)
        subgroup = gl.groups.get(subgroup_id)

        active_projects = set()
        projects = subgroup.projects.list(all=True, include_subgroups=True, archived=False)

        for project in projects:
            active_projects.add(project.name)

        return active_projects
    except Exception as e:
        log(f"An error occurred: {e}", AnsiColor.RED, 1)


def get_gitlab_subgroups(gitlab_url: str, private_token: str, group_id: int) -> set:
    """Fetch all subgroup and nested subgroup names from GitLab."""
    gl = gitlab.Gitlab(gitlab_url, private_token=private_token)
    subgroups = set()
    groups_to_process = [gl.groups.get(group_id)]

    while groups_to_process:
        current_group = groups_to_process.pop()
        for subgroup in current_group.subgroups.list(all=True):
            subgroups.add(subgroup.name)
            groups_to_process.append(gl.groups.get(subgroup.id))

    return subgroups