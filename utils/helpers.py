import re

import typer
from enum import Enum
from typing import Optional
from snow.snow_broker_client import fetch_record
from models.snow_broker_models import ChangeRecordResponse, NotFoundResponse
from utils.config_manager import ConfigManager

config = ConfigManager.get_config()

class TargetServer(str, Enum):
    ECS_S3 = "ECS_S3"
    AWS_S3 = "AWS_S3"


def list_to_array(value: str):
    return value.split(",")

def validate_boolean(value: str):
    if value.lower() not in ["true", "false"]:
        raise typer.BadParameter("Invalid value. Must be 'true' or 'false'")
    return value.lower()


def validate_prefix(prefix: str):
    """Validate that the prefix does not start or end with special characters."""
    if re.match(r"^[^\w]|[^\w]$", prefix):
        raise typer.BadParameter("The prefix cannot start or end with special characters.")
    return prefix


def validate_bucket_name(bucket_name: str):
    """Validate bucket name is non-prod."""
    if bucket_name.startswith("prd") or bucket_name in list_to_array(config.prod_buckets):
        raise typer.BadParameter("Production buckets are not supported by this command")
    return bucket_name


def validate_change_record(change_record: Optional[str], ctx: typer.Context):
    """Validate change record with snow broker service."""
    try:
        bucket_name = ctx.params.get("bucket_name", "").lower()

        if bucket_name.startswith("prd") or bucket_name in list_to_array(config.prod_buckets):
            record = fetch_record(change_record)

            if change_record is None:
                raise typer.BadParameter("A change record is required to modify prod environment")
            elif record and isinstance(record, ChangeRecordResponse):
                if record.valid:
                    return change_record
                else:
                    raise typer.BadParameter(record.invalid_reason)
            elif record and isinstance(record, NotFoundResponse):
                raise typer.BadParameter(record.description)
            else:
                raise typer.BadParameter("Fatal Error: Unable to connect to ServiceNow")
        else:
            return change_record
    except Exception as e:
        print(f"Unexpected Exception: {e}")
        raise typer.BadParameter("Fatal Error: Unable to connect to ServiceNow")

