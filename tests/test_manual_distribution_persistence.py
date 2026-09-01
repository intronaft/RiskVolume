import unittest

from main import RiskVolumeApp


class FakeTable:
    def __init__(self, values):
        self._items = []
        for v in values:
            class FakeCell:
                def __init__(self, text):
                    self._text = text
                def text(self):
                    return self._text
                def setText(self, text):
                    self._text = text
            self._items.append(FakeCell(v))

    def item(self, row, col):
        if row < 0 or row >= len(self._items) or col != 2:
            return None
        return self._items[row]


class ManualDistributionPersistenceTests(unittest.TestCase):
    def test_get_manual_distribution_keeps_nonzero_fallback_when_snapshot_has_blank_rows(self):
        app = RiskVolumeApp.__new__(RiskVolumeApp)
        app.settings = {
            "scalp_manual_multipliers": [10, 20, 30, 40, 50],
            "scalp_manual_multipliers_pos": [10, 0, 0, 0, 0],
            "cells_reversed": False,
            "pos_mode_enabled": False,
        }

        self.assertEqual(app._get_manual_distribution_values(), [10, 20, 30, 40, 50])

    def test_capture_current_distribution_preserves_prior_values_for_blank_cells(self):
        app = RiskVolumeApp.__new__(RiskVolumeApp)
        app.settings = {
            "scalp_manual_multipliers": [10, 20, 30, 40, 50],
            "scalp_manual_multipliers_pos": [10, 20, 30, 40, 50],
            "cells_reversed": False,
            "pos_mode_enabled": False,
        }
        app.cells_table = FakeTable(["10", "", "30", "", "50"])

        app._capture_current_manual_distribution(pos_mode=False)

        self.assertEqual(
            app.settings["scalp_manual_multipliers"],
            [10, 20, 30, 40, 50],
        )

    def test_persist_manual_percent_snapshot_keeps_prior_values_for_empty_cells(self):
        app = RiskVolumeApp.__new__(RiskVolumeApp)
        app.settings = {
            "scalp_manual_multipliers": [10, 20, 30, 40, 50],
            "scalp_manual_multipliers_pos": [10, 20, 30, 40, 50],
            "cells_reversed": False,
            "pos_mode_enabled": False,
        }
        app.cells_table = FakeTable(["10", "", "30", "", "50"])
        app.cb_distribution = type("Cb", (), {"currentIndex": lambda self: 2})()

        app._persist_manual_percent_snapshot(pos_mode=False)

        self.assertEqual(
            app.settings["scalp_manual_multipliers"],
            [10, 20, 30, 40, 50],
        )

    def test_startup_restore_does_not_save_zero_snapshot_over_manual_values(self):
        app = RiskVolumeApp.__new__(RiskVolumeApp)
        app.settings = {
            "scalp_manual_multipliers": [10, 20, 30, 40, 50],
            "scalp_manual_multipliers_pos": [10, 20, 30, 40, 50],
            "cells_reversed": False,
            "pos_mode_enabled": False,
            "scalp_distribution_type": 2,
        }
        app._startup_restore_suppressed = True

        class FakeCell:
            def __init__(self):
                self.text_value = ""
            def text(self):
                return self.text_value
            def setText(self, value):
                self.text_value = value

        class FakeItemChanged:
            def disconnect(self, *args, **kwargs):
                pass
            def connect(self, *args, **kwargs):
                pass

        app.cells_table = type("Table", (), {"itemChanged": FakeItemChanged(), "item": lambda self, row, col: FakeCell()})()
        app.cb_distribution = type(
            "Cb",
            (),
            {"currentIndex": lambda self: 2, "blockSignals": lambda self, value: None, "setCurrentIndex": lambda self, value: None},
        )()
        app.save_cell_settings = lambda: (_ for _ in ()).throw(RuntimeError("startup restore should not persist zero snapshot"))
        app._apply_manual_active_row_flags = lambda: None
        app._update_selected_rows_visuals = lambda: None
        app.update_cell_volumes = lambda: None
        app._get_active_rows_for_table = lambda: set(range(5))
        app.on_table_item_changed = lambda *args, **kwargs: None

        try:
            app._restore_distribution_state(False)
        except RuntimeError as exc:
            self.fail(f"startup restore unexpectedly persisted settings: {exc}")


if __name__ == "__main__":
    unittest.main()
