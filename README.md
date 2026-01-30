# WalletExporter

Export ERC-20 token transactions from Etherscan to Excel files.

---

## 🚀 Download & Run (No Installation Needed!)

**No coding experience? No problem!**

### Step 1: Download
Go to [Releases](https://github.com/Whyiamsocool/special-palm-tree/releases) and download for your OS:
- **Windows:** `WalletExporter.zip` (23.2 MB) - Super fast download!
- **macOS:** `WalletExporter.app.zip` (60 MB)

### Step 2: Extract
Right-click the zip → **Extract All** (or double-click to extract)

### Step 3: Run
- **Windows:** Double-click `WalletExporter.exe`
- **macOS:** Double-click `WalletExporter.app` (if security warning appears, right-click → Open)

### Step 4: Get API Key
1. Go to https://etherscan.io/apis
2. Create account (if needed)
3. Copy your API key

### Step 5: Export
1. Paste API key into app
2. Enter wallet address (0x...)
3. Click "Export"
4. Choose where to save Excel file

**That's it!** ✨ No Python, no setup, no hassle!

---

## For Developers: Run from Source

**If you want to run from source code:**

```bash
# Clone the repository
git clone https://github.com/Whyiamsocool/special-palm-tree.git
cd special-palm-tree

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

## For Developers: Build Executables

**Already built versions are available in [Releases](https://github.com/Whyiamsocool/special-palm-tree/releases).**

To build your own from source:

**macOS:**
```bash
./build_macos.sh
# Creates: dist/WalletExporter.app
```

**Windows:**
```bash
build_windows.bat
# Creates: dist/WalletExporter/WalletExporter.exe
```

See [BUILD.md](BUILD.md) for detailed build instructions, prerequisites, and troubleshooting.

## Features

- 🪙 Export ERC-20 token transactions from any Ethereum wallet
- 📊 Save to Excel with proper formatting
- 📅 Filter by date range
- ⚡ Rate-limited API access (respects Etherscan limits)
- 💾 Persistent configuration (saves your settings)
- 🖥️ Cross-platform (macOS, Windows, Linux)

## Requirements

### To Use the App (Recommended)
- **Windows 10+** or **macOS 10.14+**
- **Internet connection** (for Etherscan API)
- **That's it!** ✅ No Python, no installation, no setup

Just download from [Releases](https://github.com/Whyiamsocool/special-palm-tree/releases) and run!

### To Run from Source Code
- **Python 3.11+**
- Basic terminal knowledge
- See [BUILD.md](BUILD.md)

### To Build Executables
- **Python 3.11+**
- See [BUILD.md](BUILD.md) for detailed build instructions

## How to Use

### Step 1: Get a Free API Key
- Visit https://etherscan.io/apis
- Click "Create Account" (if you don't have one)
- Copy your API key

### Step 2: Open the App
- Double-click `WalletExporter.app` (macOS) or `WalletExporter.exe` (Windows)

### Step 3: Paste API Key
- Paste your Etherscan API key into the "API Key" field
- Click "Save"

### Step 4: Add Your Wallet
- Paste your Ethereum wallet address (starts with 0x)
- Example: `0x742d35Cc6634C0532925a3b844Bc9e7595f42D8e`
- Click "Add to List"

### Step 5: Export Transactions
- (Optional) Select a date range to filter
- Click "Export"
- Choose where to save the Excel file
- Done! Your transactions are in Excel

### Step 6: View Results
- Open the Excel file with Microsoft Excel, Google Sheets, or similar
- See all your transactions with dates, amounts, and details

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

## Getting Help

### Common Issues

**"Cannot verify developer" (macOS)**
- Right-click the app → Click "Open"
- Click "Open" in the confirmation dialog
- The app will remember your choice

**"Windows protected your PC" (Windows)**
- Click "More info"
- Click "Run anyway"
- The app will remember your choice

**"API key not working"**
- Make sure you're on https://etherscan.io/apis (not etherscan.com)
- Copy the entire API key (no extra spaces)
- Some wallets may have API rate limit restrictions

**"Transactions not showing"**
- Check your wallet address starts with `0x`
- Make sure you have an Etherscan API key set
- Check internet connection

### Still Need Help?
- Report issues on [GitHub Issues](https://github.com/Whyiamsocool/special-palm-tree/issues)
- Include: your OS version, what you were trying to do, and any error messages
