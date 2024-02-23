from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
import calendar
import datetime
import viewsqlite
from kivy.app import App 
import random
import sqlite3
from sqlite3 import Error
from categoryapp import CategoryManager
from accountapp import AccountManager
from kivy.uix.spinner import Spinner
from kivy.garden.graph import Graph, MeshLinePlot

class AdvancedCalendar(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 10
        self.spacing = 10
        self.date = datetime.date.today()
        self.calendar = calendar.Calendar()
        self.view_mode = 'month'  # Can be 'month' or 'day'
        
        # Navigation and view toggle
        nav_layout = BoxLayout(size_hint_y=None, height=50)
        self.prev_button = Button(text='<<', font_size=16, size_hint=(0.2, 1), on_press=self.prev)
        self.next_button = Button(text='>>', font_size=16, size_hint=(0.2, 1), on_press=self.next)
        self.view_toggle_button = Button(text='Switch View', font_size=16, size_hint=(0.2, 1),on_press=self.toggle_view)
        self.view_toggle_button = Button(text='Switch View', font_size=16, size_hint=(0.2, 1),on_press=self.toggle_view)
        self.current_label = Label(text='', font_size=16)
        self.spinner = Spinner(
            # Provide the options to choose from
            values=('INCOME', 'TRANSFER', 'EXPENSE'),
            # Default text that is displayed
            text='MODE',
            # Callback for when an option is selected
            on_text=self.on_spinner_select,
            size_hint=(0.3, 1)
        )

        self.graph = Spinner(
            # Provide the options to choose from
            values=('Day', 'Month', 'Year',"ALL TIME"),
            # Default text that is displayed
            text='Time',
            # Callback for when an option is selected
            on_text=self.on_spinner_select,
            size_hint=(0.3, 1)
        )

        
        nav_layout.add_widget(self.prev_button)
        nav_layout.add_widget(self.current_label)
        nav_layout.add_widget(self.next_button)
        CategoryManager.set_category_button_text("Category")
        AccountManager.set_account_button_text("Account")
        self.account_input = AccountManager(size_hint=(0.3, 1))
        AccountManager.set_account_button_text("Select Account")
        self.category_manager = CategoryManager(size_hint=(0.3,1))
        CategoryManager.set_category_button_text("Select Category")
        nav_layout.add_widget(self.category_manager)
        nav_layout.add_widget(self.account_input)
        nav_layout.add_widget(self.spinner)
        nav_layout.add_widget(self.view_toggle_button)
        nav_layout.add_widget(self.graph)
        
        # Dynamic content area
        self.content_layout = BoxLayout()
        self.month_layout = GridLayout(cols=7)  # Placeholder for month view
        self.day_layout = BoxLayout(orientation='vertical')  # Placeholder for day view
        
        self.add_widget(nav_layout)
        self.add_widget(self.content_layout)
        
        self.update_view()   

    def toggle_view(self, instance):
        # Toggle between month/day and graph view
        if self.view_mode not in ['month', 'day']:
            self.view_mode = 'month'  # Default to month view if not currently in month or day view
        else:
            # Switch to graph view
            self.view_mode = 'graph'
            self.update_view()

    def get_values(self): 
        category = self.category_manager.get_selected_category()
        account = self.account_input.get_selected_account()
        transaction_type = self.spinner.text
        return(category, account, transaction_type)

    def on_spinner_select(self, spinner, text):
        print(f'Selected value: {text}')

    def update_view(self):
        # Clear the current view
        self.content_layout.clear_widgets()
        
        if self.view_mode == 'month':
            self.update_month_view()
            self.content_layout.add_widget(self.month_layout)
            self.current_label.text = self.date.strftime('%B %Y')
        elif self.view_mode == 'day':
            self.update_day_view()
            self.content_layout.add_widget(self.day_layout)
            self.current_label.text = self.date.strftime('%A, %B %d,\n %Y')
        elif self.view_mode == 'graph':
            self.update_graph_view()
    
    def update_graph_view(self):
        # Initialize Graph widget
        graph = Graph(xlabel='Date', ylabel='Amount', x_ticks_minor=5,
                      x_ticks_major=25, y_ticks_major=1,
                      y_grid_label=True, x_grid_label=True, padding=5,
                      x_grid=True, y_grid=True, xmin=0, xmax=50, ymin=0, ymax=10)
        plot = MeshLinePlot(color=[1, 0, 0, 1])
        graph.add_plot(plot)

        # Fetch transactions that match the selected criteria and update the plot
        conn = viewsqlite.create_connection('mydatabase.db')
        category, account, transaction_type = self.get_values()
        transactions = self.fetch_filtered_transactions(conn, category, account, transaction_type)
        if transactions:
            # Prepare plot points (example: using transaction amounts)
            plot_points = [(i, transaction[3]) for i, transaction in enumerate(transactions)]
            plot.points = plot_points
            # Adjust graph bounds based on the transactions
            graph.xmax = len(transactions) + 1
            graph.ymax = max(plot_points, key=lambda x: x[1])[1] + 1

        self.content_layout.add_widget(graph)
    
    def fetch_filtered_transactions(self, conn, category, account, transaction_type):
        # This method assumes you modify `select_all_transactions` to accept filters and return filtered transactions
        return viewsqlite.select_filtered_transactions(conn, category, account, transaction_type)
    
    def update_month_view(self):
        self.month_layout.clear_widgets()
        for week in self.calendar.monthdays2calendar(self.date.year, self.date.month):
            for day, day_of_week in week:
                if day == 0:
                    self.month_layout.add_widget(Label(text=''))
                else:
                    day_btn = Button(text=str(day))
                    day_btn.bind(on_press=self.select_day)
                    self.month_layout.add_widget(day_btn)

    def update_day_view(self):
        self.day_layout.clear_widgets()
        # Connect to the database
        conn = viewsqlite.create_connection('mydatabase.db')
        if conn is not None:
            # Fetch transactions for the selected date
            search_date = self.date.strftime('%Y-%m-%d')  # Format date as string
            transactions = viewsqlite.select_transactions_by_date(conn, search_date)
            conn.close()  # Close the database connection

            if transactions:
                # Display each transaction in the day view
                for transaction in transactions:
                    transaction_label = Label(text=f"Category: {transaction[1]}, Account: {transaction[2]}, "
                                                f"Amount: {transaction[3]}, Type: {transaction[4]}, Date: {transaction[5]}")
                    self.day_layout.add_widget(transaction_label)
            else:
                # If no transactions, display a message
                self.day_layout.add_widget(Label(text="No transactions for this day."))
        else:
            # If the database connection failed
            self.day_layout.add_widget(Label(text="Failed to connect to the database."))


    def select_day(self, instance):
        self.view_mode = 'day'
        self.date = self.date.replace(day=int(instance.text))
        self.update_view()

    def prev(self, instance):
        if self.view_mode == 'month':
            self.date = self.date.replace(day=1) - datetime.timedelta(days=1)
        else:
            self.date -= datetime.timedelta(days=1)
        self.update_view()

    def next(self, instance):
        if self.view_mode == 'month':
            day = self.date.replace(day=28) + datetime.timedelta(days=4)  # Ensuring we get into the next month
            self.date = day + datetime.timedelta(days=day.day)  # Reset to the first day of the next month
        else:
            self.date += datetime.timedelta(days=1)  # Next day for day view
        self.update_view()

    def toggle_view(self, instance):
        self.view_mode = 'day' if self.view_mode == 'month' else 'month'
        self.update_view()
        print(self.get_values())


class MyApp(App):
    def build(self):
        advanced_calendar = AdvancedCalendar()
        return advanced_calendar

if __name__ == '__main__':
    MyApp().run()
