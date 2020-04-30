from kivy.uix.gridlayout import GridLayout
from kivy.properties import ObjectProperty


class MainWindow(GridLayout):
    label = ObjectProperty()
    gridArea = ObjectProperty()
    scrollView = ObjectProperty()
    addbutton = ObjectProperty()

    def __init__(self):
        super().__init__()
        self.label.text = "Персонажи"
        self.gridArea.bind(minimum_height=self.gridArea.setter('height'))


