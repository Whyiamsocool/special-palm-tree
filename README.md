# WalletExporter

Export ERC-20 token transactions from Etherscan to Excel files.

---

## 🚀 For Non-Technical Users (Fastest Way)

**No coding experience? No problem!**

1. **Download** the app for your computer:
   - **Windows:** Download `WalletExporter.exe` from [Releases](https://github.com/Whyiamsocool/special-palm-tree/releases)
   - **macOS:** Download `WalletExporter.app` from [Releases](https://github.com/Whyiamsocool/special-palm-tree/releases)

2. **Double-click** to open (just like any other app)

3. **Get a free API key:**
   - Go to https://etherscan.io/apis
   - Click "Create Account" (if needed)
   - Paste the API key into the app

4. **Enter your wallet address** (starts with 0x)

5. **Click "Export"** and choose where to save the Excel file

That's it! ✨

---

## Advanced: Run from Source Code

**For developers who want to run from source:**

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

## Advanced: Building Executables (For Developers)

If you want to create your own .app or .exe from the source code:

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

See [BUILD.md](BUILD.md) for detailed build instructions and troubleshooting.

## Features

- 🪙 Export ERC-20 token transactions from any Ethereum wallet
- 📊 Save to Excel with proper formatting
- 📅 Filter by date range
- ⚡ Rate-limited API access (respects Etherscan limits)
- 💾 Persistent configuration (saves your settings)
- 🖥️ Cross-platform (macOS, Windows, Linux)

## Requirements

### Just Want to Use It? (Non-Technical Users)
- **Windows 10+** or **macOS 10.14+**
- **Internet connection** (for Etherscan API)
- **That's all!** No Python, no setup, no coding needed

### Want to Build It Yourself? (Developers)
- **Python 3.11+**
- Basic terminal knowledge
- See [BUILD.md](BUILD.md) for detailed instructions

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
