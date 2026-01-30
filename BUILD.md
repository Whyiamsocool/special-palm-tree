# Building WalletExporter Executables

This guide explains how to build standalone executables for Windows (.exe) and macOS (.app) using PyInstaller.

## Overview

PyInstaller bundles your Python application with the Python interpreter and all dependencies into a single executable or folder. Users can then run the application **without installing Python**.

### Build vs Runtime
- **To BUILD:** You need Python 3.11+ and PyInstaller installed
- **To RUN:** Users just need the built executable (NO Python required)

## Prerequisites

### All Platforms
- **Python 3.11+** - Required to build executables
- **Git** - For version control (optional but recommended)

### macOS
- Xcode Command Line Tools (usually installed by default)
- Approximately 1-2 GB free disk space for build artifacts

### Windows
- Approximately 1-2 GB free disk space for build artifacts
- Administrator access (not strictly required, but recommended)

## Setup

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/wallet-exporter.git
cd wallet-exporter
```

### 2. Create Virtual Environment
```bash
python3 -m venv venv

# macOS/Linux
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

This installs:
- `requests` - API client
- `openpyxl` - Excel file handling
- `ttkbootstrap` - GUI framework
- `pyinstaller` - Build tool

## Building

### macOS (.app bundle)

**Recommended method (automated):**
```bash
./build_macos.sh
```

**Manual build:**
```bash
pyinstaller WalletExporter.spec
```

**Output:** `dist/WalletExporter.app`

**To run:**
```bash
open dist/WalletExporter.app
```

Or double-click from Finder.

**First Run Security Warning:**
macOS may show "Cannot verify developer" warning on first run. To fix:
1. Right-click the app → Click "Open"
2. Confirm you want to open it
3. The app will remember and run normally next time

### Windows (.exe)

**Recommended method (automated):**
```bash
build_windows.bat
```

**Manual build:**
```bash
pyinstaller WalletExporter.spec
```

**Output:** `dist\WalletExporter\WalletExporter.exe`

**To run:**
- Double-click `dist\WalletExporter\WalletExporter.exe`
- Or from Command Prompt: `dist\WalletExporter\WalletExporter.exe`

**Windows Defender SmartScreen Warning:**
Windows may warn that the app "is not commonly downloaded." To proceed:
1. Click "More info"
2. Click "Run anyway"
3. The app will be added to trusted list for future runs

**Note:** This is a false positive. PyInstaller-built apps trigger this because they're newly built and haven't been widely distributed. Signing the executable requires a code-signing certificate (future enhancement).

## Build Process Details

### What Happens During Build

1. **Analysis:** PyInstaller scans your code for imports
2. **Collection:** Gathers Python interpreter, standard library, and dependencies
3. **Bundling:** Creates executable or app bundle with all files
4. **Output:**
   - macOS: Creates `WalletExporter.app` (app bundle) in `dist/` folder
   - Windows: Creates `WalletExporter/` folder with executable in `dist/`

### Build Performance

- **First build:** 60-90 seconds (downloads and processes everything)
- **Subsequent builds:** 30-45 seconds (reuses cached dependencies)
- **App startup:** ~1-2 seconds (fast one-folder mode, not one-file)

### Build Artifacts

Generated files in `dist/`:
- **macOS:** `WalletExporter.app/` - Complete app bundle (ready to run)
- **Windows:** `WalletExporter/` - Folder with executable and dependencies

In `build/`:
- Intermediate build files (safe to delete)

In `WalletExporter.spec`:
- PyInstaller configuration (generated during build)

## Troubleshooting

### Build Errors

**"Python not found"**
- Ensure Python 3.11+ is installed and in your PATH
- Test: `python --version` or `python3 --version`

**"PyInstaller not found"**
- Ensure virtual environment is activated
- Reinstall: `pip install pyinstaller>=6.0.0`

**"No module named 'ttkbootstrap'"**
- Dependencies not installed: `pip install -r requirements.txt`

