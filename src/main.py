"""
ERC-20 Wallet Transaction Exporter
Main entry point for the application.

Usage:
    python main.py
"""

import sys
from pathlib import Path

# Add src directory to path for imports
src_dir = Path(__file__).parent
sys.path.insert(0, str(src_dir))

from gui.app import WalletExporterApp


def main():
    """Launch the application."""
    app = WalletExporterApp()
    app.run()


if __name__ == "__main__":
    main()
