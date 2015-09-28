from kivy.app import App
from kivy.garden.filebrowser import FileBrowser
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty
from kivy.uix.screenmanager import Screen
from kivy.storage.jsonstore import JsonStore
from os.path import sep, expanduser, isdir, dirname

class FileScreen(Screen):

    def on_enter(self):
        user_path = ''
        browser = FileBrowser(select_string="Select", dirselect=True)
        browser.bind(on_success=self.storefilepath,
                    on_canceled=self.canceled)
        self.add_widget(browser)


    def storefilepath(self, instance):
        pathstore = JsonStore("pathstore.json")
        pathstore.put("path", path=instance.selection)
        print instance.selection

    def canceled(self, instance):
        self.manager.current="category_screen"


class CategoryScreen(Screen):

    pass


class DupRoot(BoxLayout):
    imagepath = StringProperty("")


    def __init__(self, **kwargs):
        super(DupRoot, self).__init__(**kwargs)
        # list of previous screens
        self.screen_list = []

    def next_screen(self, neoscreen):

        self.screen_list.append(self.ids.dup_screen_manager.current)
        self.ids.dup_screen_manager.current = neoscreen

    def _fbrowser_success(self, instance):
        print instance.selection


class DupApp(App):

    def build(self):
        return DupRoot()

if __name__ == "__main__":
    DupApp().run()
