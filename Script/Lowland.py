from Herbivores import Herbivore

class Lowland:

    def __init__(self, f_max, animals):
        self.fodder = f_max
        self.animals = animals

    def eating(self, F, beta):
        for animal in self.animals:
            if F < self.fodder:
                f = F
            else:
                f = self.fodder

            animal.update_weight(f, beta)
            self.fodder -= f

    def aging(self):
        for animal in self.animals:
            animal.update_a()


    def dying(self, omega):
        for animal in self.animals:
            animal.death(omega)
            if animal.alive == False:
                self.animals.remove(animal)



