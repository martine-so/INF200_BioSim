from Herbivores import Herbivore
from operator import attrgetter


class Lowland:
    """Lowland"""

    #parameters defined at class level
    f_max=800

    default_params = {'f_max': f_max}

    @classmethod
    def set_params(cls, new_params):
        """Set class parameters
        """

        for key in new_params:
            if key not in ('f_max'):
                raise KeyError('Invalid parameter name: ' + key)

        for key in new_params:
            if not 0 <= new_params[key]:
                raise ValueError('All parametervalues must be positiv')
            cls.key = new_params[key]


    def __init__(self, animals):
        self.f_max = 800

        self.fodder = self.f_max
        self.animals = animals

    def eating(self):
        self.animals.sort(key=attrgetter('fitness'), reverse=True)
        for animal in self.animals:
            if animal.F < self.fodder:
                f = animal.F
            else:
                f = self.fodder

            animal.update_weight(f)
            self.fodder -= f
            animal.calculate_fitness()

    def breeding(self):
        newborns = []
        for animal in self.animals:
            animal.breeding(len(self.animals))
            if animal.baby is True:
                newborns.append(Herbivore(animal.newborn_weight))
                animal.calculate_fitness()
        self.animals.extend(newborns)

    def aging(self):
        for animal in self.animals:
            animal.update_a()
            animal.calculate_fitness()

    def loose_weight(self):
        for animal in self.animals:
            animal.loose_weight()
            animal.calculate_fitness()

    def dying(self):
        for animal in self.animals:
            animal.death()
            # if animal.alive is not True:
            #     self.animals.remove(animal)
        self.animals = [animal for animal in self.animals if animal.alive is True]
