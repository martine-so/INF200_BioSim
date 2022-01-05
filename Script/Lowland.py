from Herbivores import Herbivore
from operator import attrgetter


class Lowland:

    def __init__(self, animals, f_max=800):
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

    def breeding(self, zeta, w_birth, sigma_birth, xi, gamma, phi_age, phi_weight, a_half, w_half):
        newborns = []
        for animal in self.animals:
            animal.breeding(zeta, w_birth, sigma_birth, xi, gamma, len(self.animals))
            if animal.baby is True:
                newborns.append(Herbivore(w=w_birth))
                animal.calculate_fitness(phi_age, phi_weight, a_half, w_half)
        self.animals.extend(newborns)

    def aging(self, phi_age, phi_weight, a_half, w_half):
        for animal in self.animals:
            animal.update_a()
            animal.calculate_fitness(phi_age, phi_weight, a_half, w_half)

    def loose_weight(self, eta, phi_age, phi_weight, a_half, w_half):
        for animal in self.animals:
            animal.loose_weight(eta)
            animal.calculate_fitness(phi_age, phi_weight, a_half, w_half)

    def dying(self, omega):
        for animal in self.animals:
            animal.death(omega)
            if animal.alive is not True:
                self.animals.remove(animal)
