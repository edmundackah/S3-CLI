from urllib.parse import urljoin

import requests

from models.snow_broker_models import ChangeRecordResponse, NotFoundResponse, ChangeRecordException
from utils.config_manager import ConfigManager

config = ConfigManager.get_config()


def fetch_record(change_record):
    """
    Fetches details for a given record number (change record or incident).

    Parameters:
        change_record (str): The record number (MCR or INC).

    Returns:
        BaseModel: A parsed response object.

    Raises:
        ChangeRecordException: If an unexpected status code is returned.
    """

    if change_record.startswith("MCR"):
        endpoint = f"{config.snow_broker.endpoint.change_record}/{change_record}"
    elif change_record.startswith("INC"):
        endpoint = f"{config.snow_broker.endpoint.incident}/{change_record}"
    else:
        raise ValueError("Invalid record number. Must start with 'MCR' or 'INC'.")

    url = urljoin(config.snow_broker.hostname,endpoint)

    try:
        response = requests.get(url, headers={"Accept": "application/json"})

        if response.status_code == 200:
            return ChangeRecordResponse.parse_obj(response.json())
        elif response.status_code == 404:
            return NotFoundResponse.parse_obj(response.json())
        else:
            raise ChangeRecordException(f"Unexpected status code {response.status_code}: {response.text}")
    except requests.RequestException as e:
        raise ChangeRecordException(f"An error occurred while making the API call: {e}")

