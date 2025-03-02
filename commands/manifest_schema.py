import json
import logging
from typing import List

import requests
import typer
import yaml
from jsonschema import Draft7Validator

from utils.file_picker import get_resource_path
from utils.gitlab_util import get_active_projects
from utils.helpers import is_valid_change_record, TargetServer, build_artifact_url
from utils.log_util import log, AnsiColor

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

def validate_manifest(yaml_file: str, subgroup_id: int, gitlab_url: str, private_token: str):
    _validate_yaml(yaml_file, "resources/release-manifest-schema.json")

    log("Fetching active projects from GitLab...", AnsiColor.BLUE)

    valid_projects = get_active_projects(subgroup_id, gitlab_url, private_token)

    # Validate GitLab project name
    with open(yaml_file, "r") as file:
        data = yaml.safe_load(file)

    project_name = data.get("projectName")

    if project_name in valid_projects:
        log(f"✅ '{project_name}' is a valid GitLab project ", AnsiColor.GREEN)
    else:
        log(f"❌ '{project_name}' does not exist in GitLab.", AnsiColor.RED, 1)

    artifact_exists(data.get("projectName"), data.get("version"), data.get("targetServer"))

    # Validate change record
    _validate_change_record(data.get("changeRecord"))


def validate_maintenance_yaml(yaml_file: str, subgroup_id: int, gitlab_url: str, private_token: str):
    _validate_yaml(yaml_file, "resources/maintenance-flag-schema.json")

    # Fetch valid projects
    log("Fetching active projects from GitLab...", AnsiColor.BLUE)
    valid_projects = get_active_projects(subgroup_id, gitlab_url, private_token)

    log("Validating Flag dependencies...", AnsiColor.BLUE)

    # Validate Maintenance flag dependencies against active GitLab projects.
    with open(yaml_file, "r") as file:
        data = yaml.safe_load(file)

    for flag in data.get("flags", []):
        for dependency in flag.get("dependencies", []):
            if dependency not in valid_projects:
                log(f"❌ Flag dependency '{dependency}' does not exist in GitLab.", AnsiColor.RED, 1)

    log("✅ All Flag dependencies are valid!", AnsiColor.GREEN)

    # Validate change record
    _validate_change_record(data.get("changeRecord"))


def artifact_exists(application: str, version: str, servers: List[TargetServer]):
    """Check if an artifact exists at a given Artifactory URL without downloading it."""

    # Check artifact exists in artifactory
    for server in servers:
        try:
            if server == TargetServer.AWS_S3:
                version = f"{version}-aws"

            url: str = build_artifact_url(application, version)

            response = requests.head(url)
            logging.info(f"Checking artifact: [HEAD] {url} , status code: {response.status_code}")

            if response.status_code == 200:
                log(f"✅ '{application}'  version '{version}' found in artifactory", AnsiColor.GREEN)
            else:
                log(f"❌ '{application}'  version '{version}' not found", AnsiColor.RED, 1)
        except requests.exceptions.RequestException as e:
            log(f"Error checking artifact existence: {e}", AnsiColor.RED, 1)


def _validate_change_record(change_record: str):
    response = is_valid_change_record(change_record)

    if not response["isValid"]:
        log(f"❌ {response['message']}", AnsiColor.RED, 1)
    else:
        log(f"✅ Change record {change_record} is valid!", AnsiColor.GREEN)


def _validate_yaml(yaml_file: str, schema: str):
    try:
        # Load the YAML file
        with open(yaml_file, 'r') as yf:
            yaml_data = yaml.safe_load(yf)

        # Load the JSON schema
        schema_path = get_resource_path(schema)

        with open(schema_path, 'r') as sf:
            json_schema = json.load(sf)

        validator = Draft7Validator(json_schema)
        errors = list(validator.iter_errors(yaml_data))

        # Check for validation errors
        if errors:
            log("Validation failed! Errors found:", AnsiColor.YELLOW)
            for error in errors:
                log(f"    - {'.'.join(map(str, error.absolute_path))}: {error.message}", AnsiColor.BRIGHT_RED)
            raise typer.Exit(code=1)

        typer.echo("Validation successful! The YAML file is valid. 🥳")
    except FileNotFoundError as fnfe:
        log(f"File not found: {fnfe.filename}", AnsiColor.RED, 1)
    except yaml.YAMLError as ye:
        log(f"Failed to parse YAML: {ye}", AnsiColor.RED, 1)
    except json.JSONDecodeError as je:
        log(f"Failed to parse JSON schema: {je}", AnsiColor.RED, 1)