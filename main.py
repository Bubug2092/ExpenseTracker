import os
from datetime import date, timedelta
from kivy.app import App
from kivy.lang import Builder
from kivy.core.text import LabelBase
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from db_manager import DBManager

# 註冊中文字體
font_path = os.path.join(os.path.dirname(__file__), "fonts", "MaokenAssortedSans.ttf")
LabelBase.register(name="Maoken", fn_regular=font_path)

# 日期週期計算
def get_next_payment_date(start_date: date, cycle: str, from_date: date = None) -> date:
    if from_date is None:
        from_date = date.today()
    next_date = start_date
    while next_date <= from_date:
        if cycle == "每週":
            next_date += timedelta(weeks=1)
        elif cycle == "每月":
            year = next_date.year + (next_date.month // 12)
            month = next_date.month % 12 + 1
            day = min(next_date.day, 28)
            next_date = date(year, month, day)
        elif cycle == "每年":
            next_date = date(next_date.year + 1, next_date.month, next_date.day)
        else:
            break
    return next_date

# 各頁面類別定義
class MainScreen(Screen):
    pass

class SubscriptionScreen(Screen):
    def save_subscription(self):
        name = self.ids.sub_name.text.strip()
        amount = self.ids.sub_amount.text.strip()
        category = self.ids.sub_category.text
        cycle = self.ids.sub_cycle.text
        start_date = date.today()  # 這裡應接收日期選擇器結果

        if not name or not amount or category == "選擇類別" or cycle == "選擇週期":
            print("❌ 請填寫完整欄位")
            return

        app = App.get_running_app()
        sub_data = {
            "name": name,
            "amount": float(amount),
            "category": category,
            "cycle": cycle,
            "start_date": start_date
        }

        app.db.add_subscription(sub_data)
        print(f"✅ 新增訂閱：{name}")

        self.clear_fields()
        app.root.current = "subscription_list"
        app.root.get_screen("subscription_list").refresh_list()

    def clear_fields(self):
        self.ids.sub_name.text = ""
        self.ids.sub_amount.text = ""
        self.ids.sub_category.text = "選擇類別"
        self.ids.sub_cycle.text = "選擇週期"

class SubscriptionListScreen(Screen):
    def on_pre_enter(self):
        self.refresh_list()

    def refresh_list(self):
        layout = self.ids.sub_list_layout
        layout.clear_widgets()
        subs = App.get_running_app().db.get_all_subscriptions()
        if not subs:
            layout.add_widget(Label(text="⚠️ 尚無訂閱資料"))
            return

        for sub in subs:
            box = BoxLayout(size_hint_y=None, height=40)
            box.add_widget(Label(text=f"{sub['name']} - ${sub['amount']} - {sub['category']} - {sub['cycle']}"))
            btn = Button(text="🗑 刪除", size_hint_x=None, width=80)
            btn.bind(on_release=lambda instance, sid=sub['id']: self.delete_sub(sid))
            box.add_widget(btn)
            layout.add_widget(box)

    def delete_sub(self, sub_id):
        App.get_running_app().db.delete_subscription(sub_id)
        self.refresh_list()

class ExpenseListScreen(Screen):
    def on_pre_enter(self):
        self.refresh_list()

    def refresh_list(self):
        layout = self.ids.expense_list_layout
        layout.clear_widgets()
        selected = self.ids.filter_category.text
        expenses = App.get_running_app().db.get_all_expenses()

        if selected != "全部類別":
            expenses = [e for e in expenses if e["category"] == selected]

        if not expenses:
            layout.add_widget(Label(text="⚠️ 尚無支出資料"))
            return

        for exp in expenses:
            layout.add_widget(Label(text=f"{exp['date']} - {exp['name']} - ${exp['amount']} - {exp['category']}"))

class ExpenseFormScreen(Screen):
    def save_expense(self):
        name = self.ids.expense_name.text.strip()
        amount = self.ids.expense_amount.text.strip()
        category = self.ids.expense_category.text
        method = self.ids.expense_method.text
        expense_date = date.today()  # 日期選擇器未完成，先用今天

        if not name or not amount or category == "選擇類別" or method == "選擇付款方式":
            print("❌ 請填寫完整欄位")
            return

        app = App.get_running_app()
        app.db.add_expense({
            "name": name,
            "amount": float(amount),
            "category": category,
            "date": expense_date
        })

        print(f"✅ 新增支出：{name}，金額：{amount}")
        self.clear_fields()
        app.root.current = "expense_list"
        app.root.get_screen("expense_list").refresh_list()

    def clear_fields(self):
        self.ids.expense_name.text = ""
        self.ids.expense_amount.text = ""
        self.ids.expense_category.text = "選擇類別"
        self.ids.expense_method.text = "選擇付款方式"

# App 主類別
class ExpenseApp(App):
    def build(self):
        self.db = DBManager()
        Builder.load_file("main.kv")

        self.generate_expenses_from_subscriptions()

        sm = ScreenManager()
        sm.add_widget(MainScreen(name="main"))
        sm.add_widget(SubscriptionScreen(name="subscription"))
        sm.add_widget(SubscriptionListScreen(name="subscription_list"))
        sm.add_widget(ExpenseListScreen(name="expense_list"))
        sm.add_widget(ExpenseFormScreen(name="expense_form"))
        return sm

    def generate_expenses_from_subscriptions(self, today=None):
        if today is None:
            today = date.today()
        subscriptions = self.db.get_all_subscriptions()
        for sub in subscriptions:
            next_payment = get_next_payment_date(sub["start_date"], sub["cycle"])
            if next_payment == today:
                self.db.add_expense({
                    "name": sub["name"],
                    "amount": sub["amount"],
                    "category": sub["category"],
                    "date": today
                })

if __name__ == "__main__":
    ExpenseApp().run()
