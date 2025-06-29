from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty

class HomeScreen(Screen):
    name_input = ObjectProperty(None)
    amount_input = ObjectProperty(None)
    category_spinner = ObjectProperty(None)
    payment_spinner = ObjectProperty(None)
    date_picker = ObjectProperty(None)
    history_label = ObjectProperty(None)
    progress_bar = ObjectProperty(None)

    def save_expense(self):
        name = self.name_input.text
        amount = self.amount_input.text
        category = self.category_spinner.text
        payment = self.payment_spinner.text
        date = self.date_picker.text

        print(f"儲存: {name} | {amount} | {category} | {payment} | {date}")
        self.history_label.text = f"最近記錄：{name} - ${amount} - {category}"
