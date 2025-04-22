import logging
import os
import shutil
import sys
import tarfile

import requests

from commands.generate_metadata import generate_metadata_file
from commands.remove_objects import remove_objects
from utils.helpers import TargetServer, create_artifact_url
from utils.log_util import AnsiColor, log
from utils.s3_util import upload_folder_to_s3

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

def deploy_release(application: str, version: str, bucket_name: str, prefix: str, target_server: TargetServer):
    """Deploy the release package to an S3 bucket."""

    artifactory_url = create_artifact_url(application, version)
    tgz_file = artifactory_url.split("/")[-1]
    try:
        log(f"Downloading release package from {artifactory_url}...", AnsiColor.BRIGHT_GREEN)
        response = requests.get(artifactory_url, stream=True)
        response.raise_for_status()
        with open(tgz_file, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        log(f"Downloaded {tgz_file} successfully.", AnsiColor.BRIGHT_GREEN)
    except Exception as e:
        log(f"Failed to download the release package: {e}", AnsiColor.RED, 1)

    # Extract the .tgz file
    extract_dir = "release_extract"
    try:
        logging.info(f"Extracting {tgz_file}...")
        with tarfile.open(tgz_file, "r:gz") as tar:
            tar.extractall(path=extract_dir)
        logging.info(f"Extracted contents to {extract_dir}.")
    except Exception as e:
        log(f"Failed to extract the release package: {e}", AnsiColor.RED)
        _cleanup(tgz_file, extract_dir)
        sys.exit(1)

    # Locate the package/build directory
    build_dir = os.path.join(extract_dir, "package", "build")
    if not os.path.exists(build_dir):
        log(f"The expected directory {build_dir} does not exist.", AnsiColor.RED)
        _cleanup(tgz_file, extract_dir)
        sys.exit(1)

    # Remove current objects and upload new ones
    remove_objects(bucket_name, prefix, target_server)
    generate_metadata_file(extract_dir, bucket_name, version)
    upload_folder_to_s3(build_dir, bucket_name, prefix, target_server)

    # Clean up temporary files
    _cleanup(tgz_file, extract_dir)
    log("Deployment completed successfully.", AnsiColor.GREEN)


def _cleanup(tgz_file: str, extract_dir: str):
    """Clean up temporary files and directories."""
    logging.info("Cleaning up temporary files...")
    if os.path.exists(tgz_file):
        os.remove(tgz_file)
        logging.info(f"Removed {tgz_file}.")
    if os.path.exists(extract_dir):
        shutil.rmtree(extract_dir)
        logging.info(f"Removed {extract_dir}.")