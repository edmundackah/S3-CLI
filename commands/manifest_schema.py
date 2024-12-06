import json
import sys

import typer
import yaml
from jsonschema import Draft7Validator
from utils.helpers import is_valid_change_record
from utils.gitlab_util import get_active_projects


def validate_manifest(yaml_file: str, subgroup_id: int, gitlab_url: str, private_token: str):
    _validate_yaml(yaml_file, "resources/release-manifest-schema.json")

    # Fetch valid projects
    typer.secho("Fetching active projects from GitLab...", fg=typer.colors.BLUE)
    valid_projects = get_active_projects(subgroup_id, gitlab_url, private_token)

    # Validate GitLab project name
    with open(yaml_file, "r") as file:
        data = yaml.safe_load(file)

    project_name = data.get("projectName")

    if project_name in valid_projects:
        typer.secho(f"✅ '{project_name}' is a valid GitLab project ", fg=typer.colors.GREEN)
    else:
        typer.secho(f"❌ '{project_name}' does not exist in GitLab.", fg=typer.colors.RED)
        sys.exit(1)

    # Validate change record
    change_record = data.get("changeRecord")
    _validate_change_record(change_record)


def validate_maintenance_yaml(yaml_file: str, subgroup_id: int, gitlab_url: str, private_token: str):
    _validate_yaml(yaml_file, "resources/maintenance-flag-schema.json")

    # Fetch valid projects
    typer.secho("Fetching active projects from GitLab...", fg=typer.colors.BLUE)
    valid_projects = get_active_projects(subgroup_id, gitlab_url, private_token)

    typer.secho("Validating Flag dependencies...", fg=typer.colors.BLUE)

    # Validate Maintenance flag dependencies against active GitLab projects.
    with open(yaml_file, "r") as file:
        data = yaml.safe_load(file)

    for flag in data.get("flags", []):
        for dependency in flag.get("dependencies", []):
            if dependency not in valid_projects:
                typer.secho(f"❌ Flag dependency '{dependency}' does not exist in GitLab.", fg=typer.colors.RED)
                sys.exit(1)

    typer.secho("✅ All Flag dependencies are valid!", fg=typer.colors.GREEN)

    # Validate change record
    change_record = data.get("changeRecord")
    _validate_change_record(change_record)


def _validate_change_record(change_record: str):
    response = is_valid_change_record(change_record)

    if not response["isValid"]:
        typer.secho(f"❌ {response['message']}", fg=typer.colors.RED)
        sys.exit(1)
    else:
        typer.secho(f"✅ Change record {change_record} is valid!", fg=typer.colors.GREEN)


def _validate_yaml(yaml_file: str, schema: str):
    try:
        # Load the YAML file
        with open(yaml_file, 'r') as yf:
            yaml_data = yaml.safe_load(yf)

        # Load the JSON schema
        with open(schema, 'r') as sf:
            json_schema = json.load(sf)

        validator = Draft7Validator(json_schema)
        errors = list(validator.iter_errors(yaml_data))

        # Check for validation errors
        if errors:
            typer.echo("Validation failed! Errors found:", err=True)
            for error in errors:
                typer.echo(f"    - {'.'.join(map(str, error.absolute_path))}: {error.message}", err=True)
            raise typer.Exit(code=1)

        typer.echo("Validation successful! The YAML file is valid. 🥳")
    except FileNotFoundError as fnfe:
        typer.echo(f"File not found: {fnfe.filename}", err=True)
        raise typer.Exit(code=1)
    except yaml.YAMLError as ye:
        typer.echo(f"Failed to parse YAML: {ye}", err=True)
        raise typer.Exit(code=1)
    except json.JSONDecodeError as je:
        typer.echo(f"Failed to parse JSON schema: {je}", err=True)
        raise typer.Exit(code=1)