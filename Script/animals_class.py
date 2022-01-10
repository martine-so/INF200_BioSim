import math
import random


class Animals:
    """How animals generally behave"""

    default_params = None

    @classmethod
    def set_params(cls, new_params):
        """Set class parameters
        """

        for key in new_params:
            if key not in ('beta', 'phi_age', 'phi_weight', 'a_half', 'w_half', 'zeta', 'w_birth',
                           'sigma_birth', 'xi', 'gamma', 'eta', 'omega'):
                raise KeyError('Invalid parameter name: ' + key)

            if not 0 <= new_params[key]:
                raise ValueError('All parameter values must be positive')

            if key == 'eta':
                if not new_params['eta'] <= 1:
                    raise ValueError('eta must be in [0, 1].')

            if key == 'DeltaPhiMax':
                if not 0 < new_params['DeltaPhiMax']:
                    raise ValueError('DeltaPhiMax must be higher than 0')
            cls.key = new_params[key]

    @classmethod
    def get_params(cls):
        """ Get classparameters"""
        return {'F': cls.F, 'beta': cls.beta, 'phi_age': cls.phi_age, 'phi_weight': cls.phi_weight,
                'a_half': cls.a_half, 'w_half': cls.w_half, 'zeta': cls.zeta, 'w_birth': cls.w_birth,
                'sigma_birth': cls.sigma_birth, 'xi': cls.xi, 'gamma': cls.gamma, 'eta': cls.eta,
                'omega': cls.omega, 'mu': cls.mu}

    def __init__(self, a=0, w=None):
        """
        :param a: age of an animal. Zero as default value.
        :param w: Weight of an animal.
        """
        self.a = a
        self.fitness = 0
        self.w = w
        self.dead = False

        if w is None:
            self.w = random.gauss(self.w_birth, self.sigma_birth)
        else:
            self.w = w

    def update_weight(self, f):
        """
        Updates an animal's weight

        :param f: amount of food eaten by an animal that year
        """
        self.w += self.beta * f

    def calculate_fitness(self):
        """"calculates an animals fitness as a number between 0 and 1"""
        if self.w <= 0:
            self.fitness = 0

        else:
            self.fitness = (1/(1 + math.exp(self.phi_age * (self.a - self.a_half)))) * \
                           (1/(1 + math.exp(-self.phi_weight * (self.w - self.w_half))))

    def breeding(self, num_of_animals):
        newborn = type(self)()
        if self.w < self.zeta * (self.w_birth + self.sigma_birth) or self.w < self.xi * newborn.w:
            return None

        prob = min(1, self.gamma * self.fitness * (num_of_animals - 1))
        if random.random() < prob:
            self.w -= self.xi * newborn.w
            return newborn

    def update_a_and_w(self):
        """updates the age of an animal with 1 and weight..."""
        self.a += 1
        self.w -= self.eta * self.w

    def death(self):
        """checks if an animal dies that year"""
        prob = self.omega * (1 - self.fitness)
        if random.random() < prob or self.w == 0:
            return True
