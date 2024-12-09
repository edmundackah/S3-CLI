import logging
import os

import yaml

from models.app_config_models import AppConfig, ProfileConfig

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")


def load_config(file_path: str, active_profile: str) -> ProfileConfig:
    """Load configuration for the specified active profile."""
    with open(file_path, "r") as file:
        data = yaml.safe_load(file)
    app_config = AppConfig(**data)

    # Get the active profile configuration
    if active_profile not in app_config.profiles:
        raise ValueError(f"Profile '{active_profile}' not found in configuration.")
    return app_config.profiles[active_profile]


class ConfigManager:
    _config = None

    @classmethod
    def get_config(cls):
        if cls._config is None:
            config_path = "resources/config.yaml"
            active_profile = os.getenv("ACTIVE_PROFILE", "default")
            logging.info(f"CLI running with profile: {active_profile}")
            cls._config = load_config(config_path, active_profile)
        return cls._config
