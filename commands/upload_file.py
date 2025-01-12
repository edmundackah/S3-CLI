import logging
import mimetypes
import os
import sys

from utils.helpers import TargetServer
from utils.log_util import log, AnsiColor
from utils.s3_util import select_s3_server

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")


def upload_file_to_s3(file_path: str, bucket_name: str, target_server: TargetServer):
    """
    Upload a file to an S3 bucket under a given prefix. The object key will be the file name, optionally prefixed.
    """
    logging.info("Starting file upload...")
    logging.info(f"File Path: {file_path}")
    logging.info(f"Bucket Name: {bucket_name}")

    # Validate file existence
    if not os.path.exists(file_path):
        logging.error(f"The file '{file_path}' does not exist.")
        sys.exit(1)

    file_name = os.path.basename(file_path)
    
    try:
        s3_client = select_s3_server(target_server)

        content_type, _ = mimetypes.guess_type(file_path)
        content_type = content_type or "text/plain"

        # Check if the object exists
        try:
            logging.info(f"Checking if object s3://{bucket_name}/{file_name} exists...")
            s3_client.head_object(Bucket=bucket_name, Key=file_name)

            logging.info("Object exists. Deleting it...")
            s3_client.delete_object(Bucket=bucket_name, Key=file_name)
            logging.info("Object deleted successfully.")
        except s3_client.exceptions.ClientError:
            logging.info("Object does not exist. Proceeding with upload.")

        logging.info(f"Uploading {file_path} to s3://{bucket_name}/{file_name}... with content-type: {content_type}")
        extra_args = {'ContentType': content_type}
        if target_server == TargetServer.AWS_S3:
            extra_args['ServerSideEncryption'] = 'AES256'
        else:
            extra_args['ACL'] = 'public-read'

        s3_client.upload_file(Filename=file_path, Bucket=bucket_name, Key=file_name, ExtraArgs=extra_args)
        log(f"File successfully uploaded to s3://{bucket_name}/{file_name}.", AnsiColor.GREEN)
    except Exception as e:
        log(f"Failed to upload the file: {e}", AnsiColor.RED, 1)