from kivy.app import App
from datetime import datetime
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.core.window import Window
from categoryapp import CategoryManager
from accountapp import AccountManager
from viewsqlite import insert_transaction
import viewsqlite
import calendar
from datetime import datetime


class NumericKeypad(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 3
        self.create_numeric_buttons()
        self.input_field = None

    def create_numeric_buttons(self):
        # Create buttons with numbers 1-9
        for number in range(1, 10):
            button = Button(text=str(number), on_release=self.button_pressed)
            self.add_widget(button)
        # Create bottom row buttons (+, 0, .)
        self.add_widget(Button(text='+', on_release=self.button_pressed))  # Placeholder for operation
        self.add_widget(Button(text='0', on_release=self.button_pressed))
        self.add_widget(Button(text='.', on_release=self.button_pressed))  # Placeholder for decimal

    def button_pressed(self, instance):
        if self.input_field:
            self.input_field.text += instance.text

class RecordScreen(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 10
        self.spacing = 10

        # Top bar with Cancel and Save buttons
        self.top_bar = BoxLayout(size_hint_y=None, height=50)
        self.cancel_button = Button(text='CANCEL')
        self.save_button = Button(text='SAVE')
        self.save_button.bind(on_release=self.save_account)
        self.top_bar.add_widget(self.cancel_button)
        self.top_bar.add_widget(self.save_button)
        self.add_widget(self.top_bar)
        from kivy.uix.spinner import Spinner

        # Toggle buttons for transaction type
        self.transaction_type_bar = BoxLayout(size_hint_y=None, height=50)
        self.income_button = ToggleButton(text='INCOME', group='transaction_type')
        self.expense_button = ToggleButton(text='EXPENSE', state='down', group='transaction_type')
        self.transfer_button = ToggleButton(text='TRANSFER', group='transaction_type')
        self.transaction_type_bar.add_widget(self.income_button)
        self.transaction_type_bar.add_widget(self.expense_button)
        self.transaction_type_bar.add_widget(self.transfer_button)
        self.add_widget(self.transaction_type_bar)
        self.toggle_buttons = [self.income_button, self.expense_button, self.transfer_button]
        
        current_year = 2024  # Example year, you might want to use datetime.now().year
        year_range = [str(year) for year in range(2000, 2031)]  # Example range

        self.spinner_year = Spinner(text=str(current_year), values=year_range, on_text=self.update_days,size_hint=(0.33, 0.2))
        self.spinner_month = Spinner(text='January', values=list(calendar.month_name)[1:], on_text=self.update_days,size_hint=(0.33, 0.2))
        self.spinner_day = Spinner(text='1', values=[str(day) for day in range(1, 32)],size_hint=(0.33, 0.2))
        self.top_bar = BoxLayout(size_hint_y=0.3)
        self.top_bar.add_widget(self.spinner_year)
        self.top_bar.add_widget(self.spinner_month)
        self.top_bar.add_widget(self.spinner_day)
        self.add_widget(self.top_bar)
        

        self.update_days()


        # Input fields for Account and Category
        self.account_input = AccountManager(size_hint_y=0.2)
        
        # Adjust CategoryManager to take up 20% of the screen
        self.category_manager = CategoryManager(size_hint_y=0.2)
        self.add_widget(self.category_manager)
        
        self.add_widget(self.account_input)

        # Input field for notes
        self.notes_input = TextInput(hint_text='Add notes', size_hint_y=None, height=100)
        self.add_widget(self.notes_input)

        # Numeric keypad
        self.keypad = NumericKeypad(size_hint_y=2)
        self.keypad.input_field = self.notes_input  # Bind the input field to the keypad
        self.add_widget(self.keypad)

        # Set up window size (for demo purposes)
        Window.size = (360, 640)

    def get_selected_date(self):
        """Constructs a date string from the selected spinner values."""
        year = self.spinner_year.text
        month = str(list(calendar.month_name).index(self.spinner_month.text)).zfill(2)
        day = self.spinner_day.text.zfill(2)
        date_str = f"{year}-{month}-{day}"
        return date_str

    # Optionally, convert the string to a datetime.date object
    def get_selected_date_object(self):
        date_str = self.get_selected_date()
        return datetime.strptime(date_str, '%Y-%m-%d').date() 

    def update_days(self, *args):
        year = int(self.spinner_year.text)
        month = list(calendar.month_name).index(self.spinner_month.text)
        last_day = calendar.monthrange(year, month)[1]
        self.spinner_day.values = [str(day) for day in range(1, last_day + 1)]

        # Adjust the day if the current selection is out of the new range
        if int(self.spinner_day.text) > last_day:
            self.spinner_day.text = str(last_day)

    def save_account(self, instance):
        # Attempt to create a database connection
        conn = viewsqlite.create_connection('mydatabase.db')
        if conn is not None:
            viewsqlite.create_table(conn)
            print(self.category_manager.get_selected_category(),self.account_input.get_selected_account())
            # Ensure all inputs are properly retrieved and validated
            try:
                category = self.category_manager.get_selected_category()
                account = self.account_input.get_selected_account()
                amount = self.validate_amount(self.notes_input.text)
                transaction_type = self.get_down_state_text()
                transaction_date = self.get_selected_date_object()
                # Prepare the transaction tuple
                list_finance = (category, account, amount, transaction_type, transaction_date)
                print(list_finance)
                # Insert the transaction and print all transactions
                viewsqlite.insert_transaction(conn, list_finance)
                viewsqlite.select_all_transactions(conn)
            except ValueError as ve:
                print(f"Error saving transaction: {ve}")
            except Exception as e:
                print(f"Saved to database")
            finally:
                # Ensure the database connection is closed after the operation
                conn.close()
        else:
            print("Failed to create database connection.")

    def validate_amount(self, amount_str):
        """Validate and convert the amount to a float."""
        try:
            return float(amount_str)
        except ValueError:
            raise ValueError("Invalid amount format. Please enter a numeric value.")

    def get_down_state_text(self):
        for button in self.toggle_buttons:
            if button.state == 'down':
                return button.text
        return None
class MyApp(App):
    def build(self):
        return RecordScreen()

if __name__ == '__main__':
    MyApp().run()