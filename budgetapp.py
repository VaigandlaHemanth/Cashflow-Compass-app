from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import ScreenManager, Screen
from budget import BudgetingTool

class BudgetingComponent(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 2  # Set the number of columns in the grid layout
        self.budget_tool = BudgetingTool(0)  # Initialize with a default budget of 0

        # Adding widgets for user input
        self.add_widget(Label(text='Budget:'))
        self.budget_input = TextInput(multiline=False)
        self.add_widget(self.budget_input)

        self.add_widget(Label(text='User Name:'))
        self.user_input = TextInput(multiline=False)
        self.add_widget(self.user_input)

        self.add_widget(Label(text='Priority:'))
        self.priority_input = TextInput(multiline=False)
        self.add_widget(self.priority_input)

        # Button to add a user
        add_user_button = Button(text='Add User')
        add_user_button.bind(on_press=self.add_user)
        self.add_widget(add_user_button)

        # Button to allocate budget
        allocate_button = Button(text='Allocate Budget')
        allocate_button.bind(on_press=self.allocate_budget)
        self.add_widget(allocate_button)

        # Adding widgets for item input
        self.add_widget(Label(text='Item Name:'))
        self.item_name_input = TextInput(multiline=False)
        self.add_widget(self.item_name_input)

        self.add_widget(Label(text='Cost:'))
        self.cost_input = TextInput(multiline=False)
        self.add_widget(self.cost_input)

        self.add_widget(Label(text='Time Range:'))
        self.time_range_input = TextInput(multiline=False)
        self.add_widget(self.time_range_input)

        self.add_widget(Label(text='Need:'))
        self.need_input = TextInput(multiline=False)
        self.add_widget(self.need_input)

        self.add_widget(Label(text='Item Priority:'))
        self.item_priority_input = TextInput(multiline=False)
        self.add_widget(self.item_priority_input)

        # Button to add an item
        add_item_button = Button(text='Add Item')
        add_item_button.bind(on_press=self.add_item)
        self.add_widget(add_item_button)

        # Label for displaying output messages
        self.output_label = Label(text='')
        self.add_widget(self.output_label)

    def allocate_budget(self, instance):
        budget_text = self.budget_input.text
        if budget_text.strip():  # Check if input is not empty
            try:
                budget = float(budget_text)
                self.budget_tool.budget = budget  # Update budget in BudgetingTool
                purchased_items, remaining_budget = self.budget_tool.allocate_budget()
                # Format purchased items for display
                purchased_items_formatted = ', '.join([f"{user_name}: {item_name}" for user_name, item_name in purchased_items])
                output_text = f"Purchased items: {purchased_items_formatted}\nRemaining budget: {remaining_budget}"
                # Switch to output screen and display the results
                app = App.get_running_app()
                output_screen = app.screen_manager.get_screen('output')
                output_screen.display_results(output_text)
                app.screen_manager.current = 'output'
            except ValueError:
                self.output_label.text = "Please enter a valid numerical value for the budget."
        else:
            self.output_label.text = "Please enter a budget value."

    def add_user(self, instance):
        user_name = self.user_input.text
        priority_text = self.priority_input.text
        if user_name.strip() and priority_text.strip():  # Check if inputs are not empty
            try:
                priority = int(priority_text)
                # Assuming your BudgetingTool class has an add_user method
                self.budget_tool.add_user(user_name, priority)
                self.output_label.text = f"User {user_name} added with priority {priority}."
            except ValueError:
                self.output_label.text = "Please enter a valid numerical value for priority."
        else:
            self.output_label.text = "Please enter a user name and priority."


    def add_item(self, instance):
        user_name = self.user_input.text
        item_name = self.item_name_input.text
        cost_text = self.cost_input.text
        time_range_text = self.time_range_input.text
        need_text = self.need_input.text
        item_priority_text = self.item_priority_input.text

        if cost_text.strip() and time_range_text.strip() and need_text.strip() and item_priority_text.strip():  # Check if inputs are not empty
            try:
                cost = float(cost_text)
                time_range = int(time_range_text)
                need = float(need_text)
                item_priority = int(item_priority_text)
                self.budget_tool.add_item(user_name, item_name, cost, time_range, need, item_priority)
                self.output_label.text = f"Item {item_name} added for user {user_name}."
            except ValueError:
                self.output_label.text = "Please enter valid numerical values for cost, time range, need, and item priority."
        else:
            self.output_label.text = "Please enter values for all item fields."

class OutputScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = GridLayout(cols=1)  # Set layout
        self.output_label = Label(size_hint_y=None, height=100)  # Label for results
        layout.add_widget(self.output_label)
        back_button = Button(text='Back to Main', size_hint_y=None, height=50)  # Back button
        back_button.bind(on_press=self.switch_back)
        layout.add_widget(back_button)
        self.add_widget(layout)

    def display_results(self, results):
        self.output_label.text = results  # Display results

    def switch_back(self, instance):
        app = App.get_running_app()
        app.screen_manager.current = 'main'  # Switch back to main screen

class BudgetingApp(App):
    def build(self):
        self.screen_manager = ScreenManager()  # Initialize ScreenManager
        self.main_screen = Screen(name='main')  # Main screen
        budgeting_component = BudgetingComponent()  # Budgeting component
        self.main_screen.add_widget(budgeting_component)  # Add to main screen
        self.screen_manager.add_widget(self.main_screen)  # Register main screen
        self.output_screen = OutputScreen(name='output')  # Output screen
        self.screen_manager.add_widget(self.output_screen)  # Register output screen
        return self.screen_manager  # Return the screen manager
    
if __name__ == '__main__':
    BudgetingApp().run()  # Run the app