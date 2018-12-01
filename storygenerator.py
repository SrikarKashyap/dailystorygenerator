import random

def from_file_to_dict(filename):
    content_as_dict = {}
    with open(filename, "r") as f:
        content = f.read().splitlines()
    for line in content:
        this_line = line.split(":")
        content_as_dict[this_line[0]] = this_line[1]
    return content_as_dict

def shuffle_and_get(a_list, num):
    random.shuffle(a_list)
    return a_list[:num]

class Storygenerator:

    def __init__(self, cities_file, heroes_file, triggers_file, beginnings_file, themes):
        self.storing_file = "story_content.txt"
        self.cities_file, self.heroes_file, self.triggers_file, self.beginnings_file = [cities_file,
                                                                                  heroes_file,
                                                                                  triggers_file,
                                                                                  beginnings_file]
        self.themes = themes
        self.theme = themes[0]
        self.scroller = 0
        with open(self.cities_file, "r") as f:
            cities = f.read().splitlines()
        self.city = shuffle_and_get(cities, 1)[0]
        with open(self.beginnings_file, "r") as f:
            beginnings = f.read().splitlines()
        self.begininning = shuffle_and_get(beginnings, 1)[0]        
        self.all_heroes_and_villains = from_file_to_dict(self.heroes_file)
        self.all_heroes = list(self.all_heroes_and_villains.keys())
        self.all_villains = list(self.all_heroes_and_villains.values())
        with open(self.triggers_file, "r") as f:
            triggers = f.read().splitlines()
        self.triggers = shuffle_and_get(triggers, 3)
        self.store_triggers(self.storing_file)

    def random_hero(self):
        choix = random.randint(0, len(self.all_heroes_and_villains) - 1)
        self.hero = list(self.all_heroes_and_villains.keys())[choix]
        self.villain = self.all_heroes_and_villains[self.hero]
        self.store_triggers(self.storing_file)

    def new_hero(self, choice):
        self.hero = choice
        self.villain = self.all_heroes_and_villains[self.hero]
        self.store_triggers(self.storing_file)

    def increase_scroller(self):
        self.scroller += 1

    def store_triggers(self, store_file):
        with open(store_file, "w") as f:
            for i in range(len(self.triggers)-1):
                f.write(self.triggers[i]+", ")
            f.write(self.triggers[len(self.triggers)-1])

    def add_theme(self,theme_to_add):
        self.themes.append(theme_to_add)

    def change_theme(self,theme_to_change):
        self.theme = theme_to_change


    def __str__(self):
        return "Hero: {}\nVillain: {}\nVille: {}\nEvenements: {}".format(self.hero,
                                                                  self.villain,
                                                                  self.city,
                                                                  self.triggers)
    def __repr__(self):
        return str(self)

