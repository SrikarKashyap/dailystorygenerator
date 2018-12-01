#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import storygenerator
import kivy
from pathlib import Path

kivy.require("1.9.0")
from kivy.app import App
from kivy.lang import Builder
from kivy.properties import StringProperty, ListProperty
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen


DATA_FOLDER = Path("img/")

THEMES = []
with open("config.txt", "r") as f:
    THEMES += f.read().splitlines()

DEFAULT = THEMES[0]+"/"


CITY_FILE = "cities.txt"
HEROES_FILE = "heroes_and_villains.txt"
TRIGGERS_FILE = "triggers.txt"
BEG_FILE = "beginnings.txt"
DEFAULT_STORING_FILE = "story_content.txt"


def raise_error_popup():
    the_popup = ErrorPopUp()
    the_popup.open()

def create_defaults(directory):
    list_of_files = ["cities.txt", "heroes_and_villains.txt",
                     "triggers.txt", "beginnings.txt"]
    for item in list_of_files:
        with open(directory+"/"+item, "w") as f:
            pass

def image_to_open(name_image):
    path_to_image = DATA_FOLDER / "{}.jpg".format(name_image)
    return str(path_to_image)

def file_to_open(name_image):
    path_to_image = DATA_FOLDER / "{}.jpg".format(name_image)
    return str(path_to_image)

def create_dir(directory):
    Path(directory).mkdir(parents=True, exist_ok=True)


def write_config(filename, line):
    directory = new_story.theme
    with open(directory + "/" + filename, "a+") as f:
        f.write(line)



class ErrorPopUp(Popup):

    def open_config(self):
        the_popup = ConfigPopup()
        the_popup.open()


class CreateThemePopup(Popup):
    new_story = storygenerator.Storygenerator(DEFAULT + CITY_FILE, DEFAULT + HEROES_FILE,
                                              DEFAULT + TRIGGERS_FILE, DEFAULT + BEG_FILE, THEMES)
    custom_theme = StringProperty()

    def __init__(self, **kwargs):
        super(CreateThemePopup, self).__init__(**kwargs)

    def run_config(self):
        self.custom_theme = self.ids.custom_theme.text
        new_story.add_theme(self.custom_theme)
        new_story.theme = self.custom_theme
        create_dir(self.custom_theme)
        create_defaults(self.custom_theme)
        the_popup = ConfigPopup()
        the_popup.open()

class ConfigPopup(Popup):
    name_hero = StringProperty()
    name_villain = StringProperty()

    def __init__(self, **kwargs):
        super(ConfigPopup, self).__init__(**kwargs)
        with open(DEFAULT_STORING_FILE, "r") as f:
            self.name_hero = new_story.hero


    def save_config(self):
        with open("config.txt", "w") as f:
            for item in new_story.themes:
                f.write(item+"\n")

    def write_hero_and_villains(self):
        write_config(HEROES_FILE, "{}:{}\n".format(self.ids.hero_name.text, self.ids.villain_name.text))

    def write_cities(self):
        write_config(CITY_FILE, "{}\n".format(self.ids.city_name.text))

    def write_story_beg(self):
        write_config(BEG_FILE, "{}\n".format(self.ids.story_beginning.text))

    def write_trigger(self):
        write_config(TRIGGERS_FILE, "{}\n".format(self.ids.trigger.text))



class BeginStoryPopUp(Popup):
    beginning = StringProperty()
    trigger = StringProperty()

    def __init__(self, **kwargs):
        super(BeginStoryPopUp, self).__init__(**kwargs)
        self.beginning = new_story.begininning
        self.name_villain = new_story.villain
        self.trigger = new_story.trigger


class StoryScreenPopup(Popup):
    contents = StringProperty()
    img_hero = StringProperty()
    img_villain = StringProperty()
    img_vs = StringProperty()
    name_hero = StringProperty()
    name_villain = StringProperty()
    name_city = StringProperty()

    def __init__(self, **kwargs):
        super(StoryScreenPopup, self).__init__(**kwargs)
        with open(DEFAULT_STORING_FILE, "r") as f:
            self.contents = f.read()
            self.name_hero = new_story.hero
            self.name_villain = new_story.villain
            self.name_city = new_story.city
            self.img_hero = image_to_open(new_story.hero)
            self.img_villain = image_to_open(new_story.villain)
            self.img_vs = image_to_open("vs")


    def open_begin_story_popup(self):
        the_popup = BeginStoryPopUp()
        the_popup.open()


class IntroScreen(Screen):
    themes = ListProperty()

    def __init__(self, **kwargs):
        new_story = storygenerator.Storygenerator(DEFAULT + CITY_FILE, DEFAULT + HEROES_FILE,
                                                  DEFAULT + TRIGGERS_FILE, DEFAULT + BEG_FILE, THEMES)
        super(IntroScreen, self).__init__(**kwargs)
        self.themes = new_story.themes

    def assign_choice(self, choice):

        new_story = storygenerator.Storygenerator(choice+"/"+CITY_FILE,
                                                  choice+"/"+HEROES_FILE,
                                                  choice+"/"+TRIGGERS_FILE,
                                                  choice+"/"+BEG_FILE, THEMES)
        new_story.change_theme(choice)


    def spinner_clicked(self, value):
        if value != "(create a theme)":
            try:
                self.assign_choice(value)
            except:
                raise_error_popup()
        else:
            self.create_theme()

    def create_theme(self):
        the_popup = CreateThemePopup()
        the_popup.open()

class WelcomeScreen(Screen):
    img_bkg = "WELCOME.jpg"

    def random_hero(self):
        new_story.random_hero()


class ScrollingScreen(Screen):
    img_hero = StringProperty(None)
    img_villain = StringProperty(None)

    def random_hero(self):
        new_story.random_hero()


class MyScreenManager(ScreenManager):

    def new_hero(self):
        new_story.increase_scroller()
        scroller = new_story.scroller % len(new_story.all_heroes)
        img_hero = image_to_open(new_story.all_heroes[scroller])
        img_villain = image_to_open(new_story.all_villains[scroller])
        name = str(time.time())  # getting unique name
        s = ScrollingScreen(name=name)
        self.add_widget(s)
        self.current = name
        s.img_hero = img_hero
        s.img_villain = img_villain
        new_story.new_hero(new_story.all_heroes[scroller])

    def open_story_screen_popup(self):
        the_popup = StoryScreenPopup()
        the_popup.open()


buildKV = Builder.load_file("screenmanager.kv")

class StoryGeneratorApp(App):

    def build(self):
        return buildKV


if __name__ == '__main__':
    new_story = storygenerator.Storygenerator(DEFAULT+CITY_FILE, DEFAULT+HEROES_FILE,
                                              DEFAULT+TRIGGERS_FILE, DEFAULT+BEG_FILE, THEMES)
    new_story.random_hero()
    StoryGeneratorApp().run()
