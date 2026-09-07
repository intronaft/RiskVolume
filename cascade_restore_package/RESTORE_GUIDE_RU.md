# Комплект восстановления вкладки «Каскады» для Profit Forge

Эта папка собрана из старой рабочей версии RiskVolume. Она предназначена для
передачи в новую версию проекта и восстановления удаленной функциональности
каскадов, калибровки и связанных с Profit Forge элементов.

## Что находится внутри

- `source_snapshot/cascade_tab.py` — основная вкладка каскадов, таблица заявок,
  расчет распределения, калибровка координат и автоматическая расстановка
  ордеров через `pyautogui`.
- `source_snapshot/main.py` — полный старый файл главного окна. Из него нужно
  перенести интеграционные части, а не заменять им новую версию целиком:
  импорт `CascadeTab`, создание `self.tab_cascade`, добавление вкладки,
  обработку переключения вкладок, горячей клавиши калибровки, запуск
  автоматизации и обновление/масштабирование вкладки.
- `source_snapshot/calculator_tab.py` — связанные с Profit Forge контролы
  пресетов, стекол/рамок предпросмотра и точки калибровки.
- `source_snapshot/settings_dialog.py` — настройки терминала Profit Forge,
  калибровки, координат и связанных параметров.
- `source_snapshot/config.py` — общие пути и настройки старой версии.
- `source_snapshot/translations.py` — строки интерфейса каскадов, калибровки и
  Profit Forge.
- `source_snapshot/logic.py`, `ui_components.py`, `secure_credentials.py` —
  зависимости, которые могут потребоваться при интеграции.
- `source_snapshot/requirements.txt` — зависимости старой версии.
- `data/ScalpSettings_Py_legacy_template.json` — шаблон старой схемы настроек
  с ключами `cas_*`, `calc_points_profit_forge`, `pf_*` и без API-секретов.

## Важные группы данных и ключей

Сохрани совместимость или сделай явную миграцию следующих ключей:

- `cas_p_gear`, `cas_p_left_scrollbar`, `cas_p_book`, `cas_p_scrollbar`;
- `cas_p_vol1`, `cas_p_dist1`, `cas_p_vol2`, `cas_p_dist2`;
- `cas_p_close_x`, `cas_p_btn_add`, `cas_p_btn_del`, `cas_p_combo_vol`;
- `cas_use_custom_vol`, `cas_custom_total_vol`, `cas_use_custom_percent`,
  `cas_custom_percent`;
- `cas_max_count_enabled`, `cas_max_count`, `cas_type_index`,
  `cas_dist_step`, `cas_range_mode`, `cas_range_width`, `cas_manual_k`;
- `last_cascade_count`;
- `calc_points_profit_forge`, `pf_glasses_count`, `pf_glasses_points`,
  `pf_active_glass`, `pf_selected_glasses`, `pf_show_preview_frames`.

## Как восстанавливать в новой версии

1. Сначала изучить текущую архитектуру новой версии и сравнить ее с
   `source_snapshot/main.py`, не перезаписывая новые файлы целиком.
2. Перенести `cascade_tab.py` с адаптацией импортов и текущих типов настроек.
3. Вернуть интеграцию вкладки в главное окно и только связанные с каскадами
   вызовы из старого `main.py`.
4. Вернуть Profit Forge-калибровку и точки/рамки из `calculator_tab.py`,
   `settings_dialog.py` и `translations.py`.
5. Добавить миграцию старых ключей настроек, чтобы новая конфигурация не
   потеряла существующие параметры пользователя.
6. Проверить, что вкладка доступна только для терминала Profit Forge, кнопка
   остановки/ESC работает, координаты калибруются, таблица пересчитывается, а
   автоматическая расстановка не блокирует интерфейс.
7. Запустить существующие тесты и проверить приложение из исходников.

Координаты экранных точек зависят от разрешения, масштаба Windows и конкретного
окна Profit Forge. Их нельзя считать универсальными: после восстановления
проверь калибровку вручную.

