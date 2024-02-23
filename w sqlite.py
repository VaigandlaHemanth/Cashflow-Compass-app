from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.uix.popup import Popup


class BudgetApp(App):
    def build(self):
        self.main_layout = BoxLayout(orientation='vertical')

        # Input fields for adding user
        self.user_input = TextInput(hint_text='Enter username')
        add_user_button = Button(text='Add User')
        add_user_button.bind(on_press=self.add_user)

        # Input fields for adding category
        self.category_input = TextInput(hint_text='Enter category name')
        add_category_button = Button(text='Add Category')
        add_category_button.bind(on_press=self.add_category)

        # Dropdown for selecting user
        self.user_dropdown = DropDown()
        self.update_user_dropdown()

        user_select_button = Button(text='Select User')
        user_select_button.bind(on_release=self.user_dropdown.open)
        self.user_dropdown.bind(on_select=lambda instance, x: setattr(user_select_button, 'text', x))

        # Dropdown for selecting category
        self.category_dropdown = DropDown()
        self.update_category_dropdown()

        category_select_button = Button(text='Select Category')
        category_select_button.bind(on_release=self.category_dropdown.open)
        self.category_dropdown.bind(on_select=lambda instance, x: setattr(category_select_button, 'text', x))

        # Input fields for adding transaction
        self.year_input = TextInput(hint_text='Enter year')
        self.month_input = TextInput(hint_text='Enter month')
        self.day_input = TextInput(hint_text='Enter day')
        self.amount_input = TextInput(hint_text='Enter amount')

        add_transaction_button = Button(text='Add Transaction')
        add_transaction_button.bind(on_press=self.add_transaction)

        # Add widgets to the main layout
        self.main_layout.add_widget(Label(text='Add User'))
        self.main_layout.add_widget(self.user_input)
        self.main_layout.add_widget(add_user_button)

        self.main_layout.add_widget(Label(text='Select User'))
        self.main_layout.add_widget(user_select_button)

        self.main_layout.add_widget(Label(text='Add Category'))
        self.main_layout.add_widget(self.category_input)
        self.main_layout.add_widget(add_category_button)

        self.main_layout.add_widget(Label(text='Select Category'))
        self.main_layout.add_widget(category_select_button)

        self.main_layout.add_widget(Label(text='Add Transaction'))
        self.main_layout.add_widget(self.year_input)
        self.main_layout.add_widget(self.month_input)
        self.main_layout.add_widget(self.day_input)
        self.main_layout.add_widget(self.amount_input)
        self.main_layout.add_widget(add_transaction_button)

        return self.main_layout

    def add_user(self, instance):
        username = self.user_input.text.strip()
        if username:
            # Placeholder for adding user to the database
            self.update_user_dropdown()
            self.user_input.text = ''
        else:
            self.show_popup('Please enter a username')

    def update_user_dropdown(self):
        # Placeholder for updating the user dropdown
        # You need to fetch users from the database and update the dropdown
        self.user_dropdown.clear_widgets()
        users = ["User1", "User2", "User3"]  # Example list of users, replace it with actual user data
        for user in users:
            btn = Button(text=user, size_hint_y=None, height=44)
            btn.bind(on_release=lambda btn: self.user_dropdown.select(btn.text))
            self.user_dropdown.add_widget(btn)

    def add_category(self, instance):
        category_name = self.category_input.text.strip()
        if category_name:
            # Placeholder for adding category to the database
            self.update_category_dropdown()
            self.category_input.text = ''
        else:
            self.show_popup('Please enter a category name')

    def update_category_dropdown(self):
        # Placeholder for updating the category dropdown
        # You need to fetch categories from the database and update the dropdown
        self.category_dropdown.clear_widgets()
        categories = ["Category1", "Category2", "Category3"]  # Example list of categories, replace it with actual data
        for category in categories:
            btn = Button(text=category, size_hint_y=None, height=44)
            btn.bind(on_release=lambda btn: self.category_dropdown.select(btn.text))
            self.category_dropdown.add_widget(btn)

    def add_transaction(self, instance):
        year = self.year_input.text.strip()
        month = self.month_input.text.strip()
        day = self.day_input.text.strip()
        amount = self.amount_input.text.strip()

        if year and month and day and amount:
            # Placeholder for adding transaction to the database
            self.show_popup('Transaction added successfully')
            self.year_input.text = ''
            self.month_input.text = ''
            self.day_input.text = ''
            self.amount_input.text = ''
        else:
            self.show_popup('Please fill all fields correctly')

    def show_popup(self, message):
        popup = Popup(title='Message', content=Label(text=message), size_hint=(None, None), size=(300, 200))
        popup.open()


if __name__ == '__main__':
    BudgetApp().run()
