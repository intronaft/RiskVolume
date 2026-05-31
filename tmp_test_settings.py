import sys
sys.path.insert(0, r'd:/Development/RiskVolume-dev')
from PyQt6.QtWidgets import QApplication, QWidget
from settings_dialog import SettingsDialog

class Parent(QWidget):
    def __init__(self):
        super().__init__()
        self.settings = {
            'lang':'ru',
            'scale':100,
            'hk_show':'f1',
            'hk_coords':'f2',
            'use_fee':True,
            'fee_percent':0.1,
            'fee_taker':0.05,
            'fee_maker':0.05,
            'auto_dep_enabled':False,
            'auto_dep_exchange':'binance',
            'auto_dep_market':'futures',
            'auto_dep_asset':'USDT',
            'auto_dep_api_key':'',
            'auto_dep_api_secret':'',
            'auto_dep_api_passphrase':'',
            'auto_dep_connected':False,
            'auto_dep_connected_exchange':'',
            'auto_dep_connected_market':'',
            'auto_dep_allow_unverified':False,
            'prec_dep':2,
            'prec_risk':2,
            'prec_fee':3,
            'prec_lev':1,
        }
    def save_settings(self):
        pass
    def refresh_labels(self):
        pass
    def apply_styles(self):
        pass
    def rebind_hotkeys(self):
        pass
    def update_calc(self):
        pass
    def schedule_update_calc(self):
        pass
    def _apply_auto_deposit_sync(self, force_now=False):
        pass

if __name__ == '__main__':
    app = QApplication([])
    parent = Parent()
    dlg = SettingsDialog(parent)
    print('dialog created')
