from kivy.app import App
from kivy.garden.filebrowser import FileBrowser
from kivy.uix.image import AsyncImage as Image
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty
from kivy.uix.screenmanager import Screen
from kivy.storage.jsonstore import JsonStore

import os


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
        self.manager.current="category_screen"

    def canceled(self, instance):
        self.manager.current="category_screen"


class CategoryScreen(Screen):

    imagepath = StringProperty("")

    def on_enter(self):
        pathstore = JsonStore("pathstore.json")
        if pathstore.exists("path"):
            print pathstore["path"]
            self.imagepath = pathstore["path"]["path"][0]
            print self.imagepath
            self.populateCarousel()

    def populateCarousel(self):
        imagenames = []
        directories = []
        fullpaths = []

        for dirpath, dirnames, filenames in os.walk(self.imagepath):
            directories.append(dirpath)
            imagenames.append(filenames)

        print imagenames
        print directories
        iterator = 0
        print imagenames[0]

        for path in directories:
            for imagename in imagenames[iterator]:
                fullpaths.append(path+"/"+imagename)

            iterator += 1

        for images in fullpaths:
            image = Image(source=images, allow_stretch=True)
            self.ids.gallery_carousel.add_widget(image)


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
