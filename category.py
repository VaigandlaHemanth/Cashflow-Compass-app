from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.core.window import Window
from categoryapp import CategoryManager
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
        self.top_bar.add_widget(self.cancel_button)
        self.top_bar.add_widget(self.save_button)
        self.add_widget(self.top_bar)

        # Toggle buttons for transaction type
        self.transaction_type_bar = BoxLayout(size_hint_y=None, height=50)
        self.income_button = ToggleButton(text='INCOME', group='transaction_type')
        self.expense_button = ToggleButton(text='EXPENSE', state='down', group='transaction_type')
        self.transfer_button = ToggleButton(text='TRANSFER', group='transaction_type')
        self.transaction_type_bar.add_widget(self.income_button)
        self.transaction_type_bar.add_widget(self.expense_button)
        self.transaction_type_bar.add_widget(self.transfer_button)
        self.add_widget(self.transaction_type_bar)

        # Input fields for Account and Category
        self.account_input = TextInput(hint_text='Account', size_hint_y=None, height=50)
        self.category_manager = CategoryManager()
        self.add_widget(self.category_manager)
        self.add_widget(self.account_input)

        # Input field for notes
        self.notes_input = TextInput(hint_text='Add notes', size_hint_y=None, height=100)
        self.add_widget(self.notes_input)

        # Numeric keypad
        self.keypad = NumericKeypad(size_hint_y=2)
        self.add_widget(self.keypad)

        # Bind the input field to the keypad
        self.keypad.input_field = self.notes_input  # For example, bind to notes_input

        # Set up window size (for demo purposes)
        Window.size = (360, 640)

class MyApp(App):
    def build(self):
        return RecordScreen()

if __name__ == '__main__':
    MyApp().run()
