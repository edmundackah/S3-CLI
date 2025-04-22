import logging
import os
import shutil
import tempfile
import uuid
import zipfile
from datetime import datetime

from botocore.exceptions import ClientError

from utils.helpers import TargetServer
from utils.log_util import AnsiColor, log
from utils.s3_util import select_s3_server


def download_objects(bucket: str, target_server: TargetServer, prefix: str):
    """Downloads all S3 objects (or only those matching a prefix) and zips them."""
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    zip_name = f"{bucket}-{target_server.value}-{timestamp}.zip"
    download_folder = os.path.join(os.getcwd(), f".s3-download-{uuid.uuid4().hex[:8]}")

    try:
        s3 = select_s3_server(target_server)
        log(f"Fetching object list from bucket '{bucket}'...", AnsiColor.BRIGHT_GREEN)

        response = s3.list_objects_v2(Bucket=bucket, Prefix=prefix or "")
        contents = response.get("Contents", [])

        if not contents:
            log("No objects found for the given bucket and prefix.", AnsiColor.BRIGHT_YELLOW, 1)

        os.makedirs(download_folder, exist_ok=True)

        for obj in contents:
            key = obj["Key"]
            local_path = os.path.join(download_folder, key)
            parent_dir = os.path.dirname(local_path)

            # Fix: If a file is blocking creation of a required directory
            if os.path.exists(parent_dir) and not os.path.isdir(parent_dir):
                os.remove(parent_dir)

            os.makedirs(parent_dir, exist_ok=True)

            s3.download_file(Bucket=bucket, Key=key, Filename=local_path)
            logging.info(f"Downloaded object: {key}")

        # Create zip
        zip_path = os.path.join(os.getcwd(), zip_name)
        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
            for root, _, files in os.walk(download_folder):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, download_folder)
                    zipf.write(file_path, arcname)

        log(f"ZIP file created: {zip_name}", AnsiColor.BRIGHT_MAGENTA)

    except ClientError as e:
        log(f"S3 Error: {e}", AnsiColor.BRIGHT_RED, 1)
    except Exception as e:
        log(f"Unexpected Error: {e}", AnsiColor.BRIGHT_RED, 1)
    finally:
        shutil.rmtree(download_folder, ignore_errors=True)