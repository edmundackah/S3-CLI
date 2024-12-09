import json
import logging
import sys

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
        s3_client.put_object(
            Body=updated_contents,
            Bucket=bucket_name,
            Key=MAINTENANCE_FILE,
            ACL='public-read',
            ContentType="application/json"
        )
        logging.info("Maintenance flags deployed successfully.")
        sys.exit(1)
    except Exception as e:
        logging.error(f"Failed to upload {MAINTENANCE_FILE}: {e}")
        sys.exit(1)