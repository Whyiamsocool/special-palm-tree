# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A cross-platform (Mac/Windows) desktop application to export ERC-20 token transactions from Etherscan to Excel files.

## Technology Stack

- **Python 3.11+** - Primary language
- **ttkbootstrap** - GUI framework (modern Tkinter)
- **openpyxl** - Excel file handling
- **requests** - HTTP client for API calls
- **PyInstaller** - Packaging for distribution

## Getting Started

### Setup
```bash
# Create virtual environment
python3 -m venv venv

# Activate (Mac/Linux)
source venv/bin/activate
# Activate (Windows)
# venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Running the Application
```bash
cd src
python main.py
```

### Running in PyInstaller
```bash
pip install pyinstaller
cd src
pyinstaller --onefile --windowed --name "WalletExporter" main.py
```

## Architecture

### Core Modules

**`src/api/etherscan.py`** - API client for Etherscan v2 API
- `EtherscanClient`: Handles all API communication with built-in rate limiting (250ms between requests = 4 req/sec)
- `get_erc20_transactions()`: Fetches paginated ERC-20 token transfers with optional timestamp filtering
- `_format_transaction()`: Converts raw API response to export-ready dictionary
- Uses `EtherscanAPIError` for API-specific errors
- Pagination: v2 API constraint is `page * offset <= 10000`, uses 1000 results per page

**`src/export/xlsx_handler.py`** - Excel file operations
- `XlsxHandler`: Creates/updates Excel files with proper formatting
- `HEADERS`: Defines 11 column output format (see Data Format below)
- `create_new_file()`: Creates new file with headers and column widths
- `append_transactions()`: Adds new rows without modifying existing data
- Preserves formatting: frozen header row, bold headers, fixed column widths
- Use `openpyxl` to read/write, always write values-only when appending

**`src/gui/app.py`** - User interface with ttkbootstrap
- `WalletExporterApp`: Main window managing all UI components
- Uses threading (`threading.Thread`) for long operations to keep UI responsive
- `Config` class saves/loads user settings (API key, wallet list)
- Batch mode: stores wallet list as `[(address, file_path, selected_var), ...]`
- Date filtering: `get_date_range_blocks()` converts date range to Unix timestamps
- Disables export button during processing to prevent double-clicks
- Shows progress updates via callback from API client

**`src/utils/helpers.py`** - Utility functions
- `validate_eth_address()`: Validates Ethereum address format
- `calculate_token_value()`: Converts raw token value (with decimals) to human-readable format
- `unix_to_datetime()`: Converts Unix timestamp to datetime object
- `format_date_display()`: Formats datetime as "DD/MM/YYYY" for Excel

**`src/utils/config.py`** - Persistent configuration
- `Config`: Manages saved settings (uses local file storage)
- Saves/loads API key and wallet history

### Data Flow
1. User enters wallet address and API key in GUI
2. GUI spawns thread calling `EtherscanClient.get_erc20_transactions()`
3. Client fetches paginated results from Etherscan API (respects rate limits)
4. For each page, transactions are formatted and filtered by date range
5. `XlsxHandler.append_transactions()` writes to Excel file without overwriting existing data
6. GUI updates with progress and completion status

## Data Format

### Excel Output Columns (in order)
1. Transaction Hash - 70 chars wide
2. Blockno - 12 chars
3. UnixTimestamp - 14 chars
4. DateTime (UTC) - 14 chars, formatted as DD/MM/YYYY
5. From - 45 chars (wallet address)
6. To - 45 chars (wallet address)
7. TokenValue - 20 chars (human-readable with decimals)
8. USDValueDayOfTx - 16 chars (left blank, requires external data)
9. ContractAddress - 45 chars
10. TokenName - 25 chars
11. TokenSymbol - 12 chars

### Excel Behavior
- Headers are frozen on row 1 and bolded
- Each export appends new rows below existing data
- Only values are written (never formulas or special formatting)
- Column widths remain fixed for consistency

## API Specifics

**Etherscan API v2** (not v1)
- Base URL: `https://api.etherscan.io/v2/api`
- Endpoint: `?module=account&action=tokentx&chainid=1&address=...`
- Rate limit: 5 calls/second (code uses 250ms = 4/sec for safety margin)
- Max per request: 1000 results
- Pagination limit: `page * offset <= 10000` (max 10 pages at 1000 per page)
- Response status: `"0"` = error, `"1"` = success
- "No transactions found" is treated as success (empty list)

**API Response → Export Mapping**
- `hash` → Transaction Hash
- `blockNumber` → Blockno
- `timeStamp` (Unix) → UnixTimestamp, DateTime (UTC)
- `from`/`to` → From/To
- `value` (raw with decimals) → TokenValue (converted via `tokenDecimal`)
- `contractAddress` → ContractAddress
- `tokenName`/`tokenSymbol` → TokenName/TokenSymbol

## Testing

```bash
cd src
# Test API client import
python -c "from api.etherscan import EtherscanClient; print('API module OK')"
# Test Excel handler
python -c "from export.xlsx_handler import XlsxHandler; print('Export module OK')"
# Test GUI import
python -c "from gui.app import WalletExporterApp; print('GUI module OK')"
```

## Key Implementation Details

### Timestamp Handling
- API returns Unix timestamps (seconds since epoch)
- Convert to UTC: `datetime.fromtimestamp(unix_ts, tz=timezone.utc)`
- Format for display: `strftime("%d/%m/%Y")` (DD/MM/YYYY)
- Store both UnixTimestamp (raw) and DateTime (UTC) in Excel

### Token Value Conversion
- API returns raw token value (string) with optional `tokenDecimal` field
- Default decimals: 18 (standard ERC-20)
- Conversion: divide raw value by 10^decimals
- Example: raw="1000000000000000000", decimals=18 → 1.0

### Threading Pattern (GUI)
- Long operations run in `threading.Thread(target=func, daemon=True)`
- Use callbacks to update GUI from worker threads
- Disable buttons before spawning thread, re-enable on completion
- Progress callback signature: `callback(current: int, total: int)`

### Path Handling
- Use `pathlib.Path` throughout (not string paths)
- Add `src/` to `sys.path` in entry points to enable module imports
- Works cross-platform (Windows/Mac/Linux)

## Common Patterns

### Adding a New Column to Export
1. Add to `HEADERS` list in `xlsx_handler.py`
2. Add to `COLUMN_WIDTHS` dict
3. Update `_format_transaction()` in `etherscan.py` to populate it from API response
4. Update `append_transactions()` in `xlsx_handler.py` if special handling needed

### Adding Date Filtering
- Use Unix timestamps for API filtering
- `get_date_range_blocks()` converts date objects to Unix timestamps
- Filter transactions in `get_erc20_transactions()` before formatting

### Handling API Errors
- Catch `EtherscanAPIError` (custom exception)
- Show user-friendly message in GUI (never expose raw API response)
- Log to console for debugging if needed
- Status "0" + "No transactions found" message = success (empty list)
