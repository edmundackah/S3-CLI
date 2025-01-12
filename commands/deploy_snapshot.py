import logging
import os

from commands.remove_objects import remove_objects
from utils.helpers import TargetServer
from utils.log_util import log, AnsiColor
from utils.s3_util import upload_folder_to_s3

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

def deploy_snapshot(folder_path: str, bucket_name: str, prefix: str, target_server: TargetServer):
    """Deploy a local folder to an S3 bucket as a snapshot."""
    if not os.path.exists(folder_path):
        log(f"Folder '{folder_path}' does not exist.", AnsiColor.RED, 1)

    # Remove current objects and upload new ones
    remove_objects(bucket_name, prefix, target_server)
    upload_folder_to_s3(folder_path, bucket_name, prefix, target_server)