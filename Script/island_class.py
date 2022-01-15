from lowland_class import Lowland
from highland_class import Highland
from desert_class import Desert
import random
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


        #for i in self.animals_loc:
        #    print(len(self.animals_loc[i].herb), len(self.animals_loc[i].carn))
        #print(' ')

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

    def matrix(self):
        herb_dict = {}
        carn_dict = {}
        for i in range(len(self.island_map)):
            for j in range(len(self.island_map[0])):
                loc = (i+1, j+1)
                herb_dict[loc] = 0
                carn_dict[loc] = 0


        for coord in self.animals_loc:
            herb_dict[coord] = len(self.animals_loc[coord].herb)
            carn_dict[coord] = len(self.animals_loc[coord].carn)

        temp_x = max([cord[0] for cord in herb_dict.keys()])
        temp_y = max([cord[1] for cord in herb_dict.keys()])
        herb_matrix = [[0] * (temp_y) for ele in range(temp_x)]
        carn_matrix = [[0] * (temp_y) for ele in range(temp_x)]

        for (i, j), val in herb_dict.items():
            herb_matrix[i-1][j-1] = val

        for (i, j), val in carn_dict.items():
            carn_matrix[i-1][j-1] = val

        return herb_matrix, carn_matrix

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

random.seed(100)
geogr = textwrap.dedent(geogr)
island = Island(geogr)
island.place_animals(ini_herbs)
island.one_year()
island.place_animals(ini_carns)
island.one_year()
island.matrix()
# for year in range(10):
#     island.one_year()