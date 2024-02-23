from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup

class AccountManager(BoxLayout):
    default_accounts = ['Checking', 'Savings','Debit', 'Credit']
    account_button_text='Select Account'

    def __init__(self, **kwargs):
        super(AccountManager, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.account = None

        # Initialize the dropdown for categories
        self.dropdown = DropDown()

        # Button to select a account
        self.account_button = Button(text=self.account_button_text, size_hint_y=1, height=50)
        self.account_button.bind(on_release=self.dropdown.open)
        self.add_widget(self.account_button)

        # Initially populate the dropdown with default categories
        self.populate_dropdown()

        # Explicitly bind the dropdown select to update the button text
        self.dropdown.bind(on_select=lambda instance, x: setattr(self.account_button, 'text', x))

    @classmethod
    def get_default_accounts(cls):
        """Class method to get the default categories."""
        return cls.default_accounts
    
    @classmethod
    def set_account_button_text(cls, new_text):
        """Set the text on the category selection button."""
        cls.account_button_text = new_text
    
    def on_dropdown_select(self, instance, value):
        # Update the button text and print the selected value
        self.account_button.text = value
        self.account = self.account_button.text
        print(AccountManager.get_default_accounts)
    
    def get_selected_account(self):
        # Assuming you have a way to select or store the current category
        return self.account_button.text
    
    def populate_dropdown(self):
        # Clear the dropdown to repopulate
        self.dropdown.clear_widgets()
        
        for account in self.default_accounts:
            btn = Button(text=account, size_hint_y=None, height=44)
            btn.bind(on_release=lambda btn: self.dropdown.select(btn.text))
            self.dropdown.add_widget(btn)
        
        add_account_btn = Button(text='Add Account', size_hint_y=None, height=44)
        add_account_btn.bind(on_release=self.open_add_account_popup)
        self.dropdown.add_widget(add_account_btn)

    def open_add_account_popup(self, instance):
        content = BoxLayout(orientation='vertical', spacing=5)
        self.new_account_input = TextInput(hint_text='Enter new account', size_hint_y=None, height=30)
        add_button = Button(text='Add', size_hint_y=None, height=50)
        add_button.bind(on_press=self.add_new_account)
        content.add_widget(self.new_account_input)
        content.add_widget(add_button)
        self.popup = Popup(title='Add New Account', content=content, size_hint=(None, None), size=(400, 200))
        self.popup.open()

    def add_new_account(self, instance):
        new_account = self.new_account_input.text.strip()
        if new_account and new_account not in self.default_accounts:
            self.default_accounts.append(new_account)
            self.account_button.text = new_account
            self.populate_dropdown()  # Repopulate the dropdown to include the new account
        self.popup.dismiss()

class AccountApp(App):
    def build(self):
        return AccountManager()

if __name__ == '__main__':
    AccountApp().run()
