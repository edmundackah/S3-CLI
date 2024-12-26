import json
import logging
import os
import sys

import typer
import yaml
from tabulate import tabulate

from utils.helpers import TargetServer
from utils.s3_util import select_s3_server

MAINTENANCE_FILE = "maintenance.json"

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")


def verify_maintenance(bucket_name: str, target_server: TargetServer):
    """
    Fetch and display the contents of maintenance.json from S3.
    """
    s3_client = select_s3_server(target_server)

    try:
        logging.info(f"Fetching {MAINTENANCE_FILE} from bucket {bucket_name}...")

        response = s3_client.get_object(Bucket=bucket_name, Key=MAINTENANCE_FILE)
        contents = response["Body"].read().decode("utf-8")

        data = json.loads(contents)
        if not isinstance(data, dict):
            logging.error("Invalid format: Expected a JSON object.")
            sys.exit(1)

        table = [[key, value] for key, value in data.items()]
        print(tabulate(table, headers=["Flag", "State"], tablefmt="grid"))
    except s3_client.exceptions.NoSuchKey:
        logging.info(f"{MAINTENANCE_FILE} does not exist in bucket {bucket_name}.")
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        sys.exit(1)


def deploy_maintenance(bucket_name: str, flags: str, state: bool, target_server: TargetServer):
    """
    Deploy or update maintenance flags in an S3 bucket.
    """
    s3_client = select_s3_server(target_server)

    try:
        # Try to fetch the existing file
        logging.info(f"Fetching {MAINTENANCE_FILE} from bucket {bucket_name}...")
        response = s3_client.get_object(Bucket=bucket_name, Key=MAINTENANCE_FILE)

        contents = response["Body"].read().decode("utf-8")
        data = json.loads(contents)
        logging.info(f"Existing {MAINTENANCE_FILE} file retrieved.")
    except s3_client.exceptions.NoSuchKey:
        # File doesn't exist; start with an empty object
        logging.warning(f"{MAINTENANCE_FILE} does not exist. Creating a new file.")
        data = {}

    # Update or create flags
    for flag in flags.split(","):
        logging.info(f"Setting flag '{flag}' to state '{state}'.")
        data[flag] = state

    # Save the updated file back to S3
    updated_contents = json.dumps(data, indent=4)

    try:
        logging.info(f"Uploading updated {MAINTENANCE_FILE} to bucket {bucket_name}...")
        extra_args = {'ContentType': "application/json"}

        # Add server-specific parameters
        if target_server == TargetServer.AWS_S3:
            extra_args['ServerSideEncryption'] = 'AES256'
        else:
            extra_args['ACL'] = 'public-read'

        # Upload the object
        logging.info(f"Uploading maintenance file to S3 bucket {bucket_name}...")
        s3_client.put_object(Body=updated_contents, Bucket=bucket_name, Key=MAINTENANCE_FILE, **extra_args)
        logging.info("Maintenance flags deployed successfully.")
        sys.exit(1)
    except Exception as e:
        logging.error(f"Failed to upload {MAINTENANCE_FILE}: {e}")
        sys.exit(1)


def update_maintenance_flags(yaml_file: str, bucket_name: str, target_server: TargetServer):
    """
    Update the maintenance flags using the YAML manifest.
    """
    typer.secho(f"Starting maintenance flags update in bucket '{bucket_name}'...\nUsing maintenance file: {yaml_file}",
                fg=typer.colors.YELLOW, bold=True)

    # Validate YAML file exist
    if not os.path.exists(yaml_file):
        typer.secho(f"The file '{yaml_file}' does not exist.", fg=typer.colors.RED, bold=True)
        raise typer.Exit(code=1)

    # Read the YAML file
    try:
        with open(yaml_file, "r") as file:
            yaml_data = yaml.safe_load(file)
            new_flags = {item["flag"]: str(item["state"]).lower() for item in yaml_data["flags"]}
    except yaml.YAMLError as e:
        typer.secho(f"Failed to parse YAML file: {e}", fg=typer.colors.RED, bold=True)
        raise typer.Exit(code=1)

    # Connect to S3
    s3_client = select_s3_server(target_server)

    # Fetch existing maintenance.json or create a new one
    try:
        typer.secho(f"Fetching existing '{MAINTENANCE_FILE}' from bucket...", fg=typer.colors.CYAN)
        response = s3_client.get_object(Bucket=bucket_name, Key=MAINTENANCE_FILE)
        existing_flags = json.loads(response["Body"].read().decode("utf-8"))
    except s3_client.exceptions.NoSuchKey:
        typer.secho(f"{MAINTENANCE_FILE} does not exist in bucket '{bucket_name}'. Creating a new one...",
                    fg=typer.colors.YELLOW, bold=True)
        existing_flags = {}

    # Compare and update flags
    updated_flags = existing_flags.copy()
    changes = []

    for flag, state in new_flags.items():
        if existing_flags.get(flag) != state:
            changes.append((flag, existing_flags.get(flag), state))
            updated_flags[flag] = state

    if not changes:
        typer.secho("No changes detected. Maintenance flags are up-to-date.", fg=typer.colors.GREEN, bold=True)
        raise typer.Exit(code=0)

    # Log changes
    typer.secho("Applying the following changes:", fg=typer.colors.YELLOW, bold=True)
    for flag, old_state, new_state in changes:
        typer.secho(f" - {flag}: {old_state} -> {new_state}", fg=typer.colors.BLUE)

    # Upload updated maintenance.json
    try:
        extra_args = {'ContentType': "application/json"}

        # Add server-specific parameters
        if target_server == TargetServer.AWS_S3:
            extra_args['ServerSideEncryption'] = 'AES256'
        else:
            extra_args['ACL'] = 'public-read'

        typer.secho(f"Uploading updated '{MAINTENANCE_FILE}' to bucket...", fg=typer.colors.CYAN, bold=True)
        s3_client.put_object(Bucket=bucket_name, Key=MAINTENANCE_FILE, Body=json.dumps(updated_flags, indent=4), **extra_args)
        typer.secho("Maintenance flags updated successfully.", fg=typer.colors.GREEN, bold=True)
    except Exception as e:
        typer.secho(f"Failed to upload updated {MAINTENANCE_FILE}: {e}", fg=typer.colors.RED, bold=True)
        raise typer.Exit(code=1)