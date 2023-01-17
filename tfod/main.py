from kivy.app import App
from kivy.properties import ObjectProperty
from kivy.lang.builder import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from Tensorflow.models.research import prediction
global file_name
from constants import *


class MenuScreen(Screen):
    pass


class ChooseScreen(Screen):
    text_1 = ObjectProperty(None)

    def submit(self):
        global file_name
        file_name = self.text_1.text


class Glossary(Screen):
    text = "\n\n\n\n".join(glossary_text.values())


class ClickScreen(Screen):
    def update(self):
        global file_name
        """
        Place for your function here
        file_name - file with photo for detection
        mold_type - type of mold that is detected
        """
        mold_type = prediction.get_by_custom_picture(picture_name=file_name)

        self.ids.image.source = f"download.jpg"
        if mold_type is None:
            text = "Sorry, we couldn't identify any mold on this photo :("
            self.ids.image.source = f"{file_name}"
        else:
            text = f"Your recognized type of mold is:{mold_type}\n\n\n {glossary_text[mold_type]}"
        self.ids.text_input.text = text

    def back(self):
        global file_name
        self.ids.image.source = f"loading.gif"
        self.ids.text_input.text = "Processing..."
        file_name = "test_pictures\\access.jpg"


class CameraClick(Screen):
    def capture(self):
        global file_name
        file_name = "access.jpg"
        camera = self.ids['camera']
        camera.export_to_png(f"test_pictures\\{file_name}")


# Create the screen manager
Builder.load_file(screen)


class DemoApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MenuScreen(name="menu"))
        sm.add_widget(CameraClick(name="camera"))
        sm.add_widget(Glossary(name="Glossary"))
        sm.add_widget(ClickScreen(name="ClickScreen"))
        sm.add_widget(ChooseScreen(name="Screen"))
        return sm


DemoApp().run()
