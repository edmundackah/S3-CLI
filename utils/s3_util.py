import logging
import mimetypes
import os
import sys

import boto3

from utils.config_manager import ConfigManager
from utils.helpers import TargetServer

config = ConfigManager.get_config()

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

def select_s3_server(target_server: TargetServer):
    # Initialise S3 client
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
        logging.error(f"{target_server} support is not implemented yet.")
        sys.exit(1)


def upload_folder_to_s3(folder_path: str, bucket_name: str, prefix: str, target_server: TargetServer):
    """Upload the contents of a local folder to an S3 bucket."""
    try:
        # Initialise S3 client
        s3_client = select_s3_server(target_server)

        for root, _, files in os.walk(folder_path):
            for file in files:
                local_file_path = os.path.join(root, file)
                relative_path = os.path.relpath(local_file_path, folder_path)
                s3_key = f"{prefix}/{relative_path}".replace("\\", "/")  # Ensure key uses forward slashes

                # Determine Content-Type
                content_type, _ = mimetypes.guess_type(local_file_path)
                content_type = content_type or "text/plain"

                try:
                    logging.info(f"Uploading {local_file_path} to S3://{bucket_name}/{s3_key} with Content-Type: {content_type}")
                    extra_args = {'ContentType': content_type}
                    if target_server == TargetServer.AWS_S3:
                        extra_args['ServerSideEncryption'] = 'AES256'
                    else:
                        extra_args['ACL'] = 'public-read'

                    s3_client.upload_file(Filename=local_file_path, Bucket=bucket_name, Key=s3_key, ExtraArgs=extra_args)
                    logging.info(f"Uploaded {local_file_path} successfully.")
                except Exception as e:
                    logging.error(f"Failed to upload {local_file_path}: {e}")
                    sys.exit(1)

        logging.info("All files uploaded successfully.")
    except Exception as e:
        logging.error(f"Failed to upload files to S3: {e}")
        sys.exit(1)