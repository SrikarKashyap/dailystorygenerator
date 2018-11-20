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

    def __init__(self, villes_file, heroes_file, events_file, debuts_file):
        self.scroller = 0
        self.hero = None
        self.villain = None
        with open(villes_file, "r") as f:
            villes = f.read().splitlines()
        self.ville = shuffle_and_get(villes, 1)[0]
        self.all_heroes_and_villains = from_file_to_dict(heroes_file)
        self.all_beginnings = from_file_to_dict(debuts_file)
        self.begininning = self.all_beginnings[self.ville]
        self.all_heroes = list(self.all_heroes_and_villains.keys())
        self.all_villains = list(self.all_heroes_and_villains.values())
        with open(events_file, "r") as f:
            events = f.read().splitlines()
        self.events = shuffle_and_get(events, 3)
        self.store_info()

    def random_hero(self):
        choix = random.randint(0, len(self.all_heroes_and_villains) - 1)
        self.hero = list(self.all_heroes_and_villains.keys())[choix]
        self.villain = self.all_heroes_and_villains[self.hero]
        self.store_info()

    def new_hero(self, choice):
        self.hero = choice
        self.villain = self.all_heroes_and_villains[self.hero]
        self.store_info()

    def increase_scroller(self):
        self.scroller += 1

    def changer_jour(self, jour):
        self.jour = jour

    def store_info(self):
        with open("story_content.txt", "w") as f:
#            f.write("Hero: {}\nVillain: {}\nVille: {}".format(self.hero, self.villain, self.ville))
#            f.write(self.ville+"\n\n")
#            f.write("\nEvenements: \n")
            for i in range(len(self.events)-1):
                f.write(self.events[i]+", ")
            f.write(self.events[len(self.events)-1])

    def __str__(self):
        return "Hero: {}\nVillain: {}\nVille: {}\nEvenements: {}".format(self.hero,
                                                                  self.villain,
                                                                  self.ville,
                                                                  self.events)

    def __repr__(self):
        return str(self)

