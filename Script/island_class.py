from lowland_class import Lowland
from highland_class import Highland
from desert_class import Desert
import textwrap


class Island:

    def __init__(self, island_map):
        self.island_map = island_map.split()
        self.animals_loc = {}
        self.migrated_animals = {}

        landscapes = {'L': Lowland, 'H': Highland, 'D': Desert}
        island_dict = {}

        for i in range(len(self.island_map)):
            for j in range(len(self.island_map[0])):
                loc = (i+1, j+1)
                island_dict[loc] = self.island_map[i][j]
                if self.island_map[i][j] != 'W':
                    self.animals_loc[loc] = landscapes[self.island_map[i][j]]()

    def place_animals(self, pop):
        for i in pop:
            if i['loc'] not in self.animals_loc:
                raise ValueError('Coordinates must be on island')
            else:
                self.animals_loc[i['loc']].add_animals(i['pop'])

    def migrating(self):
        new_animals_loc = self.animals_loc
        for i in self.animals_loc:
            new_animals_loc = new_animals_loc[i].migrating_animal(i, new_animals_loc)

        self.animals_loc = new_animals_loc


        for i in self.animals_loc:
            print(len(self.animals_loc[i].herb), len(self.animals_loc[i].carn))
        print(' ')

    def one_year(self):
        for i in self.animals_loc:
            self.animals_loc[i].reset_fodder_and_moved()
            self.animals_loc[i].eating_herbivores()
            self.animals_loc[i].eating_carnivores()
            self.animals_loc[i].breeding()

        self.migrating()

        for i in self.animals_loc:
            self.animals_loc[i].aging_and_loosing_weight()
            self.animals_loc[i].dying()

geogr = """\
           WWWWW
           WWLWW
           WLLLW
           WWLWW
           WWWWW"""

ini_herbs = [{'loc': (3, 3),
              'pop': [{'species': 'Herbivore',
                       'age': 5,
                       'weight': 20}
                      for _ in range(50)]}]

ini_carns = [{'loc': (2, 3),
              'pop': [{'species': 'Carnivore',
                       'age': 5,
                       'weight': 20}
                      for _ in range(20)]}]

geogr = textwrap.dedent(geogr)
island = Island(geogr)
island.place_animals(ini_herbs)
island.one_year()
island.place_animals(ini_carns)
for year in range(10):
    island.one_year()