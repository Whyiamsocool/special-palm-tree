# ERC-20 Wallet Transaction Exporter - Development Guidelines

## Project Overview

A cross-platform (Mac/Windows) desktop application to export ERC-20 token transactions from Etherscan to Excel files.

## Technology Stack

- **Python 3.11+** - Primary language
- **ttkbootstrap** - GUI framework (modern Tkinter)
- **openpyxl** - Excel file handling
- **requests** - HTTP client for API calls
- **PyInstaller** - Packaging for distribution

## Project Structure

```
WalletExport/
├── src/
│   ├── main.py              # Application entry point
│   ├── api/
│   │   └── etherscan.py     # Etherscan API client
│   ├── export/
│   │   └── xlsx_handler.py  # Excel read/write operations
│   ├── gui/
│   │   └── app.py           # Main GUI application
│   └── utils/
│       └── helpers.py       # Utility functions
├── requirements.txt
├── CLAUDE.md
└── README.md
```

## Running the Application

```bash
# First time setup - create virtual environment
python3 -m venv venv

# Activate virtual environment
# On Mac/Linux:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# Install dependencies (only needed once)
pip install -r requirements.txt

# Run the application
cd src
python main.py
```

## API Configuration

- **Etherscan API Key**: User provides their own key via GUI input field
- **Get your free API key**: https://etherscan.io/myapikey
- **Rate Limit**: 5 calls/second (free tier)
- **Max Records**: 10,000 per request (use pagination for more)

## Data Format Requirements

### Excel Output Columns (in order)
1. Transaction Hash
2. Blockno
3. UnixTimestamp
4. DateTime (UTC) - **Format: DD/MM/YYYY**
5. From
6. To
7. TokenValue
8. USDValueDayOfTx
9. ContractAddress
10. TokenName
11. TokenSymbol

### Excel Behavior
- When appending to existing file: **paste as values only**
- Never modify existing data, formulas, or formatting
- New data goes below the last row with data

## Coding Standards

### General
- Use type hints for all function parameters and returns
- Include docstrings for all classes and public methods
- Keep functions small and focused (single responsibility)
- Handle errors gracefully with user-friendly messages

### Naming Conventions
- Classes: `PascalCase`
- Functions/variables: `snake_case`
- Constants: `UPPER_SNAKE_CASE`
- Private methods: `_leading_underscore`

### Error Handling
- Always catch specific exceptions, not bare `except:`
- Log errors for debugging
- Show user-friendly error messages in GUI
- Never expose API keys or sensitive data in error messages

### API Calls
- Always handle network errors
- Implement retry logic with exponential backoff
- Respect rate limits (use time.sleep if needed)
- Validate responses before processing

### GUI Guidelines
- Keep UI responsive (use threading for long operations)
- Disable buttons during export to prevent double-clicks
- Show progress for long operations
- Validate input before processing

## Etherscan API Reference

### ERC-20 Token Transfer Events Endpoint
```
https://api.etherscan.io/api
  ?module=account
  &action=tokentx
  &address={wallet_address}
  &startblock=0
  &endblock=99999999
  &sort=asc
  &apikey={api_key}
```

### Response Fields Mapping
| API Field | Excel Column |
|-----------|--------------|
| hash | Transaction Hash |
| blockNumber | Blockno |
| timeStamp | UnixTimestamp |
| timeStamp (converted) | DateTime (UTC) |
| from | From |
| to | To |
| value (with decimals) | TokenValue |
| (not available) | USDValueDayOfTx |
| contractAddress | ContractAddress |
| tokenName | TokenName |
| tokenSymbol | TokenSymbol |

**Note**: USDValueDayOfTx column will be left blank (Etherscan free API doesn't provide this). Users can fill it manually later if needed.

## Testing Commands

```bash
# Run from project root
cd src
python -c "from api.etherscan import EtherscanClient; print('API module OK')"
python -c "from export.xlsx_handler import XlsxHandler; print('Export module OK')"
python -c "from gui.app import WalletExporterApp; print('GUI module OK')"
```

## Packaging for Distribution

```bash
# Install PyInstaller
pip install pyinstaller

# Create executable (run from src directory)
pyinstaller --onefile --windowed --name "WalletExporter" main.py
```

## Common Issues and Solutions

### Rate Limiting
If you see "Max rate limit reached", add delays between API calls:
```python
import time
time.sleep(0.25)  # 250ms delay = 4 calls/second
```

### Large Exports
For wallets with >10,000 transactions, implement pagination using block numbers.

### Date Parsing
Always use UTC for consistency. Convert timestamps like this:
```python
from datetime import datetime, timezone
dt = datetime.fromtimestamp(unix_timestamp, tz=timezone.utc)
formatted = dt.strftime("%d/%m/%Y")
```

## Implementation Priority

1. `utils/helpers.py` - Validation and date utilities
2. `api/etherscan.py` - API client
3. `export/xlsx_handler.py` - Excel operations
4. `gui/app.py` - User interface
5. `main.py` - Wire everything together
6. Testing and packaging
