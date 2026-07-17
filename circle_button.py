"""Circular button widget used by the app shell (main.py imports CircleBtn).

The source file was missing from the repo (only a stale .pyc remained), which
meant `from circle_button import CircleBtn` in main.py failed and the app could
not start. This restores it: a round Button that draws itself as an ellipse and
hit-tests within its radius, plus a small container widget.
"""
from math import sqrt

from kivy.app import App
from kivy.graphics import Color, Ellipse
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button


class CircleButton(Button):
    """A Button rendered as a filled circle, with a circular touch area."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Hide the default rectangular button background; draw our own circle.
        self.background_color = (0, 0, 0, 0)
        self.size_hint = (None, None)
        self.size = (100, 100)
        with self.canvas.before:
            Color(1, 0, 0, 1)
            self.circle = Ellipse(pos=self.pos, size=self.size)
        self.bind(pos=self.update_canvas, size=self.update_canvas)

    def update_canvas(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(1, 0, 0, 1)
            Ellipse(pos=self.pos, size=self.size)

    def on_touch_down(self, touch):
        cx, cy = self.center_x, self.center_y
        radius = self.width / 2
        if sqrt((touch.x - cx) ** 2 + (touch.y - cy) ** 2) <= radius:
            return super().on_touch_down(touch)
        return False


class CircleBtn(BoxLayout):
    """Vertical container holding a CircleButton wired to a press handler."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.padding = 10
        self.spacing = 10
        btn = CircleButton(text="Click")
        self.add_widget(btn)
        btn.bind(on_press=self.on_button_press)

    def on_button_press(self, instance):
        print("The button was pressed!")


class MyApp(App):
    def build(self):
        return CircleBtn()


if __name__ == "__main__":
    MyApp().run()
