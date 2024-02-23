# user_manager.py

from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from database_manager import DatabaseManager
from kivy.app import App

class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        self.db_manager = DatabaseManager()
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        self.username_input = TextInput(hint_text='Username', multiline=False)
        self.password_input = TextInput(hint_text='Password', password=True, multiline=False)
        login_button = Button(text='Login')
        login_button.bind(on_press=self.login_user)

        layout.add_widget(Label(text='Login'))
        layout.add_widget(self.username_input)
        layout.add_widget(self.password_input)
        layout.add_widget(login_button)

        self.add_widget(layout)

    def login_user(self, instance):
        username = self.username_input.text
        password = self.password_input.text
        # Implement login logic with database verification
        if self.db_manager.validate_user(username, password):
            # Switch to the main app screen on successful login
            self.manager.current = 'main'
        else:
            # Show login error
            pass  # Implement error popup or notification

class RegisterScreen(Screen):
    def __init__(self, **kwargs):
        super(RegisterScreen, self).__init__(**kwargs)
        self.db_manager = DatabaseManager()
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        self.username_input = TextInput(hint_text='Username', multiline=False)
        self.password_input = TextInput(hint_text='Password', password=True, multiline=False)
        self.password_confirm_input = TextInput(hint_text='Confirm Password', password=True, multiline=False)
        register_button = Button(text='Register')
        register_button.bind(on_press=self.register_user)

        layout.add_widget(Label(text='Register'))
        layout.add_widget(self.username_input)
        layout.add_widget(self.password_input)
        layout.add_widget(self.password_confirm_input)
        layout.add_widget(register_button)

        self.add_widget(layout)

    def register_user(self, instance):
        username = self.username_input.text
        password = self.password_input.text
        password_confirm = self.password_confirm_input.text
        # Implement registration logic with database interaction
        if password == password_confirm:
            if self.db_manager.add_user(username, password):
                # Switch to login screen on successful registration
                self.manager.current = 'login'
            else:
                # Show registration error
                pass  # Implement error popup or notification

# Add more classes or methods as needed for session management, user validation, etc.
