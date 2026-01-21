"""
Etherscan API client for fetching ERC-20 token transactions.
"""

import time
import requests
from typing import Callable

# Add parent directory to path for imports
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.helpers import calculate_token_value, unix_to_datetime, format_date_display


class EtherscanAPIError(Exception):
    """Custom exception for Etherscan API errors."""
    pass


class EtherscanClient:
    """Client for interacting with Etherscan API v2."""

    BASE_URL = "https://api.etherscan.io/v2/api"
    CHAIN_ID = 1  # Ethereum Mainnet
    RATE_LIMIT_DELAY = 0.25  # 250ms between requests (4 req/sec, under 5/sec limit)
    MAX_RESULTS_PER_PAGE = 1000  # v2 API: page * offset must be <= 10000

    def __init__(self, api_key: str):
        """
        Initialize the Etherscan client.

        Args:
            api_key: Your Etherscan API key
        """
        self.api_key = api_key
        self._last_request_time = 0

    def _rate_limit(self):
        """Ensure we don't exceed API rate limits."""
        elapsed = time.time() - self._last_request_time
        if elapsed < self.RATE_LIMIT_DELAY:
            time.sleep(self.RATE_LIMIT_DELAY - elapsed)
        self._last_request_time = time.time()

    def _make_request(self, params: dict) -> dict:
        """
        Make a rate-limited request to the Etherscan API.

        Args:
            params: Query parameters

        Returns:
            API response as dictionary

        Raises:
            EtherscanAPIError: If the request fails
        """
        self._rate_limit()

        params["apikey"] = self.api_key
        params["chainid"] = self.CHAIN_ID

        try:
            response = requests.get(self.BASE_URL, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()

            # Check for API-level errors
            if data.get("status") == "0":
                message = data.get("message", "Unknown error")
                result = data.get("result", "")
                # "No transactions found" is not an error
                if "No transactions found" in str(result):
                    return {"status": "1", "result": []}
                raise EtherscanAPIError(f"{message}: {result}")

            return data

        except requests.exceptions.Timeout:
            raise EtherscanAPIError("Request timed out. Please try again.")
        except requests.exceptions.ConnectionError:
            raise EtherscanAPIError("Connection error. Please check your internet connection.")
        except requests.exceptions.RequestException as e:
            raise EtherscanAPIError(f"Request failed: {str(e)}")

    def get_erc20_transactions(
        self,
        address: str,
        start_timestamp: int | None = None,
        end_timestamp: int | None = None,
        progress_callback: Callable[[int, int], None] | None = None
    ) -> list[dict]:
        """
        Fetch all ERC-20 token transactions for a wallet address.

        Args:
            address: Ethereum wallet address
            start_timestamp: Optional start Unix timestamp
            end_timestamp: Optional end Unix timestamp
            progress_callback: Optional callback function(current, total) for progress updates

        Returns:
            List of transaction dictionaries formatted for Excel export
        """
        all_transactions = []
        page = 1
        max_page = 10000 // self.MAX_RESULTS_PER_PAGE  # v2 API limit: page * offset <= 10000

        while page <= max_page:
            params = {
                "module": "account",
                "action": "tokentx",
                "address": address,
                "startblock": 0,
                "endblock": 99999999,
                "page": page,
                "offset": self.MAX_RESULTS_PER_PAGE,
                "sort": "asc"
            }

            data = self._make_request(params)
            transactions = data.get("result", [])

            if not transactions:
                break

            # Filter by timestamp if specified
            for tx in transactions:
                tx_timestamp = int(tx.get("timeStamp", 0))

                # Apply date filters
                if start_timestamp and tx_timestamp < start_timestamp:
                    continue
                if end_timestamp and tx_timestamp > end_timestamp:
                    continue

                # Format transaction for export
                formatted_tx = self._format_transaction(tx)
                all_transactions.append(formatted_tx)

            # Progress update
            if progress_callback:
                progress_callback(len(all_transactions), -1)  # -1 means unknown total

            # Check if we got fewer results than the max (last page)
            if len(transactions) < self.MAX_RESULTS_PER_PAGE:
                break

            page += 1

        return all_transactions

    def _format_transaction(self, tx: dict) -> dict:
        """
        Format a raw transaction into the export format.

        Args:
            tx: Raw transaction from API

        Returns:
            Formatted transaction dictionary
        """
        timestamp = int(tx.get("timeStamp", 0))
        dt = unix_to_datetime(timestamp)

        # Calculate human-readable token value
        raw_value = tx.get("value", "0")
        decimals = int(tx.get("tokenDecimal", 18))
        token_value = calculate_token_value(raw_value, decimals)

        return {
            "Transaction Hash": tx.get("hash", ""),
            "Blockno": tx.get("blockNumber", ""),
            "UnixTimestamp": str(timestamp),
            "DateTime (UTC)": format_date_display(dt),
            "From": tx.get("from", ""),
            "To": tx.get("to", ""),
            "TokenValue": token_value,
            "USDValueDayOfTx": "",  # Left blank as per user preference
            "ContractAddress": tx.get("contractAddress", ""),
            "TokenName": tx.get("tokenName", ""),
            "TokenSymbol": tx.get("tokenSymbol", "")
        }

    def test_connection(self) -> bool:
        """
        Test if the API key is valid.

        Returns:
            True if connection successful, False otherwise
        """
        try:
            params = {
                "module": "stats",
                "action": "ethprice"
            }
            self._make_request(params)
            return True
        except EtherscanAPIError:
            return False
