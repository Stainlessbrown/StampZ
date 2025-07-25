# -*- mode: python ; coding: utf-8 -*-
import sys
import os
from PyInstaller.utils.hooks import collect_all

# Safely collect odfpy data files and imports
try:
    datas, binaries, hiddenimports = collect_all('odfpy')
except Exception:
    datas, binaries, hiddenimports = [], [], []

# Add additional hidden imports
hiddenimports += [
    'PIL.Image',
    'PIL.ImageTk',
    'PIL._tkinter_finder',
    'PIL._imaging',
    'PIL._imagingft',
    'PIL._imagingmath',
    'PIL._imagingmorph',
    'PIL.ImageDraw',
    'PIL.ImageFont',
    'PIL.ImageFilter',
    'tkinter',
    'tkinter.filedialog',
    'tkinter.messagebox',
    'tkinter.simpledialog',
    'tkinter.ttk',
    '_tkinter',
    'numpy',
    'colorspacious',
    'odf.opendocument',
    'odf.table',
    'odf.text',
    'odf.style',
    'odf.number',
]

# Platform specific settings
if sys.platform == 'darwin':
    # macOS
    icon_path = 'StampZ.icns' if os.path.exists('StampZ.icns') else None
    onefile = False  # Use --onedir for app bundles
elif sys.platform == 'win32':
    # Windows
    icon_path = 'resources/StampZ.ico' if os.path.exists('resources/StampZ.ico') else None
    onefile = True
else:
    # Linux
    icon_path = None
    onefile = True

# Collect data files - only if they exist
if os.path.exists('resources'):
    datas += [('resources', 'resources')]
if os.path.exists('data'):
    datas += [('data', 'data')]

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=['.'],  # Look for hooks in current directory
    hooksconfig={},
    runtime_hooks=['runtime_hook.py'],
    excludes=[],
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=None)

if onefile:
    exe = EXE(
        pyz,
        a.scripts,
        a.binaries,
        a.datas,
        [],
        name='StampZ',
        debug=False,
        bootloader_ignore_signals=False,
        strip=False,
        upx=True,
        upx_exclude=[],
        runtime_tmpdir=None,
        console=False,
        disable_windowed_traceback=False,
        argv_emulation=False,
        target_arch=None,
        codesign_identity=None,
        entitlements_file=None,
        icon=icon_path,
    )
else:
    exe = EXE(
        pyz,
        a.scripts,
        [],
        exclude_binaries=True,
        name='StampZ',
        debug=False,
        bootloader_ignore_signals=False,
        strip=False,
        upx=True,
        console=False,
        disable_windowed_traceback=False,
        argv_emulation=False,
        target_arch=None,
        codesign_identity=None,
        entitlements_file=None,
        icon=icon_path,
    )
    
    coll = COLLECT(
        exe,
        a.binaries,
        a.datas,
        strip=False,
        upx=True,
        upx_exclude=[],
        name='StampZ',
    )
    
    # macOS app bundle
    if sys.platform == 'darwin':
        app = BUNDLE(
            coll,
            name='StampZ.app',
            icon=icon_path,
            bundle_identifier='com.stainlessbrown.stampz',
            version='1.53',
        )
