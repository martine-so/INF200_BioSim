import textwrap
from herbivores_class import Herbivore
from carnivores_class import Carnivore
from island_class import Island
from lowland_class import Lowland
import random
import matplotlib.pyplot as plt

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
for seed in range(100,150):
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

plt.show()