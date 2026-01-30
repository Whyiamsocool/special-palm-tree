# WalletExporter

Export ERC-20 token transactions from Etherscan to Excel files.

## Quick Start

### Option 1: Pre-built Executables (Recommended for Users)
No Python installation required!

- **macOS:** Download and run `WalletExporter.app`
- **Windows:** Download and run `WalletExporter.exe`

See [Releases](https://github.com/yourusername/wallet-exporter/releases) for pre-built binaries.

### Option 2: Run from Source (For Development)

```bash
# Install Python 3.11+
# Clone the repository
git clone https://github.com/yourusername/wallet-exporter.git
cd wallet-exporter

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Run the application
python src/main.py
```

## Building Executables

To create standalone executables (.app or .exe):

**macOS:**
```bash
./build_macos.sh
```

**Windows:**
```bash
build_windows.bat
```

Output will be in the `dist/` folder.

See [BUILD.md](BUILD.md) for detailed build instructions and troubleshooting.

## Features

- 🪙 Export ERC-20 token transactions from any Ethereum wallet
- 📊 Save to Excel with proper formatting
- 📅 Filter by date range
- ⚡ Rate-limited API access (respects Etherscan limits)
- 💾 Persistent configuration (saves your settings)
- 🖥️ Cross-platform (macOS, Windows, Linux)

## Requirements

### To Run Pre-built Executable
- macOS 10.14+ or Windows 10+
- Internet connection for API calls

### To Run from Source
- Python 3.11+
- Dependencies listed in `requirements.txt`

### To Build Executables
- Python 3.11+
- All runtime dependencies
- PyInstaller

## Usage

1. Get an Etherscan API key (free at https://etherscan.io/apis)
2. Enter your API key in the app
3. Enter Ethereum wallet addresses (0x...)
4. Choose a date range (optional)
5. Click "Export" and select output Excel file
6. Open the resulting Excel file with your transaction data

## Architecture

See [CLAUDE.md](CLAUDE.md) for detailed architecture, API specifics, and development guidelines.

## Contributing

To contribute:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Make your changes
4. Push and create a Pull Request

## License

[Add your license here]

## Support

For issues or questions:
- Check [BUILD.md](BUILD.md) for build troubleshooting
- See [CLAUDE.md](CLAUDE.md) for architecture and implementation details
- Report issues on GitHub
