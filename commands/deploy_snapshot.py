import os
import sys
import logging
import mimetypes

from commands.remove_objects import remove_objects
from utils.helpers import TargetServer
from utils.s3_server_selector import select_s3_server
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

def deploy_snapshot(
    folder_path: str,
    bucket_name: str,
    prefix: str,
    target_server: TargetServer
):
    """
    The deploy-snapshot command validates a local folder and uploads its contents to an S3 bucket.
    """
    try:

        if not os.path.exists(folder_path):
            logging.error(f"Folder '{folder_path}' does not exist.")
            sys.exit(1)

        remove_objects(bucket_name, prefix, target_server)

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

        logging.info("All files uploaded successfully.")
    except NoCredentialsError:
        logging.error("AWS credentials not found. Please configure them.")
        sys.exit(1)
    except PartialCredentialsError:
        logging.error("Incomplete AWS credentials provided.")
        sys.exit(1)
    except Exception as e:
        logging.critical(f"Critical error: {e}", exc_info=True)
        sys.exit(1)