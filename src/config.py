"""
Configuration module for the MCP Cat Server.
"""
import json
import os
from typing import Dict, Any, Optional

# Default settings
DEFAULT_SETTINGS = {
    "cache_file_path": "cat_cache.json"  # Relative to project root by default
}

def get_settings_path() -> str:
    """Get the path to the settings file."""
    return os.path.join(os.path.dirname(os.path.dirname(__file__)), "settings.json")

def load_settings() -> Dict[str, Any]:
    """Load settings from the settings file, or return default settings if the file doesn't exist."""
    settings_path = get_settings_path()
    try:
        if os.path.exists(settings_path):
            with open(settings_path, "r") as f:
                return json.load(f)
        return DEFAULT_SETTINGS
    except (json.JSONDecodeError, IOError) as e:
        print(f"Error loading settings: {e}")
        return DEFAULT_SETTINGS

def get_cache_file_path() -> str:
    """Get the path to the cache file based on settings."""
    settings = load_settings()
    cache_file_path = settings.get("cache_file_path", DEFAULT_SETTINGS["cache_file_path"])
    
    # If the path is relative, make it relative to the project root
    if not os.path.isabs(cache_file_path):
        cache_file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), cache_file_path)
    
    return cache_file_path
