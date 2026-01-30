# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec file for WalletExporter
Creates standalone executables (.app on macOS, .exe on Windows)
Run: pyinstaller WalletExporter.spec
"""

import sys
from pathlib import Path

block_cipher = None

a = Analysis(
    ['src/main.py'],
    pathex=[str(Path.cwd())],
    binaries=[],
    datas=[
        # Include ttkbootstrap theme files
        # PyInstaller should auto-detect, but explicit inclusion ensures themes work
    ],
    hiddenimports=[
        'ttkbootstrap',
        'ttkbootstrap.themes',
        'openpyxl',
        'openpyxl.cell._writer',
        'openpyxl.worksheet',
        'openpyxl.styles',
        'requests',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludedimports=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='WalletExporter',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # No console window (windowed mode)
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # Set to icon path when available (e.g., 'assets/app.icns')
)

# One-folder mode: collects everything in a single folder
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='WalletExporter',
)

# For macOS: Create .app bundle
app = BUNDLE(
    coll,
    name='WalletExporter.app',
    icon=None,  # Set to icon path when available (e.g., 'assets/app.icns')
    bundle_identifier='com.walletexporter.app',
    info_plist={
        'NSPrincipalClass': 'NSApplication',
        'NSHighResolutionCapable': 'True',
    },
)
