import base64
import hashlib
import json
import logging
import sys

from botocore.exceptions import BotoCoreError, ClientError

from utils.helpers import TargetServer
from utils.log_util import AnsiColor, log
from utils.s3_util import select_s3_server

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")


def remove_objects(bucket_name: str, prefix: str, target_server: TargetServer):
    """Remove objects from an AWS S3 or ECS S3 bucket with the specified prefix."""

    try:
        s3_client = select_s3_server(target_server)

        logging.info(f"Listing objects with prefix '{prefix}' in bucket '{bucket_name}'...")
        response = s3_client.list_objects_v2(Bucket=bucket_name, Prefix=prefix)

        if "Contents" not in response or not response["Contents"]:
            logging.warning(f"No objects found with prefix '{prefix}' in bucket '{bucket_name}'.")
            return

        objects_to_delete = [{"Key": obj["Key"]} for obj in response["Contents"]]
        logging.info(f"Found {len(objects_to_delete)} objects to delete.")

        # Ensure there are objects to delete
        if not objects_to_delete:
            logging.warning("No objects to delete. Skipping delete request.")
            return

        # AWS S3: Use `delete_objects` for batch deletion
        if target_server == TargetServer.AWS_S3:
            delete_response = s3_client.delete_objects(
                Bucket=bucket_name,
                Delete={"Objects": objects_to_delete, "Quiet": False}
            )

            deleted_count = len(delete_response.get("Deleted", []))
            logging.info(f"Successfully deleted {deleted_count} objects.")

            if "Errors" in delete_response:
                logging.warning(f"Failed to delete {len(delete_response['Errors'])} objects:")
                for error in delete_response["Errors"]:
                    logging.error(f"- {error['Key']}: {error['Message']}")
                sys.exit(1)

        # ECS S3: Use `delete_object` in a loop (avoids ContentMD5 issue)
        else:
            failed_deletions = []
            for obj in objects_to_delete:
                try:
                    s3_client.delete_object(Bucket=bucket_name, Key=obj["Key"])
                    logging.info(f"Deleted {obj['Key']} successfully.")
                except (BotoCoreError, ClientError) as e:
                    logging.error(f"Failed to delete {obj['Key']}: {e}")
                    failed_deletions.append(obj["Key"])

            if failed_deletions:
                logging.warning(f"Failed to delete {len(failed_deletions)} objects.")
                sys.exit(1)

    except (BotoCoreError, ClientError) as e:
        logging.error(f"Error during object removal: {e}")
        sys.exit(1)