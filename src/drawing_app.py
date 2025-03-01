from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Color, Line
import numpy as np

class DrawingWidget(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.lines = []
        self.current_line = None
        self.all_points_x = []
        self.all_points_y = []

    def on_touch_down(self, touch):
        with self.canvas:
            Color(1, 1, 1)  # Black color
            self.current_line = Line(points=(touch.x, touch.y), width=2)
            self.lines.append(self.current_line)
            self.all_points_x.append(touch.x)
            self.all_points_y.append(touch.y)

    def on_touch_move(self, touch):
        if self.current_line:
            self.current_line.points += [touch.x, touch.y]
            self.all_points_x.append(touch.x)
            self.all_points_y.append(touch.y)

    def on_touch_up(self, touch):
        self.current_line = None
        self.analyze_drawing()

    def analyze_drawing(self):
        if not self.all_points_x:
            return

        x_coords = np.array(self.all_points_x)
        y_coords = np.array(self.all_points_y)

        # Calculate total length
        distances = np.sqrt(np.diff(x_coords)**2 + np.diff(y_coords)**2)
        total_length = np.sum(distances)
        print(f"Total drawing length: {total_length:.2f} pixels")

        # Calculate center point
        avg_x = np.mean(x_coords)
        avg_y = np.mean(y_coords)
        print(f"Center point: ({avg_x:.2f}, {avg_y:.2f})")

        # Clear for next drawing
        self.all_points_x = []
        self.all_points_y = []

class DrawingApp(App):
    def build(self):
        return DrawingWidget()

if __name__ == '__main__':
    DrawingApp().run()