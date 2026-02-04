"""Configuration loading utilities."""

import json
from pathlib import Path
from typing import Any

from nanobot.config.schema import Config


def get_config_path() -> Path:
    """Get the default configuration file path."""
    return Path.home() / ".nanobot" / "config.json"


def get_data_dir() -> Path:
    """Get the nanobot data directory."""
    from nanobot.utils.helpers import get_data_path
    return get_data_path()


def load_config(config_path: Path | None = None) -> Config:
    """
    Load configuration from file or create default.
    Also merges 'feishu.json' and 'glm.json' if they exist in the same directory.
    
    Args:
        config_path: Optional path to config file. Uses default if not provided.
    
    Returns:
        Loaded configuration object.
    """
    path = config_path or get_config_path()
    data = {}
    
    if path.exists():
        try:
            with open(path) as f:
                data = json.load(f)
        except (json.JSONDecodeError, ValueError) as e:
            print(f"Warning: Failed to load config from {path}: {e}")
            print("Using default configuration.")
            
    # Load separate Feishu config
    feishu_path = path.parent / "feishu.json"
    if feishu_path.exists():
        try:
            with open(feishu_path) as f:
                feishu_data = json.load(f)
                if "channels" not in data:
                    data["channels"] = {}
                # Allow both full structure or direct config
                if "feishu" in feishu_data and isinstance(feishu_data["feishu"], dict):
                    data["channels"]["feishu"] = feishu_data["feishu"]
                else:
                    data["channels"]["feishu"] = feishu_data
        except Exception as e:
            print(f"Warning: Failed to load Feishu config from {feishu_path}: {e}")

    # Load separate GLM (Zhipu) config
    glm_path = path.parent / "glm.json"
    if glm_path.exists():
        try:
            with open(glm_path) as f:
                glm_data = json.load(f)
                if "providers" not in data:
                    data["providers"] = {}
                 # Allow both full structure or direct config
                if "zhipu" in glm_data and isinstance(glm_data["zhipu"], dict):
                    data["providers"]["zhipu"] = glm_data["zhipu"]
                else:
                    data["providers"]["zhipu"] = glm_data
        except Exception as e:
             print(f"Warning: Failed to load GLM config from {glm_path}: {e}")
    
    if not data:
        return Config()

    return Config.model_validate(convert_keys(data))


def save_config(config: Config, config_path: Path | None = None) -> None:
    """
    Save configuration to file.
    
    Args:
        config: Configuration to save.
        config_path: Optional path to save to. Uses default if not provided.
    """
    path = config_path or get_config_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    
    # Convert to camelCase format
    data = config.model_dump()
    data = convert_to_camel(data)
    
    with open(path, "w") as f:
        json.dump(data, f, indent=2)


def convert_keys(data: Any) -> Any:
    """Convert camelCase keys to snake_case for Pydantic."""
    if isinstance(data, dict):
        return {camel_to_snake(k): convert_keys(v) for k, v in data.items()}
    if isinstance(data, list):
        return [convert_keys(item) for item in data]
    return data


def convert_to_camel(data: Any) -> Any:
    """Convert snake_case keys to camelCase."""
    if isinstance(data, dict):
        return {snake_to_camel(k): convert_to_camel(v) for k, v in data.items()}
    if isinstance(data, list):
        return [convert_to_camel(item) for item in data]
    return data


def camel_to_snake(name: str) -> str:
    """Convert camelCase to snake_case."""
    result = []
    for i, char in enumerate(name):
        if char.isupper() and i > 0:
            result.append("_")
        result.append(char.lower())
    return "".join(result)


def snake_to_camel(name: str) -> str:
    """Convert snake_case to camelCase."""
    components = name.split("_")
    return components[0] + "".join(x.title() for x in components[1:])
