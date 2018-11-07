import json
import random



VILLAINS = {"Capitaine America": "Red Skull", "Ironman":"Mandarin",
    "Thor":"Thanos","Spiderman":"Le Lezard","Doctor Strange":"Karcilius",
    "Hulk":"Hulk-Rouge", "Vision":"Ultron",
    "Black Panther":"Mechant Black Panther", "Luke":"Darth Vador",
    "Optimus Primus":"Megatron","Lloyd":"Garmadon","Kilo Ren":"Rey"}


def choix_utilisateur(entrees):
        valid = False
        while not valid:
            try:
                print("Faites votre choix:")
                for i in range(len(entrees)):
                    print(i+1,": ", entrees[i])
                entree_demandee = int(input())
                assert entree_demandee in range(1,len(entrees)+1)
                valid = True
                return entree_demandee
            except ValueError:
                print("\nErreur, entrer un chiffre!\n")
            except AssertionError:
                print("\nErreur, cette valeur n'est pas dans les choix\n")


def choix_quantite(texte, max):
        valid = False
        while not valid:
            try:
                print(texte)
                entree_demandee = int(input())
                assert entree_demandee in range(1, max+1)
                valid = True
                return entree_demandee
            except ValueError:
                print("\nErreur, entrer un chiffre!\n")
            except AssertionError:
                print("\nErreur, cette valeur est impossible!\n")

def choix_hero():
    tous_heros = list(VILLAINS.keys())
    return tous_heros[choix_utilisateur(tous_heros)-1]

def shuffle_and_get(list, num):
    liste_melangee = random.shuffle(list)
    return list[:num]

if __name__ == '__main__':
    with open('evenements.txt', 'r') as f:
        evenements = f.read().splitlines()
        f.close()
    type = choix_utilisateur(["Choisir mon hero", "Choix de hero au hasard"])
    if type == 1:
        hero = choix_hero()
    else:
        choix = random.randint(0,len(VILLAINS)-1)
        hero = list(VILLAINS.keys())[choix]
    villain = VILLAINS[hero]
    nb_evenements = choix_quantite("Combien d'evenements voulez-vous?", len(evenements))
#    liste_melangee = random.shuffle(evenements)
#    print(evenements[:nb_evenements])
    evenements_histoire = shuffle_and_get(evenements, nb_evenements)
    print("******************************************")
    print("             NOUVELLE HISTOIRE")
    print("******************************************\n\n")
    print("\nLes Evenements de l'histoire seront: \n")
    for eve in evenements_histoire:
        print(eve)
    print("\nVotre hero sera: ", hero)
    print("\nLe villain de l'histoire sera: ", villain)
    with open("villes.txt", "r") as f:
        villes = f.read().splitlines()
        f.close()
    ville =  shuffle_and_get(villes,1)
    print("\nVotre ville sera: ",ville[0])