**macOS: "Permission denied" error on build_macos.sh**
```bash
chmod +x build_macos.sh
./build_macos.sh
```

### Runtime Errors

**App crashes on launch**
- Check console for error messages:
  - macOS: Run from Terminal: `open -a Console`
  - Windows: Run from Command Prompt to see error output
- Common causes: Missing API key, invalid wallet address
- Try running from source (with Python) to verify it works: `python src/main.py`

**"ModuleNotFoundError" when running built app**
- Hidden imports missing in spec file
- Report this with error details
- Workaround: Run from source with Python installed

**App runs but API calls fail**
- Check internet connection
- Verify API key is valid (Etherscan.io)
- Check Etherscan API rate limits

### macOS Specific

**"App is damaged" or won't open**
```bash
# Reset executable permissions
chmod +x dist/WalletExporter.app/Contents/MacOS/WalletExporter
```

**Still see security warning after first run**
- Check System Preferences → Security & Privacy
- Click "Open Anyway" for the app

### Windows Specific

**Antivirus flags the executable**
- This is common for newly compiled applications
- Add to antivirus exceptions if trusted
- PyInstaller apps are safe (open source project)

**"VCRUNTIME140.dll not found"**
- Windows needs Visual C++ Runtime
- Download: https://support.microsoft.com/en-us/help/2977003
- Or use `pyinstaller --collect-submodules`

## Distribution

### Sharing Built Executables

**macOS:**
1. Build the app: `./build_macos.sh`
2. Create DMG file (optional):
   ```bash
   hdiutil create -volname WalletExporter -srcfolder dist/WalletExporter.app -ov -format UDZO WalletExporter.dmg
   ```
3. Share `WalletExporter.app` or `WalletExporter.dmg`

**Windows:**
1. Build the app: `build_windows.bat`
2. Zip the folder:
   ```bash
   Compress-Archive -Path dist/WalletExporter -DestinationPath WalletExporter.zip
   ```
3. Share `WalletExporter.zip`

### Future Enhancements

Planned improvements (not yet implemented):
- **Code signing:** Sign executables to avoid security warnings
- **GitHub Releases:** Auto-publish built binaries on releases
- **GitHub Actions:** Automated builds on every release
- **Installer scripts:** MSI (Windows) and DMG (macOS) installers
- **Version auto-updates:** Built-in update checking

## Advanced Configuration

### Customizing the Build

Edit `WalletExporter.spec` to modify:
- **Icon:** Set `icon='path/to/icon.icns'` (macOS) or `icon='path/to/icon.ico'` (Windows)
- **Bundle ID:** Change `bundle_identifier` in the spec file
- **Hidden imports:** Add module names if imports fail
- **Data files:** Include additional resources

### Performance Tuning

Current setup uses **one-folder mode** (recommended):
- Startup time: 1-2 seconds
- File size: ~200-300 MB
- Better for distribution and startup speed

Alternative **one-file mode** (not recommended):
- Startup time: 5-10 seconds (unpacks each time)
- File size: ~150-200 MB
- Slower user experience

## Testing the Built Application

Before distributing, verify:
- [ ] App launches without errors
- [ ] GUI renders correctly
- [ ] Can enter API key and save it
- [ ] Can add/remove wallet addresses
- [ ] Can select date ranges
- [ ] Can perform export and save Excel file
- [ ] Exported Excel file opens correctly
- [ ] Settings persist between app launches
- [ ] Works when moved to different folder location

## Getting Help

If you encounter issues:
1. Check this troubleshooting section
2. Run the app from source with Python to isolate the issue
3. Check the [PyInstaller documentation](https://pyinstaller.org/)
4. Report issues with:
   - OS and version (macOS 12.0, Windows 10, etc.)
   - Python version (`python --version`)
   - Full error message or log
   - Steps to reproduce

## See Also

- [PyInstaller Documentation](https://pyinstaller.org/)
- [ttkbootstrap Documentation](https://ttkbootstrap.readthedocs.io/)
- [openpyxl Documentation](https://openpyxl.readthedocs.io/)
