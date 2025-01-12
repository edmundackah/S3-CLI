import logging

from tabulate import tabulate

from utils.helpers import TargetServer
from utils.log_util import log, AnsiColor
from utils.s3_util import select_s3_server

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

def list_objects(bucket_name: str, prefix: str, target_server: TargetServer):
    """
    List and display objects in an S3 bucket as a table.
    """

    try:
        s3_client = select_s3_server(target_server)

        logging.info(f"Listing objects in bucket '{bucket_name}' with prefix '{prefix}'...")
        response = s3_client.list_objects_v2(Bucket=bucket_name, Prefix=prefix)

        if "Contents" not in response:
            logging.warning(f"No objects found in bucket '{bucket_name}' with prefix '{prefix}'.")
            return

        objects = response["Contents"]
        table_data = []

        for obj in objects:
            key = obj["Key"]
            date_modified = obj["LastModified"].strftime("%d/%m/%Y %H:%M:%S")
            size = obj["Size"]
            table_data.append([key, date_modified, size])

        # Render the table
        table = tabulate(
            table_data,
            headers=["Key", "Date Modified", "Size (Bytes)"],
            tablefmt="grid",
        )
        print(table)

    except Exception as e:
        log(f"Failed to list objects: {e}", AnsiColor.RED, 1)