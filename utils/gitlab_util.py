import gitlab


def get_active_projects(subgroup_id: int, gitlab_url: str, private_token: str):
    """
    Fetch all active (non-archived) project names in a subgroup and its nested subgroups.

    Args:
        gitlab_url (str): URL of the GitLab instance.
        private_token (str): Personal access token with appropriate permissions.
        subgroup_id (int): ID of the subgroup to fetch projects from.

    Returns:
        set: A set of active (non-archived) project names.
    """
    try:
        # Initialise GitLab connection
        gl = gitlab.Gitlab(gitlab_url, private_token=private_token)

        # Get the subgroup
        subgroup = gl.groups.get(subgroup_id)

        # Fetch all projects in the subgroup and nested subgroups
        active_projects = set()
        projects = subgroup.projects.list(all=True, include_subgroups=True, archived=False)

        for project in projects:
            if not project.archived:
                active_projects.add(project.name)

        return active_projects

    except gitlab.exceptions.GitlabAuthenticationError:
        raise Exception("Authentication failed. Check your GitLab URL and token.")
    except gitlab.exceptions.GitlabGetError as e:
        raise Exception(f"Error fetching subgroup or projects: {e}")
    except Exception as e:
        raise Exception(f"An unexpected error occurred: {e}")