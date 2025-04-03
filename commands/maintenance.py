import json
import logging
import os
import sys

import yaml
from tabulate import tabulate

from utils.helpers import TargetServer
from utils.log_util import log, AnsiColor
from utils.s3_util import select_s3_server
from utils.util import str_to_bool

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
        log(f"An error occurred: {e}", AnsiColor.RED, 1)


def deploy_maintenance(bucket_name: str, flags: str, state: bool, target_server: TargetServer):
    """Deploy or update maintenance flags in an S3 bucket."""
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
        log(f"{MAINTENANCE_FILE} does not exist. Creating a new file.", AnsiColor.BRIGHT_YELLOW)
        data = {}

    # Update or create flags
    for flag in flags.split(","):
        logging.info(f"Setting flag '{flag}' to state '{state}'.")
        data[flag] = str_to_bool(state)

    # Save the updated file back to S3
    updated_contents = json.dumps(data, indent=4)

    try:
        logging.info(f"Uploading updated {MAINTENANCE_FILE} to bucket {bucket_name}...")
        extra_args = {'ContentType': "application/json"}

        if target_server == TargetServer.AWS_S3:
            extra_args['ServerSideEncryption'] = 'AES256'
        else:
            extra_args['ACL'] = 'public-read'

        # Upload the object
        logging.info(f"Uploading maintenance file to S3 bucket {bucket_name}...")
        s3_client.put_object(Body=updated_contents, Bucket=bucket_name, Key=MAINTENANCE_FILE, **extra_args)
        log("Maintenance flags deployed successfully.", AnsiColor.BRIGHT_GREEN)
    except Exception as e:
        log(f"Failed to upload {MAINTENANCE_FILE}: {e}", AnsiColor.RED, 1)


def update_maintenance_flags(yaml_file: str, bucket_name: str, target_server: TargetServer):
    """Update the maintenance flags using the YAML manifest."""

    log(f"Starting maintenance flags update in bucket '{bucket_name}'... Using maintenance file: {yaml_file}",
                AnsiColor.BRIGHT_YELLOW)

    if not os.path.exists(yaml_file):
        log(f"The file '{yaml_file}' does not exist.", AnsiColor.BRIGHT_RED, 1)

    try:
        with open(yaml_file, "r") as file:
            yaml_data = yaml.safe_load(file)
            new_flags = {item["flag"]: str_to_bool(item["state"]) for item in yaml_data["flags"]}
    except yaml.YAMLError as e:
        log(f"Failed to parse YAML file: {e}", AnsiColor.BRIGHT_RED, 1)

    s3_client = select_s3_server(target_server)

    try:
        log(f"Fetching existing '{MAINTENANCE_FILE}' from bucket...", AnsiColor.CYAN)
        response = s3_client.get_object(Bucket=bucket_name, Key=MAINTENANCE_FILE)
        existing_flags = json.loads(response["Body"].read().decode("utf-8"))
    except s3_client.exceptions.NoSuchKey:
        log(f"{MAINTENANCE_FILE} does not exist in bucket '{bucket_name}'. Creating a new one...",
            AnsiColor.BRIGHT_YELLOW)
        existing_flags = {}

    # Compare and update flags
    updated_flags = existing_flags.copy()
    changes = []

    for flag, state in new_flags.items():
        if existing_flags.get(flag) != state:
            changes.append((flag, existing_flags.get(flag), state))
            updated_flags[flag] = state

    if not changes:
        log("No changes detected. Maintenance flags are up-to-date.", AnsiColor.BRIGHT_GREEN)

    log("Applying the following changes:", AnsiColor.BRIGHT_YELLOW)
    for flag, old_state, new_state in changes:
        log(f" - {flag}: {old_state} -> {new_state}", AnsiColor.BLUE)

    # Upload updated maintenance.json
    try:
        extra_args = {'ContentType': "application/json"}

        # Add server-specific parameters
        if target_server == TargetServer.AWS_S3:
            extra_args['ServerSideEncryption'] = 'AES256'
        else:
            extra_args['ACL'] = 'public-read'

        log(f"Uploading updated '{MAINTENANCE_FILE}' to bucket...", AnsiColor.CYAN)
        s3_client.put_object(Bucket=bucket_name, Key=MAINTENANCE_FILE, Body=json.dumps(updated_flags, indent=4), **extra_args)
        log("Maintenance flags updated successfully.", AnsiColor.GREEN)
    except Exception as e:
        log(f"Failed to upload updated {MAINTENANCE_FILE}: {e}", AnsiColor.RED, 1)