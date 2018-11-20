from pathlib import Path
import time
import storygenerator

from kivy.app import App
from kivy.lang import Builder
from kivy.properties import StringProperty

from kivy.uix.popup import Popup

from kivy.uix.screenmanager import ScreenManager, Screen

DATA_FOLDER = Path("img/")

def file_to_open(nom_image):
    path_to_image = DATA_FOLDER / "{}.jpg".format(nom_image)
    return str(path_to_image)

class BeginStoryPopUp(Popup):
    beginning = StringProperty()
    def __init__(self, **kwargs):
        super(BeginStoryPopUp, self).__init__(**kwargs)
        self.beginning = new_story.begininning

class StoryScreenPopup(Popup):
    contents = StringProperty()
    img_hero = StringProperty()
    img_villain = StringProperty()
    img_vs = StringProperty()
    nom_hero = StringProperty()
    nom_villain = StringProperty()
    nom_ville = StringProperty()

    def __init__(self, **kwargs):
        super(StoryScreenPopup, self).__init__(**kwargs)
        with open("story_content.txt") as f:
            self.contents = f.read()
            self.nom_hero = new_story.hero
            self.nom_villain = new_story.villain
            self.nom_ville = new_story.ville
            self.img_hero = file_to_open(new_story.hero)
            self.img_villain = file_to_open(new_story.villain)
            self.img_vs = file_to_open("vs")

    def open_begin_story_popup(self):
        the_popup = BeginStoryPopUp()
        the_popup.open()

class WelcomeScreen(Screen):
    img_src = "avengers.jpg"

    def random_hero(self):
        new_story.random_hero()
        new_story.store_info()

class ScrollingScreen(Screen):
    img_src = StringProperty(None)
    img_villain = StringProperty(None)

    def random_hero(self):
        new_story.random_hero()
        new_story.store_info()

class MyScreenManager(ScreenManager):

    def new_hero(self):
        new_story.increase_scroller()
        scroller = new_story.scroller % len(new_story.all_heroes)
        img_src = file_to_open(new_story.all_heroes[scroller])
        img_villain = file_to_open(new_story.all_villains[scroller])
        name = str(time.time())  # getting unique name
        s = ScrollingScreen(name=name)  # getting random colours and same alpha
        self.add_widget(s)
        self.current = name
        s.img_src = img_src
        s.img_villain = img_villain
        new_story.new_hero(new_story.all_heroes[scroller])
        new_story.store_info()

    def open_story_screen_popup(self):
        the_popup = StoryScreenPopup()
        the_popup.open()


root_widget = Builder.load_string('''
MyScreenManager:
    WelcomeScreen:
    
<BeginStoryPopUp>:
    title: "Debut:"
    BoxLayout:
        orientation: 'vertical'
        Label:
            text: "Debut de l'histoire..."
            font_size: 30
        ScrollView:
            size_hint: 1, 1
            TextInput:
                font_size:20
                height: self.minimum_height
                color: 1,1,1,.5
                size_hint_y: None
                readonly: True
                text: root.beginning
        Button:
            text: "Fermer"
            on_press: root.dismiss()
            font_size: 30

<StoryScreenPopUp>:
    title: "Votre Histoire de la Journee:"
    BoxLayout:
        orientation: 'vertical'
        BoxLayout:
            orientation: 'horizontal'
            Label:
                text: root.nom_hero
                font_size: 20
            Label:
                font_size: 20
            Label:
                text: root.nom_villain
                font_size: 20
        BoxLayout:
            orientation: 'horizontal'
            Image:
                source: root.img_hero
                allow_stretch: False
                keep_ratio: True
            Image:
                source: root.img_vs
                allow_stretch: False
                keep_ratio: True                
            Image:
                source: root.img_villain
                allow_stretch: False
                keep_ratio: True          
        Label:
            text: "L'histoire se passe a "+root.nom_ville
            font_size: 30
        Label:
            text: "Et il y aura: "
            font_size: 30
        Label:
            text: root.contents
            font_size: 20
            
        Button:
            text: "Commencer l'histoire"
            on_press: root.open_begin_story_popup()
            font_size: 30
        Button:
            text: "Fermer"
            on_press: root.dismiss()

        
<WelcomeScreen>:
    name: 'welcome'
    BoxLayout:
        orientation: 'vertical'
        Label:
            text: "Generateur d'Histoire!"
            font_size: 30
        Image:
            source: root.img_src
            allow_stretch: False
            keep_ratio: True
        BoxLayout:
            Button:
                text: 'Choisir un Hero au Hasard'
                font_size: 30
                on_press: root.random_hero()
                on_release: app.root.open_story_screen_popup()
            Button:
                text: 'Choisir Mon Hero'
                font_size: 30
                on_release: app.root.new_hero()

<ScrollingScreen>:
    BoxLayout:
        orientation: 'vertical'
        BoxLayout:
            orientation: 'horizontal'
            Label:
                text: "Hero"
                font_size: 30
            Label:
                text: "Ennemi"
                font_size: 30
        BoxLayout:
            orientation: 'horizontal'
            Image:
                source: root.img_src
                allow_stretch: False
                keep_ratio: True
            Image:
                source: root.img_villain
                allow_stretch: False
                keep_ratio: True
        BoxLayout:
            Button:
                size_hint: (.5, .5)
                text: 'OUI'
                font_size: 30
                on_release: app.root.open_story_screen_popup()
            Button:
                size_hint: (.5, .5)
                text: 'NON'
                font_size: 30
                on_release: app.root.new_hero()
            Button:
                size_hint: (.5, .5)
                text: 'Au Hasard'
                font_size: 30
                on_press: root.random_hero()
                on_release: app.root.open_story_screen_popup()

''')


class ScreenManagerApp(App):

    def build(self):
        return root_widget


if __name__ == '__main__':
    new_story = storygenerator.Storygenerator("villes.txt","heroes_and_villains.txt", "events.txt", "debuts.txt")
    ScreenManagerApp().run()
