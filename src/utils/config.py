"""
Configuration handler for saving/loading user settings.
"""

import json
from pathlib import Path


class Config:
    """Handle saving and loading user configuration."""

    def __init__(self):
        """Initialize config with default path in user's home directory."""
        self.config_dir = Path.home() / ".wallet_exporter"
        self.config_file = self.config_dir / "config.json"
        self._ensure_config_dir()

    def _ensure_config_dir(self):
        """Create config directory if it doesn't exist."""
        self.config_dir.mkdir(exist_ok=True)

    def _load(self) -> dict:
        """Load config from file."""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return {}
        return {}

    def _save(self, data: dict):
        """Save config to file."""
        with open(self.config_file, 'w') as f:
            json.dump(data, f, indent=2)

    def get_api_key(self) -> str:
        """Get saved API key."""
        config = self._load()
        return config.get("api_key", "")

    def save_api_key(self, api_key: str):
        """Save API key."""
        config = self._load()
        config["api_key"] = api_key
        self._save(config)

    def get_last_directory(self) -> str:
        """Get last used directory for file dialogs."""
        config = self._load()
        return config.get("last_directory", str(Path.home()))

    def save_last_directory(self, directory: str):
        """Save last used directory."""
        config = self._load()
        config["last_directory"] = directory
        self._save(config)

    def get_wallet_list(self) -> list[dict]:
        """Get saved wallet list."""
        config = self._load()
        return config.get("wallets", [])

    def save_wallet_list(self, wallets: list[dict]):
        """Save wallet list."""
        config = self._load()
        config["wallets"] = wallets
        self._save(config)
