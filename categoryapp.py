from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup

class CategoryManager(BoxLayout):
    default_categories = ['Food', 'Transport', 'Utilities']
    category_button_text='Select Category'
    
    def __init__(self, **kwargs):
        super(CategoryManager, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.category = None

        # Initialize the dropdown for categories
        self.dropdown = DropDown()

        # Button to select a category
        self.category_button = Button(text=self.category_button_text, size_hint_y=1, height=50)
        self.category_button.bind(on_release=self.dropdown.open)
        self.add_widget(self.category_button)

        # Initially populate the dropdown with default categories
        self.populate_dropdown()

        # Explicitly bind the dropdown select to the method to update the button text
        self.dropdown.bind(on_select=self.on_dropdown_select)

    @classmethod
    def get_default_categories(cls):
        """Class method to get the default categories."""
        return cls.default_categories
    
    @classmethod
    def set_category_button_text(cls, new_text):
        """Set the text on the category selection button."""
        cls.category_button_text = new_text


    def on_dropdown_select(self, instance, value):
        """Update the button text and store the selected category."""
        self.category_button.text = value
        self.category = value

    def get_selected_category(self):
        """Return the selected category."""
        return self.category

    def populate_dropdown(self):
        """Populate the dropdown with default categories and an option to add a new category."""
        self.dropdown.clear_widgets()
        
        for category in self.default_categories:
            btn = Button(text=category, size_hint_y=None, height=44)
            btn.bind(on_release=lambda btn: self.dropdown.select(btn.text))
            self.dropdown.add_widget(btn)

        add_category_btn = Button(text='Add Category', size_hint_y=None, height=44)
        add_category_btn.bind(on_release=self.open_add_category_popup)
        self.dropdown.add_widget(add_category_btn)

    def open_add_category_popup(self, instance):
        """Open a popup to add a new category."""
        content = BoxLayout(orientation='vertical', spacing=5)
        self.new_category_input = TextInput(hint_text='Enter new category', size_hint_y=None, height=30)
        add_button = Button(text='Add', size_hint_y=None, height=50)
        add_button.bind(on_press=self.add_new_category)
        content.add_widget(self.new_category_input)
        content.add_widget(add_button)
        self.popup = Popup(title='Add New Category', content=content, size_hint=(None, None), size=(400, 200))
        self.popup.open()

    def add_new_category(self, instance):
        """Add a new category from the popup input."""
        new_category = self.new_category_input.text.strip()
        if new_category and new_category not in self.default_categories:
            self.default_categories.append(new_category)
            self.category_button.text = new_category
            self.populate_dropdown()
        self.popup.dismiss()

class CategoryApp(App):
    def build(self):
        return CategoryManager()

if __name__ == '__main__':
    CategoryApp().run()