from PyInstaller.building.api import EXE
from PyInstaller.building.build_main import Analysis

block_cipher = None

added_files = [
    ('assets\\icon.ico', '.'),
    ('assets\\start.png', '.'),
    ('assets\\start_disabled.png', '.'),
    ('assets\\stop.png', '.'),
    ('assets\\stop_disabled.png', '.'),
    ('assets\\tray.png', '.'),
]

a = Analysis(
    ['gui.py'],
    pathex='C:\\Users\\MSarabi\\PycharmProjects\\wallpaper_changer',
    binaries=[],
    datas=added_files,
    hiddenimports=[],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='wallpaper_changer',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    upx_exclude=[],
    console=False,
    icon='assets\\icon.ico',
)
