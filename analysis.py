from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.graphics import Color, Line, Ellipse
from math import pi, sin, cos

# KV language Builder string
kv = '''
<PieChartWidget>:
    canvas.before:
        Color:
            rgba: 0.98, 0.98, 0.98, 1
        Rectangle:
            pos: self.pos
            size: self.size

BoxLayout:
    orientation: 'vertical'
    BoxLayout:
        size_hint_y: None
        height: '48dp'
        Button:
            text: 'Previous Month'
        Label:
            text: 'January, 2024'
        Button:
            text: 'Next Month'
    BoxLayout:
        PieChartWidget:
            id: pie_chart
            size_hint: None, None
            size: min(self.width, self.height), min(self.width, self.height)
            pos_hint: {'center_x': 0.5, 'center_y': 0.5}
    BoxLayout:
        size_hint_y: None
        height: '48dp'
        Button:
            text: 'Add Expense'
'''

class PieChartWidget(Widget):
    def __init__(self, **kwargs):
        super(PieChartWidget, self).__init__(**kwargs)
        self.expenses = {'Beauty': 58.00, 'Baby': 52.00}
        self.pie_slices = []

    def calculate_slices(self):
        total = sum(self.expenses.values())
        start_angle = 0
        for category, amount in self.expenses.items():
            angle = (amount / total) * 360
            self.pie_slices.append((category, start_angle, start_angle + angle))
            start_angle += angle

    def on_size(self, *args):
        self.calculate_slices()
        self.draw_pie_chart()

    def draw_pie_chart(self):
        self.canvas.clear()
        with self.canvas:
            # Set the center and radius for the pie chart
            center_x = self.center_x
            center_y = self.center_y
            radius = min(self.width, self.height) / 2

            # Draw the pie slices
            for category, start_angle, end_angle in self.pie_slices:
                Color(*self.get_color_for_category(category))
                start_rad = pi * start_angle / 180
                end_rad = pi * end_angle / 180

                Line(points=[center_x, center_y,
                             center_x + radius * cos(start_rad), center_y + radius * sin(start_rad)],
                     width=1.5)
                
                Line(circle=(center_x, center_y, radius, start_angle, end_angle), width=1.5)

                Line(points=[center_x, center_y,
                             center_x + radius * cos(end_rad), center_y + radius * sin(end_rad)],
                     width=1.5)

    def get_color_for_category(self, category):
        colors = {
            'Beauty': (1, 0, 0, 1),  # Red
            'Baby': (0, 0, 1, 1),    # Blue
        }
        return colors.get(category, (0, 0, 0, 1))  # Default to black

class PieChartApp(App):
    def build(self):
        return Builder.load_string(kv)

if __name__ == '__main__':
    PieChartApp().run()
