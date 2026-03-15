# -*- mode: python ; coding: utf-8 -*-
# PyInstaller spec file for Gerador de Documentos — Ricardo Passos Advocacia
# Build with: pyinstaller build.spec
# Note: Templates .docx are NOT bundled — they are loaded from a user-configured folder.

import os
import customtkinter

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        (os.path.dirname(customtkinter.__file__), 'customtkinter/'),
    ],
    hiddenimports=[
        'customtkinter',
        'docx',
        'openpyxl',
    ],
    hookspath=[],
    hooksconfig={},
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
    name='GeradorDocumentos',
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
)
