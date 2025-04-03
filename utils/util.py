import json

from utils.log_util import log, AnsiColor


def write_json_file(file_path: str, data: dict):
    """Writes JSON file, overwriting existing file if present."""
    log(f"File '{file_path}' created with contents:\n\t{data}\n", AnsiColor.YELLOW)

    try:
        with open(file_path, "w") as f:
            json.dump(data, f, indent=4)
        log(f"Overwritten: {file_path}", AnsiColor.GREEN)
    except Exception as e:
        log(f"Error writing file: {e}", AnsiColor.RED, 1)

def str_to_bool(value):
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.strip().lower() in ("true", "1", "yes")
    return bool(value)