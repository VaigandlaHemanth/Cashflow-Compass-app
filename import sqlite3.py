import sqlite3
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.uix.popup import Popup


class DatabaseManager:
    def __init__(self):
        self.conn = sqlite3.connect('budget.db')
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                                id INTEGER PRIMARY KEY,
                                username TEXT UNIQUE
                            )''')

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS categories (
                                id INTEGER PRIMARY KEY,
                                name TEXT UNIQUE
                            )''')

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS transactions (
                                id INTEGER PRIMARY KEY,
                                user_id INTEGER,
                                category_id INTEGER,
                                month INTEGER,
                                day INTEGER,
                                amount REAL,
                                FOREIGN KEY(user_id) REFERENCES users(id),
                                FOREIGN KEY(category_id) REFERENCES categories(id)
                            )''')
        self.conn.commit()

    def add_user(self, username):
        try:
            self.cursor.execute("INSERT INTO users (username) VALUES (?)", (username,))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def get_users(self):
        self.cursor.execute("SELECT * FROM users")
        return self.cursor.fetchall()

    def add_category(self, category_name):
        try:
            self.cursor.execute("INSERT INTO categories (name) VALUES (?)", (category_name,))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def get_categories(self):
        self.cursor.execute("SELECT * FROM categories")
        return self.cursor.fetchall()

    def add_transaction(self, user_id, category_id, month, day, amount):
        self.cursor.execute("INSERT INTO transactions (user_id, category_id, month, day, amount) "
                            "VALUES (?, ?, ?, ?, ?)", (user_id, category_id, month, day, amount))
        self.conn.commit()


class BudgetApp(App):
    def build(self):
        self.db_manager = DatabaseManager()
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
        self.main_layout.add_widget(self.month_input)
        self.main_layout.add_widget(self.day_input)
        self.main_layout.add_widget(self.amount_input)
        self.main_layout.add_widget(add_transaction_button)

        return self.main_layout

    def add_user(self, instance):
        username = self.user_input.text.strip()
        if username:
            if self.db_manager.add_user(username):
                self.update_user_dropdown()
                self.user_input.text = ''
            else:
                self.show_popup('User already exists')
        else:
            self.show_popup('Please enter a username')

    def update_user_dropdown(self):
        self.user_dropdown.clear_widgets()
        users = self.db_manager.get_users()
        for user in users:
            btn = Button(text=user[1], size_hint_y=None, height=44)
            btn.bind(on_release=lambda btn: self.user_dropdown.select(btn.text))
            self.user_dropdown.add_widget(btn)

    def add_category(self, instance):
        category_name = self.category_input.text.strip()
        if category_name:
            if self.db_manager.add_category(category_name):
                self.update_category_dropdown()
                self.category_input.text = ''
            else:
                self.show_popup('Category already exists')
        else:
            self.show_popup('Please enter a category name')

    def update_category_dropdown(self):
        self.category_dropdown.clear_widgets()
        categories = self.db_manager.get_categories()
        for category in categories:
            btn = Button(text=category[1], size_hint_y=None, height=44)
            btn.bind(on_release=lambda btn: self.category_dropdown.select(btn.text))
            self.category_dropdown.add_widget(btn)

    def add_transaction(self, instance):
        user_text = self.main_layout.children[3].text
        category_text = self.main_layout.children[7].text

        user_id = self.get_user_id(user_text)
        category_id = self.get_category_id(category_text)

        month = self.month_input.text.strip()
        day = self.day_input.text.strip()
        amount = self.amount_input.text.strip()

        if user_id and category_id and month and day and amount:
            self.db_manager.add_transaction(user_id, category_id, month, day, amount)
            self.show_popup('Transaction added successfully')
            self.month_input.text = ''
            self.day_input.text = ''
            self.amount_input.text = ''
        else:
            self.show_popup('Please fill all fields correctly')

    def get_user_id(self, username):
        users = self.db_manager.get_users()
        for user in users:
            if user[1] == username:
                return user[0]
        return None

    def get_category_id(self, category_name):
        categories = self.db_manager.get_categories()
        for category in categories:
            if category[1] == category_name:
                return category[0]
        return None

    def show_popup(self, message):
        popup = Popup(title='Message', content=Label(text=message), size_hint=(None, None), size=(300, 200))
        popup.open()


if __name__ == '__main__':
    BudgetApp().run()
