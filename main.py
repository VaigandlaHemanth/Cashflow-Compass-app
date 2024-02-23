from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.graphics import Color, RoundedRectangle
from kivy.uix.popup import Popup
from records import RecordScreen
from kivy.core.window import Window
from circle_button import CircleBtn
from advancedcalender import AdvancedCalendar
from budgetapp import BudgetingComponent
from kivy.uix.screenmanager import ScreenManager, Screen

class ImageButton(ButtonBehavior, Image):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(rgba=(0, 0, 0, 0))  # Transparent background

class TopBar(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.size_hint_y = None
        self.height = 60
        self.padding = [10, 5]
        self.spacing = 10

        with self.canvas.before:
            Color(0.086, 0.627, 0.522, 1)  # Teal color
            self.rect = RoundedRectangle(size=self.size, pos=self.pos, radius=[(10, 10)])

        self.bind(size=self.update_background, pos=self.update_background)
        
        self.menu_button = ImageButton(source='menu_icon.png', allow_stretch=True)
        self.menu_button.size_hint = (None, 1)
        self.menu_button.width = 50
        self.menu_button.bind(on_release=self.open_menu)
        self.add_widget(self.menu_button)
        
        self.title = Label(text='My Money', color=(1, 1, 1, 1))
        self.title.font_size = '24sp'
        self.title.bold = True
        self.title.size_hint_x = 2
        self.title.halign = 'left'
        self.title.valign = 'middle'
        self.title.text_size = self.title.size
        self.add_widget(self.title)
        
        self.spacer = Widget()
        self.spacer.size_hint_x = 1
        self.add_widget(self.spacer)
        
        self.search_button = ImageButton(source='search.png', allow_stretch=True)
        self.search_button.size_hint = (None, 1)
        self.search_button.width = 50
        self.search_button.bind(on_release=self.open_search)
        self.add_widget(self.search_button)

    def update_background(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

    def open_menu(self, instance):
        popup = Popup(title='Menu', content=Label(text='Menu Content'), size_hint=(None, None), size=(300, 200))
        popup.open()

    def open_search(self, instance):
        popup = Popup(title='Search', content=Label(text='Search Content'), size_hint=(None, None), size=(300, 200))
        popup.open()

class BottomNavigationBar(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.size_hint_y = None
        self.height = 60

        # Buttons for the navigation bar
        self.records_button = Button(text='Records', background_color=(0.086, 0.627, 0.522, 1))
        self.records_button.bind(on_press=lambda instance: self.button_press('records'))

        self.analysis_button = Button(text='Analysis', background_color=(0.086, 0.627, 0.522, 1))
        self.analysis_button.bind(on_press=lambda instance: self.button_press('analysis'))

        self.budgets_button = Button(text='Budgets', background_color=(0.086, 0.627, 0.522, 1))
        self.budgets_button.bind(on_press=lambda instance: self.button_press('budgets'))

        # Add buttons to the layout
        self.add_widget(self.records_button)
        self.add_widget(self.analysis_button)
        self.add_widget(self.budgets_button)

    def button_press(self, section_name):
        app = App.get_running_app() 
        app.switch_section(section_name)

class MyApp(App):
    def build(self):
        self.main_layout = BoxLayout(orientation='vertical')

        # TopBar and BottomNavigationBar
        self.top_bar = TopBar()
        self.bottom_nav_bar = BottomNavigationBar()

        # Main content area
        self.main_content = BoxLayout()

        # Assemble the layout
        self.main_layout.add_widget(self.top_bar)
        self.main_layout.add_widget(self.main_content)
        self.main_layout.add_widget(self.bottom_nav_bar)

        Window.size = (360, 640)

        return self.main_layout

    def display_results(self, results):
        # Clear existing content
        self.main_content.clear_widgets()
        # Display results in the main content area
        result_label = Label(text=results)
        self.main_content.add_widget(result_label)


    def switch_section(self, section):
        # Clear existing content
        self.main_content.clear_widgets()

        # Update main content based on the section
        if section == 'records':
            record_screen = RecordScreen()
            self.main_content.add_widget(record_screen)
        elif section == 'analysis':
            analysis_screen = AdvancedCalendar()
            self.main_content.add_widget(analysis_screen)
        elif section == 'budgets':
            plan_screen = BudgetingComponent()
            self.main_content.add_widget(plan_screen)
        else:
            self.main_content.add_widget(Label(text=f'{section} Content', font_size='20sp', color=(0, 1, 1, 1)))

if __name__ == '__main__':
    MyApp().run()   
