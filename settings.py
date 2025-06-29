from kivy.uix.screenmanager import Screen
from kivy.properties import NumericProperty, BooleanProperty
from ui_config import FONT, MODULE_VISIBILITY

class SettingsScreen(Screen):
    font_size = NumericProperty(FONT['size'])
    show_budget_bar = BooleanProperty(MODULE_VISIBILITY['budget_bar'])
    show_history_log = BooleanProperty(MODULE_VISIBILITY['history_log'])
    show_settings_button = BooleanProperty(MODULE_VISIBILITY['settings_button'])

    def apply_settings(self):
        # 把設定存回 ui_config.py 或寫入檔案（這邊示意）
        FONT['size'] = self.font_size
        MODULE_VISIBILITY['budget_bar'] = self.show_budget_bar
        MODULE_VISIBILITY['history_log'] = self.show_history_log
        MODULE_VISIBILITY['settings_button'] = self.show_settings_button
        # 實際應用還需重載 UI 或重啟 App 才生效
        print("設定已更新:", FONT, MODULE_VISIBILITY)
