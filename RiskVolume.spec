# -*- mode: python ; coding: utf-8 -*-

import json
import os


_SPEC_PATH = globals().get('__file__', os.path.join(os.getcwd(), 'RiskVolume.spec'))
_ROOT = os.path.dirname(os.path.abspath(_SPEC_PATH))
_SRC_SETTINGS = os.path.join(_ROOT, 'ScalpSettings_Py.json')
_SANITIZED_SETTINGS = os.path.join(_ROOT, 'build', 'ScalpSettings_Py.json')


def _build_sanitized_settings(src_path, dst_path):
    try:
        with open(src_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception:
        data = {}

    if not isinstance(data, dict):
        data = {}

    # Reset all calibration/capture points for release build.
    for key in (
        'points',
        'calc_points_profit_forge',
        'calc_points_metascalp',
        'calc_points_tigertrade',
        'calc_points_surf',
        'calc_points_vataga',
    ):
        data[key] = []

    for key in (
        'tiger_open_point',
        'tiger_close_point',
        'surf_open_point',
        'surf_accept_point',
        'vataga_open_point',
        'cas_p_gear',
        'cas_p_left_scrollbar',
        'cas_p_book',
        'cas_p_scrollbar',
        'cas_p_vol1',
        'cas_p_dist1',
        'cas_p_vol2',
        'cas_p_dist2',
        'cas_p_close_x',
        'cas_p_btn_add',
        'cas_p_btn_del',
        'cas_p_combo_vol',
    ):
        data[key] = None

    os.makedirs(os.path.dirname(dst_path), exist_ok=True)
    with open(dst_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False)


_build_sanitized_settings(_SRC_SETTINGS, _SANITIZED_SETTINGS)


a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('Logo', 'Logo'),
        (_SANITIZED_SETTINGS, '.'),
        ('scalp_settings.json', '.'),
    ],
    hiddenimports=[
        'keyboard',
        'pyautogui',
        'pyperclip',
        'qrcode',
        'PIL',
        'mouseinfo',
        'pyscreeze',
        'pygetwindow',
        'pymsgbox',
        'pytweening',
        'pyrect',
        'ccxt',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='RiskVolume',
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
    version='file_version_info.txt',
    icon=['Logo\\Logo.png'],
    contents_directory='internal',
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='RiskVolume',
)
