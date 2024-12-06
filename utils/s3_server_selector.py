import logging
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
    elif target_server == TargetServer.ECS_S3:
        logging.error(f"{target_server} support is not implemented yet.")
        sys.exit(1)