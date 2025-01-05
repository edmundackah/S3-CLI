import logging
import os
import yaml
from typing import Any
from models.app_config_models import AppConfig, ProfileConfig
from utils.file_picker import get_resource_path

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")


def load_config(file_path: str, active_profile: str, env_prefix: str = "S3_CLI_") -> ProfileConfig:
    """Load and validate configuration for the specified active profile, with environment variable overrides."""
    try:
        with open(file_path, "r") as file:
            data = yaml.safe_load(file)
    except FileNotFoundError:
        logging.error(f"Configuration file not found: {file_path}")
        raise
    except yaml.YAMLError as e:
        logging.error(f"Error parsing YAML configuration: {e}")
        raise

    try:
        app_config = AppConfig(**data)
    except Exception as e:
        logging.error(f"Error validating configuration: {e}")
        raise

    if active_profile not in app_config.profiles:
        logging.error(f"Profile '{active_profile}' not found in configuration.")
        raise ValueError(f"Profile '{active_profile}' not found in configuration.")

    # Extract the active profile configuration
    profile_config = app_config.profiles[active_profile].dict()

    # Apply environment variable overrides
    profile_config = apply_env_overrides(profile_config, env_prefix)

    # Re-validate the profile config after overrides
    return ProfileConfig(**profile_config)


def apply_env_overrides(config: dict, env_prefix: str) -> dict:
    """Apply environment variable overrides to the configuration."""
    def set_nested_value(d: dict, keys: list, value: Any):
        """Set a value in a nested dictionary."""
        for key in keys[:-1]:
            d = d.setdefault(key, {})
        d[keys[-1]] = value

    detailed_logging = os.getenv("S3_CLI_LOGGING", "").upper() == "DEBUG"

    for key, value in os.environ.items():
        if key.startswith(env_prefix):
            config_path = key[len(env_prefix):].lower().split("__")
            try:
                typed_value = yaml.safe_load(value)
            except Exception:
                typed_value = value

            if detailed_logging:
                logging.info(
                    f"Detected override: {key} -> {'.'.join(config_path)} = {typed_value}"
                )
            else:
                logging.info(f"Detected override: {key}")

            set_nested_value(config, config_path, typed_value)

    return config


class ConfigManager:
    _config = None

    @classmethod
    def get_config(cls):
        if cls._config is None:
            config_path = os.getenv("CONFIG_PATH", get_resource_path("resources/config.yaml"))
            active_profile = os.getenv("ACTIVE_PROFILE", "default")
            logging.info(f"CLI running with profile: {active_profile}")

            # Load the configuration
            cls._config = load_config(config_path, active_profile)

        return cls._config