"""
Utility functions for wallet address validation and date handling.
"""

import re
from datetime import datetime, timezone


def validate_eth_address(address: str) -> bool:
    """
    Validate an Ethereum wallet address.

    Args:
        address: The wallet address to validate

    Returns:
        True if valid Ethereum address, False otherwise
    """
    if not address:
        return False
    # Ethereum addresses are 42 characters: '0x' + 40 hex characters
    pattern = r'^0x[a-fA-F0-9]{40}$'
    return bool(re.match(pattern, address))


def datetime_to_unix(dt: datetime) -> int:
    """
    Convert a datetime object to Unix timestamp.

    Args:
        dt: datetime object (will be treated as UTC if no timezone)

    Returns:
        Unix timestamp as integer
    """
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return int(dt.timestamp())


def unix_to_datetime(timestamp: int) -> datetime:
    """
    Convert Unix timestamp to datetime object in UTC.

    Args:
        timestamp: Unix timestamp

    Returns:
        datetime object in UTC
    """
    return datetime.fromtimestamp(timestamp, tz=timezone.utc)


def format_date_display(dt: datetime) -> str:
    """
    Format datetime as DD/MM/YYYY for display and Excel export.

    Args:
        dt: datetime object

    Returns:
        Formatted date string
    """
    return dt.strftime("%d/%m/%Y")


def format_datetime_display(dt: datetime) -> str:
    """
    Format datetime as DD/MM/YYYY HH:MM:SS for display.

    Args:
        dt: datetime object

    Returns:
        Formatted datetime string
    """
    return dt.strftime("%d/%m/%Y %H:%M:%S")


def parse_batch_addresses(text: str) -> list[str]:
    """
    Parse multiple wallet addresses from text input.
    Accepts addresses separated by newlines, commas, or spaces.

    Args:
        text: Text containing wallet addresses

    Returns:
        List of valid wallet addresses
    """
    # Split by common separators
    addresses = re.split(r'[,\s\n]+', text.strip())
    # Filter and return only valid addresses
    return [addr.strip() for addr in addresses if validate_eth_address(addr.strip())]


def calculate_token_value(raw_value: str, decimals: int) -> str:
    """
    Convert raw token value to human-readable format.

    Args:
        raw_value: Raw token value from API (as string to handle large numbers)
        decimals: Number of decimal places for the token

    Returns:
        Human-readable token value as string
    """
    if not raw_value or decimals is None:
        return "0"

    try:
        raw_int = int(raw_value)
        if decimals == 0:
            return str(raw_int)

        # Convert to decimal value
        divisor = 10 ** decimals
        whole_part = raw_int // divisor
        decimal_part = raw_int % divisor

        # Format with proper decimal places
        if decimal_part == 0:
            return str(whole_part)

        # Pad decimal part with leading zeros if needed
        decimal_str = str(decimal_part).zfill(decimals).rstrip('0')
        return f"{whole_part}.{decimal_str}"
    except (ValueError, TypeError):
        return "0"


def get_date_range_blocks(start_date: datetime, end_date: datetime) -> tuple[int, int]:
    """
    Get Unix timestamps for date range (start of start_date to end of end_date).

    Args:
        start_date: Start date
        end_date: End date

    Returns:
        Tuple of (start_timestamp, end_timestamp)
    """
    # Start of start_date (00:00:00)
    start_dt = start_date.replace(hour=0, minute=0, second=0, microsecond=0)
    # End of end_date (23:59:59)
    end_dt = end_date.replace(hour=23, minute=59, second=59, microsecond=0)

    return datetime_to_unix(start_dt), datetime_to_unix(end_dt)
