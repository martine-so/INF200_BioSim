import math
import random


class Herbivore:

    def __init__(self, a=0, w=0, seed=101):
        self.a = a
        self.w = w
        self.fitness = 0
        self.alive = True
        self.baby = False
        random.seed(seed)

    def update_weight(self, f, beta):
        self.w += beta * f

    def calculate_fitness(self, phi_age, phi_weight, a_half, w_half):
        if self.w <= 0:
            self.fitness = 0

        else:
            self.fitness = (1/(1 + math.exp(phi_age * (self.a - a_half)))) * \
                           (1/(1 + math.exp(-phi_weight * (self.w - w_half))))

        return self.fitness

    def breeding(self, zeta, w_birth, sigma_birth, xi, gamma, N):
        if self.w < zeta * (w_birth + sigma_birth):
            probability = 0
        elif self.w < xi * w_birth:  # xi * babys vekt. Vet ikke helt hva babys vekt er?
            probability = 0
        else:
            probability = min(1, gamma * self.fitness * (N - 1))

        if random.random() < probability:
            self.baby = True
            self.w -= xi * w_birth
        else:
            self.baby = False

    def update_a(self):
        self.a += 1

    def loose_weight(self, eta):
        self.w -= eta * self.w

    def death(self, omega):
        if self.w == 0:
            self.alive = False
        else:
            probability = omega * (1 - self.fitness)
            if random.random() < probability:
                self.alive = False
