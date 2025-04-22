import logging
import shutil
import zipfile
from datetime import datetime
from pathlib import Path

from botocore.exceptions import ClientError

from utils.helpers import TargetServer
from utils.log_util import log, AnsiColor
from utils.s3_util import select_s3_server


def download_objects(bucket: str, target_server: TargetServer, prefix: str):
    """Downloads all S3 objects (or only those matching a prefix) and zips them."""
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    zip_name = f"{bucket}-{target_server.value}-{timestamp}.zip"
    folder_name = f"s3-download-{bucket}-{timestamp}"
    download_dir = Path.cwd() / folder_name
    zip_path = Path.cwd() / zip_name

    try:
        s3 = select_s3_server(target_server)
        log(f"Fetching object list from bucket '{bucket}'...", AnsiColor.BRIGHT_GREEN)

        response = s3.list_objects_v2(Bucket=bucket, Prefix=prefix or "")
        contents = response.get("Contents", [])

        if not contents:
            log("No objects found for the given bucket and prefix.", AnsiColor.BRIGHT_YELLOW, 1)

        download_dir.mkdir(parents=True, exist_ok=True)

        for obj in contents:
            key = obj["Key"]
            local_path = download_dir / key
            parent_dir = local_path.parent

            if parent_dir.exists() and not parent_dir.is_dir():
                parent_dir.unlink()  # remove file that's blocking the folder
            parent_dir.mkdir(parents=True, exist_ok=True)

            s3.download_file(Bucket=bucket, Key=key, Filename=str(local_path))
            logging.info(f"Downloaded object: {key}")

        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
            for file in download_dir.rglob("*"):
                if file.is_file():
                    zipf.write(file, file.relative_to(download_dir))

        log(f"ZIP file created: {zip_path.name}", AnsiColor.BRIGHT_MAGENTA)

    except ClientError as e:
        log(f"S3 Error: {e}", AnsiColor.BRIGHT_RED, 1)
    except Exception as e:
        log(f"Unexpected Error: {e}", AnsiColor.BRIGHT_RED, 1)
    finally:
        shutil.rmtree(download_dir, ignore_errors=True)