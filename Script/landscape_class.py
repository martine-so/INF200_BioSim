from operator import attrgetter
from herbivores_class import Herbivore
from carnivores_class import Carnivore
import random


class Landscape:
    """Landscape"""

    default_params = None

    @classmethod
    def set_params(cls, new_params):
        """Set class parameters
        """

        for key in new_params:
            if key not in ('f_max', 'DeltaPhiMax'):
                raise KeyError('Invalid parameter name: ' + key)

            if key == 'f_max':
                if not 0 <= new_params['f_max']:
                    raise ValueError('f_max values must be positive')

            if key == 'DeltaPhiMax':
                if not 0 < new_params['DeltaPhiMax']:
                    raise ValueError('DeltaPhiMax must be higher than 0')
            cls.key = new_params[key]

    @classmethod
    def get_params(cls):
        """Get class parameters"""
        return {'f_max': cls.f_max}

    def __init__(self):

        self.DeltaPhiMax = 10  # Carnivore

        self.herb = []
        self.carn = []

    def add_animals(self, pop):
        self.herb.extend([Herbivore(i['age'], i['weight']) for i in pop if i['species'] == 'Herbivore'])
        self.carn.extend([Carnivore(i['age'], i['weight']) for i in pop if i['species'] == 'Carnivore'])

    def reset_fodder_and_moved(self):
        self.fodder = self.f_max

        for herb in self.herb:
            herb.moved = False

        for carn in self.carn:
            carn.moved = False

    def eating_herbivores(self):
        self.herb.sort(key=attrgetter('fitness'), reverse=True)
        for herb in self.herb:
            if herb.F < self.fodder:
                f = herb.F
            else:
                f = self.fodder

            herb.update_weight(f)
            self.fodder -= f
            herb.calculate_fitness()

    def prob_carn_eating(self, carn, herb):
        probability = 0
        if 0 < carn.fitness - herb.fitness < self.DeltaPhiMax:
            probability = (carn.fitness - herb.fitness) / self.DeltaPhiMax
        elif carn.fitness > herb.fitness:
            probability = 1
        return probability

    def eating_carnivores(self):
        random.shuffle(self.carn)
        self.herb.sort(key=attrgetter('fitness'))
        for carn in self.carn:
            eaten_weight = 0
            for herb in self.herb:
                if eaten_weight < carn.F:
                    probability = self.prob_carn_eating(carn, herb)

                    if probability > random.random():
                        f = herb.w
                        eaten_weight += herb.w
                        if eaten_weight > carn.F:
                            f = carn.F - (eaten_weight - herb.w)
                            eaten_weight = carn.F
                        carn.update_weight(f)
                        carn.calculate_fitness()
                        herb.dead = True

            self.herb = [herb for herb in self.herb if not herb.dead]

    def breeding(self):
        newborns_herb = []
        for herb in self.herb:
            newborn = herb.breeding(len(self.herb))
            if newborn is not None:
                newborns_herb.append(newborn)
                herb.calculate_fitness()
        self.herb.extend(newborns_herb)

        newborns_carn = []
        for carn in self.carn:
            newborn = carn.breeding(len(self.carn))
            if newborn is not None:
                newborns_carn.append(newborn)
                carn.calculate_fitness()
        self.carn.extend(newborns_carn)

    def migrating_animal(self, loc, dict_with_land_locs):
        x, y = loc
        spaces_around = [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]

        removedHerbs = []
        for herb in self.herb:
            if herb.migrating() is True:
                newloc = random.choice(spaces_around)
                if newloc in dict_with_land_locs:
                    herb.moved = True
                    dict_with_land_locs[newloc].herb.append(herb)
                    removedHerbs.append(herb)
        dict_with_land_locs[loc].herb = [herb for herb in self.herb if herb not in removedHerbs]

        removedCarns = []
        for carn in self.carn:
            if carn.migrating() is True:
                newloc = random.choice(spaces_around)
                if newloc in dict_with_land_locs:
                    carn.moved = True
                    dict_with_land_locs[newloc].carn.append(carn)
                    removedCarns.append(carn)
        dict_with_land_locs[loc].carn = [carn for carn in self.carn if carn not in removedCarns]
        return dict_with_land_locs


    def aging_and_loosing_weight(self):
        for herb in self.herb:
            herb.update_a_and_w()
            herb.calculate_fitness()

        for carn in self.carn:
            carn.update_a_and_w()
            carn.calculate_fitness()

    def dying(self):
        self.herb = [herb for herb in self.herb if not herb.death()]
        self.carn = [carn for carn in self.carn if not carn.death()]
