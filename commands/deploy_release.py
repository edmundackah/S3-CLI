import logging
import mimetypes
import os
import shutil
import sys
import tarfile

import requests

from commands.remove_objects import remove_objects
from utils.helpers import TargetServer
from utils.s3_server_selector import select_s3_server

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

def deploy_release(artifactory_url: str, bucket_name: str, prefix: str, target_server: TargetServer):
    """
    Deploy the release package to an S3 bucket.
    """

    # Download the .tgz file
    tgz_file = artifactory_url.split("/")[-1]
    try:
        logging.info(f"Downloading release package from {artifactory_url}...")
        response = requests.get(artifactory_url, stream=True)
        response.raise_for_status()
        with open(tgz_file, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        logging.info(f"Downloaded {tgz_file} successfully.")
    except Exception as e:
        logging.error(f"Failed to download the release package: {e}")
        sys.exit(1)

    # Extract the .tgz file
    extract_dir = "release_extract"
    try:
        logging.info(f"Extracting {tgz_file}...")
        with tarfile.open(tgz_file, "r:gz") as tar:
            tar.extractall(path=extract_dir)
        logging.info(f"Extracted contents to {extract_dir}.")
    except Exception as e:
        logging.error(f"Failed to extract the release package: {e}")
        _cleanup(tgz_file, extract_dir)
        sys.exit(1)

    # Locate the package/build directory
    build_dir = os.path.join(extract_dir, "package", "build")
    if not os.path.exists(build_dir):
        logging.error(f"The expected directory {build_dir} does not exist.")
        _cleanup(tgz_file, extract_dir)
        sys.exit(1)

    # Upload the contents to S3
    try:
        # Delete current objects
        remove_objects(bucket_name, prefix, target_server)
        logging.info(f"Uploading contents of {build_dir} to bucket {bucket_name} with prefix {prefix}...")

        # Initialise S3 client
        s3_client = select_s3_server(target_server)

        for root, _, files in os.walk(build_dir):
            for file in files:
                local_file_path = os.path.join(root, file)
                relative_path = os.path.relpath(local_file_path, build_dir)
                s3_key = f"{prefix}/{relative_path}".replace("\\", "/")  # Ensure key uses forward slashes

                # Determine Content-Type
                content_type, _ = mimetypes.guess_type(local_file_path)
                content_type = content_type or "text/plain"

                try:
                    logging.info(f"Uploading {local_file_path} to S3://{bucket_name}/{s3_key} with Content-Type: {content_type}")
                    s3_client.upload_file(
                        Filename=local_file_path,
                        Bucket=bucket_name,
                        Key=s3_key,
                        ExtraArgs={
                            'ACL': 'public-read',
                            'ContentType': content_type
                        }
                    )
                    logging.info(f"Uploaded {local_file_path} successfully.")
                except Exception as e:
                    logging.error(f"Failed to upload {local_file_path}: {e}")
                    sys.exit(1)
                logging.info(f"Uploaded {build_dir} to S3://{bucket_name}/{s3_key}.")
        logging.info("Release package deployed successfully.")
    except Exception as e:
        logging.error(f"Failed to upload files to S3: {e}")
        _cleanup(tgz_file, extract_dir)
        sys.exit(1)

    # Clean up temporary files
    _cleanup(tgz_file, extract_dir)
    logging.info("Deployment completed successfully.")


def _cleanup(tgz_file: str, extract_dir: str):
    """
    Clean up temporary files and directories.
    """
    logging.info("Cleaning up temporary files...")
    if os.path.exists(tgz_file):
        os.remove(tgz_file)
        logging.info(f"Removed {tgz_file}.")
    if os.path.exists(extract_dir):
        shutil.rmtree(extract_dir)
        logging.info(f"Removed {extract_dir}.")