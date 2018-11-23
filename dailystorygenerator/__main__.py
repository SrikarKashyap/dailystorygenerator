#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import storygenerator
import kivy
from pathlib import Path

kivy.require("1.9.0")
from kivy.app import App
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.floatlayout import FloatLayout

DATA_FOLDER = Path("img/")
DEFAULT = "AVENGERS/"

FICHIER_VILLE = "villes.txt"
FICHIER_HEROES = "heroes_and_villains.txt"
FICHIER_EVENTS = "events.txt"
FICHIER_DEBUTS = "debuts.txt"
DEFAULT_STORING_FILE = "story_content.txt"
CONFIG_FILE = "config.txt"

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
        with open(DEFAULT_STORING_FILE, "r") as f:
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


class IntroScreen(Screen):

    def assign_choice(self, choice):
        new_story.load(choice+"/"+FICHIER_VILLE, choice+"/"+FICHIER_HEROES, choice+"/"+FICHIER_EVENTS,
                       choice+"/"+FICHIER_DEBUTS, choice)

    def spinner_clicked(self, value):
        self.assign_choice(value)
        with open(CONFIG_FILE, "w") as f:
            f.write(value)

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
        img_hero = file_to_open(new_story.all_heroes[scroller])
        img_villain = file_to_open(new_story.all_villains[scroller])
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
    new_story = storygenerator.Storygenerator(DEFAULT+FICHIER_VILLE, DEFAULT+FICHIER_HEROES,
                                              DEFAULT+FICHIER_EVENTS, DEFAULT+FICHIER_DEBUTS)
    StoryGeneratorApp().run()