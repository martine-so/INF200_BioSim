from Herbivores import Herbivore
from Carnivores import Carnivore
from operator import attrgetter
import random


class Lowland:
    """Lowland"""

    # parameters defined at class level
    f_max = 800

    default_params = {'f_max': f_max}

    @classmethod
    def set_params(cls, new_params):
        """Set class parameters
        """

        for key in new_params:
            if key not in 'f_max':
                raise KeyError('Invalid parameter name: ' + key)

        for key in new_params:
            if not 0 <= new_params[key]:
                raise ValueError('All parameter values must be positive')
            cls.key = new_params[key]

    @classmethod
    def get_params(cls):
        """Get class parameters"""
        return {'f_max': cls.f_max}

    def __init__(self, herb, carn):
        self.f_max = 800

        self.DeltaPhiMax = 10 # Carnivore

        self.fodder = self.f_max
        self.herb = herb
        self.carn = carn


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

    def eating_carnivores(self):
        probability = 0
        random.shuffle(self.carn)
        self.herb.sort(key=attrgetter('fitness'))
        for carn in self.carn:
            eaten_weight = 0
            for herb in self.herb:
                if eaten_weight < carn.F:
                    if 0 < carn.fitness - herb.fitness < self.DeltaPhiMax:
                        probability = (carn.fitness - herb.fitness)/self.DeltaPhiMax
                    elif carn.fitness > herb.fitness:
                        probability = 1

                    if probability > random.random():
                        f = herb.w
                        eaten_weight += herb.w
                        if eaten_weight > carn.F:
                            eaten_weight -= herb.w
                            f = carn.F - eaten_weight
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

        if len(self.carn) != 0:
            newborns_carn = []
            for carn in self.carn:
                newborn = carn.breeding(len(self.carn))
                if newborn is not None:
                    newborns_carn.append(newborn)
                    carn.calculate_fitness()
            self.carn.extend(newborns_carn)

    def aging_and_loosing_weight(self):
        for herb in self.herb:
            herb.update_a_and_w()
            herb.calculate_fitness()

        if len(self.carn) != 0:
            for carn in self.carn:
                carn.update_a_and_w()
                carn.calculate_fitness()

    def dying(self):
        self.herb = [herb for herb in self.herb if not herb.death()]

        if len(self.carn) != 0:
            self.carn = [carn for carn in self.carn if not carn.death()]
