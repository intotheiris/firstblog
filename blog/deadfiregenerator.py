from random import randint, choice
from .dicts import *

# Selects gender
gender = choice(gender_list)

# Selects race and subrace
race = choice(list(race_dict.keys()))
subrace = choice(race_dict[race])

# Selects class, used later as first class if multiclass
first_class = choice(list(class_dict.keys()))

# Generates subclass for first class
first_subclass = choice(class_dict[first_class])

# Generates culture
culture = choice(culture_list)

# Adds culture-specific backgrounds to backgrounds available to all cultures and selects one
background_list_full = background_list

if culture == "Aedyr":
    background_list_full.extend(("Aristocrat", "Clergy", "Colonist", "Dissident", "Mercenary", "Slave"))
elif culture == "The Deadfire Archipelago":
    background_list_full.extend(("Aristocrat", "Clergy", "Explorer", "Mercenary", "Raider", "Slave"))
elif culture == "Ixamitl Plains":
    background_list_full.extend(("Aristocrat", "Dissident", "Mercenary", "Philosopher", "Scholar"))
elif culture == "Old Vailia":
    background_list_full.extend(("Aristocrat", "Artist", "Colonist", "Dissident", "Mercenary", "Slave"))
elif culture == "Rauatai":
    background_list_full.extend(("Aristocrat", "Dissident", "Mercenary", "Scholar", "Slave"))
elif culture == "The Living Lands":
    background_list_full.extend(("Colonist", "Explorer", "Mercenary", "Scientist"))
elif culture == "The White That Wends":
    background_list_full.extend(("Aristocrat", "Explorer", "Mystic"))
background = choice(background_list_full)

# Generates second class for multiclass, avoiding duplicate
second_class = choice(list(class_dict.keys()))
while second_class == first_class:
    second_class = choice(list(class_dict.keys()))

# Creates multiclass list so that the multiclass name can be taken from the dictionary
multiclass = [first_class, second_class]
# Sorted alphabetically to match the dictionary so that Python finds the right key
multiclass = sorted(multiclass)

# Gets multiclass name from multiclass dictionary key
for key, value in multiclass_dict.items():
    if multiclass == value:
      multiclass = key

# Subclasses for multiclass. The first is inherited from earlier and is added to a selected subclass for second class
multi_subclass = first_subclass + "/" + choice(class_dict[second_class])

# Randomly picks if singleclass (1) or multiclass (2)
singleormulti = randint(1,2)

def pleasework():
    print("Gender: " + gender)
    print("Race: " + race)
    print("Subrace: " + subrace)
# Output for single class character
    if singleormulti == 1:
      print("Class: " + first_class)
      print("Subclass: " + first_subclass)
      print("Culture: " + culture)
      print("Background: " + background)
# Output for multiclass character
    else:
      print("Class: " + multiclass + " (" + first_class + "/" + second_class + ") ")
      print("Subclass: " + multi_subclass)
      print("Culture: " + culture)
      print("Background: " + background)
