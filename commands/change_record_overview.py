from rich.console import Console

from models.snow_broker_models import ChangeRecordResponse, NotFoundResponse, ChangeRecordException
from snow.snow_broker_client import fetch_record
from utils.helpers import render_table
from utils.log_util import AnsiColor, log

console = Console()

def find_change_record(record_number: str):
    """Validate a record (Change Record or Incident)."""
    try:
        record = fetch_record(record_number)

        if isinstance(record, ChangeRecordResponse):
            render_table(record.model_dump(), table_title=f"Displaying Change Record: {record_number}")
        elif isinstance(record, NotFoundResponse):
            log(f"Record Not Found: {record.description}", AnsiColor.YELLOW, 1)
        else:
            log("Unexpected response type.", AnsiColor.BRIGHT_RED, 1)
    except ChangeRecordException as e:
        log(f"Error: {e}", AnsiColor.RED, 1)
    except Exception as e:
        log(f"An unexpected error occurred: {e}", AnsiColor.RED, 1)