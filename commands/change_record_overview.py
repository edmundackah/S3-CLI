import sys

from rich.console import Console

from models.snow_broker_models import ChangeRecordResponse, NotFoundResponse, ChangeRecordException
from snow.snow_broker_client import fetch_record
from utils.helpers import render_table

console = Console()

def find_change_record(record_number: str):
    """Validate a record (Change Record or Incident)."""
    try:
        record = fetch_record(record_number)

        if isinstance(record, ChangeRecordResponse):
            render_table(record.model_dump(), table_title=f"Displaying Change Record: {record_number}")
        elif isinstance(record, NotFoundResponse):
            console.print(f"[bold yellow]Record Not Found:[/bold yellow] {record.description}")
        else:
            console.print("[bold red]Unexpected response type.[/bold red]")
        sys.exit(1)
    except ChangeRecordException as e:
        console.print(f"[bold red]Error: {e}[/bold red]")
        sys.exit(1)
    except Exception as e:
        console.print(f"[bold red]An unexpected error occurred: {e}[/bold red]")
        sys.exit(1)