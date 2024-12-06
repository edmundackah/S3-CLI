import re
import sys
from enum import Enum
from typing import Optional

import typer
from rich.console import Console
from rich.table import Table

from models.snow_broker_models import ChangeRecordResponse, NotFoundResponse
from snow.snow_broker_client import fetch_record
from utils.config_manager import ConfigManager

console = Console()
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
            response = is_valid_change_record(change_record)

            if not response["isValid"]:
                raise typer.BadParameter(response["message"])
            else:
                return change_record
        else:
            return change_record
    except Exception as e:
        raise typer.BadParameter(f"{e}")


def is_valid_change_record(change_record: str):
    record = fetch_record(change_record)
    response = { "isValid": False }

    if change_record is None:
        response["message"] = "A change record is required to modify prod environment"
    elif record and isinstance(record, ChangeRecordResponse):
        if record.valid:
            response["isValid"] = True
        else:
            response["message"] = record.invalid_reason
    elif record and isinstance(record, NotFoundResponse):
        response["message"] = record.description
    else:
        response["message"] = "Fatal Error: Unable to connect to ServiceNow"
    return response


def render_table(data: dict, table_title: str):
    """Render API response as an ASCII table."""
    try:
        if not data:
            console.print("[bold yellow]No data available to render.[/bold yellow]")
            return

        table = Table(title=table_title, show_header=True, header_style="bold blue")

        # Add columns dynamically based on keys in the data
        for key in data.keys():
            table.add_column(key)

        # Add data row
        table.add_row(*[str(value) if value is not None else "N/A" for value in data.values()])

        console.print(table)
        sys.exit(0)
    except Exception as e:
        console.print(f"[bold red]Error rendering table:[/bold red] {e}")