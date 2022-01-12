import textwrap
from herbivores_class import Herbivore
from carnivores_class import Carnivore
from island_class import Island
from lowland_class import Lowland
import random
import matplotlib.pyplot as plt

import statistics

geogr = """\
           WWW
           WLW
           WWW"""
geogr = textwrap.dedent(geogr)

ini_herbs = [{'loc': (2, 2),
              'pop': [{'species': 'Herbivore',
                       'age': 5,
                       'weight': 20}
                      for _ in range(50)]}]
ini_carns = [{'loc': (2, 2),
              'pop': [{'species': 'Carnivore',
                       'age': 5,
                       'weight': 20}
                      for _ in range(20)]}]

plt.figure(figsize=(14,8))
total_num_herbs = []
total_num_carns = []
herbs_die = 0
carns_die = 0
for seed in range(100,199):
    random.seed(seed)

    herbs = []
    carns = []

    island = Island(geogr)
    island.place_animals(ini_herbs)
    coordinates = [i['loc'] for i in ini_herbs]

    # coordinates = [i['loc'] for i in ini_herbs]
    #
    # for i in coordinates:
    #     y, x = i
    # location = geogr.split()[y - 1][x - 1]
    # land_types = {'L': Lowland}
    # if location in land_types:
    #     land_type = land_types[location]

    num_herbs = [len(herbs)]
    num_carns = [len(carns)]

    field = island.animals_loc[coordinates[0]]

    for year in range(50):
        field.reset_fodder()
        field.eating_herbivores()
        field.eating_carnivores()
        field.breeding()
        field.aging_and_loosing_weight()
        field.dying()
        herbs = field.herb

        num_herbs.append(len(herbs))
        num_carns.append(len(carns))

    island.place_animals(ini_carns)

    for year in range(50, 300):
        field.reset_fodder()
        field.eating_herbivores()
        field.eating_carnivores()
        field.breeding()
        field.aging_and_loosing_weight()
        field.dying()
        herbs = field.herb
        carns = field.carn

        num_herbs.append(len(herbs))
        num_carns.append(len(carns))

    plt.plot(num_herbs, 'b')
    plt.plot(num_carns, 'r')

    if num_carns[-1] != 0 and num_herbs[-1] != 0:
        total_num_herbs.extend(num_herbs)
        total_num_carns.extend(num_carns)

    if num_carns[-1] == 0:
        carns_die += 1

    if num_herbs[-1] == 0:
        herbs_die += 1

plt.show()
print(statistics.mean(total_num_herbs), statistics.mean(total_num_carns))
# print(herbs_die, carns_die)