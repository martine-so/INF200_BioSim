from lowland_class import Lowland
from highland_class import Highland
from desert_class import Desert


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
                    self.migrated_animals[loc] = []

    def place_animals(self, pop):
        for i in pop:
            if i['loc'] not in self.animals_loc:
                raise ValueError('Coordinates must be on island')
            else:
                self.animals_loc[i['loc']].add_animals(i['pop'])


    def specified_loc(self, loc):
        pass

    def migrating(self):
        # coordinates = [i['loc'] for i in self.ini_pop]
        #
        # for i in coordinates:
        #     x, y = i
        # location = self.island_map.split()[x - 1][y - 1]
        # land_types = {'L': Lowland}
        # if location in land_types:
        #     self.land_type = land_types[location]
        pass


# geogr = """\
#            WWW
#            WLW
#            WWW"""
#
# ini_herbs = [{'loc': (2, 2),
#               'pop': [{'species': 'Herbivore',
#                        'age': 5,
#                        'weight': 20}
#                       for _ in range(50)]}]
#
# geogr = textwrap.dedent(geogr)
# island = Island(geogr)
# island.place_ini_animals()