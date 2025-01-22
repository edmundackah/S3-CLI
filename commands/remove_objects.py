import logging
import sys

from utils.helpers import TargetServer
from utils.log_util import AnsiColor, log
from utils.s3_util import select_s3_server

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

def remove_objects(bucket_name: str, prefix: str, target_server: TargetServer):
    """Remove objects from an AWS S3 bucket with the specified prefix."""

    try:
        s3_client = select_s3_server(target_server)

        logging.info(f"Listing objects with prefix '{prefix}' in bucket '{bucket_name}'...")
        response = s3_client.list_objects_v2(Bucket=bucket_name, Prefix=prefix)

        if "Contents" not in response:
            logging.warning(f"No objects found with prefix '{prefix}' in bucket '{bucket_name}'.")
            return

        objects_to_delete = [{"Key": obj["Key"]} for obj in response["Contents"]]
        logging.info(f"Found {len(objects_to_delete)} objects to delete.")

        delete_response = s3_client.delete_objects(
            Bucket=bucket_name,
            Delete={"Objects": objects_to_delete}
        )

        deleted_count = len(delete_response.get("Deleted", []))
        logging.info(f"Successfully deleted {deleted_count} objects.")

        if "Errors" in delete_response:
            log(f"Failed to delete {len(delete_response['Errors'])} objects:", AnsiColor.YELLOW)
            for error in delete_response["Errors"]:
                log(f"- {error['Key']}: {error['Message']}", AnsiColor.RED)
            sys.exit(1)
    except Exception as e:
        log(f"Error during object removal: {e}", AnsiColor.RED, 1)