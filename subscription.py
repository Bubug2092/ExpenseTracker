from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy_garden.datepicker import DatePicker  # 需要先安裝 kivy_garden.datepicker
import sqlite3
from ui_config import FONT, CATEGORIES

DB_NAME = 'app_data.db'

class SubscriptionScreen(Screen):
    name_input = ObjectProperty(None)
    amount_input = ObjectProperty(None)
    category_spinner = ObjectProperty(None)
    payment_spinner = ObjectProperty(None)
    cycle_spinner = ObjectProperty(None)
    start_date_btn = ObjectProperty(None)
    next_pay_date_btn = ObjectProperty(None)

    start_date = None
    next_pay_date = None

    def on_start_date_press(self):
        self.show_date_picker('選擇開始日期', self.set_start_date)

    def on_next_pay_date_press(self):
        self.show_date_picker('選擇下次付款日', self.set_next_pay_date)

    def show_date_picker(self, title, callback):
        dp = DatePicker()
        popup_layout = BoxLayout(orientation='vertical')
        popup_layout.add_widget(dp)
        btn = Button(text='確認', size_hint_y=None, height=40)
        popup_layout.add_widget(btn)
        popup = Popup(title=title, content=popup_layout, size_hint=(0.8, 0.6))

        def on_confirm(instance):
            selected_date = dp.selection
            if selected_date:
                callback(selected_date)
                popup.dismiss()
            else:
                popup.dismiss()
        btn.bind(on_press=on_confirm)
        popup.open()

    def set_start_date(self, date):
        self.start_date = date
        self.start_date_btn.text = date.strftime('%Y/%m/%d')

    def set_next_pay_date(self, date):
        self.next_pay_date = date
        self.next_pay_date_btn.text = date.strftime('%Y/%m/%d')

    def save_subscription(self):
        name = self.name_input.text.strip()
        amount = self.amount_input.text.strip()
        category = self.category_spinner.text
        payment = self.payment_spinner.text
        cycle = self.cycle_spinner.text
        start_date = self.start_date_btn.text
        next_pay_date = self.next_pay_date_btn.text

        if not all([name, amount, category, payment, cycle, start_date, next_pay_date]):
            self.show_message("請完整填寫所有欄位")
            return

        # 儲存到 SQLite
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS subscriptions
                    (id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT, amount REAL, category TEXT,
                    payment TEXT, cycle TEXT,
                    start_date TEXT, next_pay_date TEXT)''')
        c.execute('''INSERT INTO subscriptions 
                    (name, amount, category, payment, cycle, start_date, next_pay_date)
                    VALUES (?, ?, ?, ?, ?, ?, ?)''',
                  (name, float(amount), category, payment, cycle, start_date, next_pay_date))
        conn.commit()
        conn.close()

        self.show_message("訂閱儲存成功！")

        # 清空輸入
        self.name_input.text = ''
        self.amount_input.text = ''
        self.category_spinner.text = CATEGORIES[0]
        self.payment_spinner.text = '現金'
        self.cycle_spinner.text = '每月'
        self.start_date_btn.text = '開始日期'
        self.next_pay_date_btn.text = '下次付款日'
        self.start_date = None
        self.next_pay_date = None

    def show_message(self, msg):
        popup = Popup(title='訊息',
                      content=Label(text=msg),
                      size_hint=(0.6, 0.4))
        popup.open()
