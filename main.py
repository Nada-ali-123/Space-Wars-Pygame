from kivy.app import App
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.core.window import Window


Builder.load_file('layout.kv')

Window.size = (600, 500)
class MyLayout(Widget):
    def selected(self, filename):
        try:
            self.ids.my_img.source = filename[0]

        except FileNotFoundError:
            pass


class ViewerApp(App):
    def build(self):
        return MyLayout()

if __name__ == '__main__':
    ViewerApp().run()