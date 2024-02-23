from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.garden.graph import Graph, MeshLinePlot
from datetime import datetime, timedelta
import random

class TransactionGraph(BoxLayout):
    def __init__(self, **kwargs):
        super(TransactionGraph, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 5

        # Initialize Graph widget with enhanced aesthetics
        self.graph = Graph(xlabel='Day', ylabel='Amount ($)', x_ticks_minor=5,
                           x_ticks_major=10, y_ticks_major=50, y_grid_label=True,
                           x_grid_label=True, padding=5, x_grid=True, y_grid=True,
                           xmin=0, xmax=30, ymin=0, ymax=100, background_color=[0, 0, 0, 1])

        # Button to regenerate the graph data
        self.regenerate_btn = Button(text='Regenerate Data', size_hint=(1, 0.1))
        self.regenerate_btn.bind(on_press=self.regenerate_data)
        self.add_widget(self.regenerate_btn)
        self.add_widget(self.graph)

        self.plot = MeshLinePlot(color=[1, 0, 0, 1])  # Initial plot
        self.graph.add_plot(self.plot)
        self.regenerate_data()

    def regenerate_data(self, *args):
        # Generate example transaction data
        transactions = [
            (i, 'Category', 'Account', random.uniform(10, 500), (self.random_date(datetime(2020, 1, 1), datetime(2020, 1, 30))).strftime('%Y-%m-%d'))
            for i in range(10)
        ]
        self.plot_transactions(transactions)

    def plot_transactions(self, transactions):
        # Prepare and set the plot data
        base_date = datetime(2020, 1, 1)
        plot_points = [(i, t[3]) for i, t in enumerate(transactions)]
        self.plot.points = plot_points
        # Dynamically adjust graph bounds
        self.graph.xmax = len(transactions)
        self.graph.ymax = max(t[3] for t in transactions) + 10

    @staticmethod
    def random_date(start, end):
        time_between_dates = end - start
        random_number_of_days = random.randrange(time_between_dates.days)
        return start + timedelta(days=random_number_of_days)

class MyApp(App):
    def build(self):
        return TransactionGraph()

if __name__ == '__main__':
    MyApp().run()
