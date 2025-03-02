import logging
import mimetypes
import os
import json
import boto3
from botocore.exceptions import BotoCoreError, ClientError

from utils.config_manager import ConfigManager
from utils.helpers import TargetServer
from utils.log_util import AnsiColor, log

config = ConfigManager.get_config()

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

def select_s3_server(target_server: TargetServer):
    logging.info(f"Connecting to S3 Server: {target_server}")

    if target_server == TargetServer.AWS_S3:
        return boto3.client('s3')
    elif target_server == TargetServer.ECS_S3:
        logging.info(f"Accessing ECS_S3 endpoint: {config.ecs_s3.endpoint_url}")
        return boto3.client(
            's3',
            endpoint_url=config.ecs_s3.endpoint_url,
            aws_access_key_id=os.getenv(config.ecs_s3.access_key_var),
            aws_secret_access_key=os.getenv(config.ecs_s3.secret_key_var),
            region_name=config.ecs_s3.region,
            verify=False
        )
    else:
        log(f"{target_server} support is not implemented yet.", AnsiColor.RED, 1)


def sanitize_metadata(metadata: dict) -> dict:
    """Ensure metadata keys start with x-amz-meta- per the Amazon S3 spec."""
    sanitized_metadata = {}
    for key, value in metadata.items():
        sanitized_metadata[key.lower()] = str(value)
    return sanitized_metadata

def upload_folder_to_s3(folder_path: str, bucket_name: str, prefix: str, target_server: TargetServer):
    """Upload the contents of a local folder to an S3 bucket, handling metadata JSON files properly."""
    try:
        s3_client = select_s3_server(target_server)

        for root, _, files in os.walk(folder_path):
            for file in files:
                # Skip metadata JSON files
                if file.endswith(".meta.json"):
                    continue

                local_file_path = os.path.join(root, file)
                relative_path = os.path.relpath(local_file_path, folder_path)
                s3_key = f"{prefix}/{relative_path}".replace("\\", "/")

                # Determine Content-Type
                content_type, _ = mimetypes.guess_type(local_file_path)
                content_type = content_type or "text/plain"

                # Check for associated metadata JSON file
                metadata_file = os.path.join(root, f"{file}.meta.json")
                metadata = {}

                if os.path.exists(metadata_file):
                    try:
                        with open(metadata_file, "r") as f:
                            metadata = json.load(f)
                        metadata = sanitize_metadata(metadata)
                        logging.info(f"Using metadata from {metadata_file}: {metadata}")
                    except Exception as e:
                        logging.warning(f"Failed to read metadata from {metadata_file}: {e}")

                # Apply encryption settings for AWS S3, public-read for ECS S3
                extra_args = {'ContentType': content_type, 'Metadata': metadata}

                if target_server == TargetServer.AWS_S3:
                    extra_args['ServerSideEncryption'] = 'AES256'
                else:
                    extra_args['ACL'] = 'public-read'

                try:
                    with open(local_file_path, 'rb') as file_data:
                        s3_client.put_object(Bucket=bucket_name, Key=s3_key, Body=file_data, **extra_args)

                    logging.info(f"Uploaded {local_file_path} to S3://{bucket_name}/{s3_key} successfully.")
                except (BotoCoreError, ClientError) as e:
                    logging.error(f"Failed to upload {local_file_path}: {e}")

        logging.info("All files uploaded successfully.")
    except Exception as e:
        logging.error(f"Failed to upload files to S3: {e}")