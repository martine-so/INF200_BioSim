from Herbivores import Herbivore
from operator import attrgetter


class Lowland:

    def __init__(self, f_max, animals):
        self.fodder = f_max
        self.animals = animals

    def eating(self, F, beta, phi_age, phi_weight, a_half, w_half):
        self.animals.sort(key=attrgetter('fitness'), reverse=True)
        for animal in self.animals:
            if F < self.fodder:
                f = F
            else:
                f = self.fodder

            animal.update_weight(f, beta)
            self.fodder -= f
            animal.calculate_fitness(phi_age, phi_weight, a_half, w_half)

    def aging(self):
        for animal in self.animals:
            animal.update_a()

    def dying(self, omega):
        for animal in self.animals:
            animal.death(omega)
            if animal.alive is not True:
                self.animals.remove(animal)

    def breeding(self, zeta, w_birth, sigma_birth, xi, gamma):
        for animal in self.animals:
            animal.breeding(zeta, w_birth, sigma_birth, xi, gamma, len(self.animals))
            if animal.baby is True:
                self.animals.append(Herbivore(w=w_birth))

    def loose_weight(self, eta):
        for animal in self.animals:
            animal.loose_weight(eta)
