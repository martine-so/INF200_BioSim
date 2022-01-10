import math
import random


class Herbivore:
    """How Herbivores work"""

    # Parameters defined at class level
    F = 10
    beta = 0.9
    phi_age = 0.6
    phi_weight = 0.1
    a_half = 40
    w_half = 10
    zeta = 3.5
    w_birth = 8
    sigma_birth = 1.5
    xi = 1.2
    gamma = 0.2
    eta = 0.05
    omega = 0.4
    mu = 0.25

    default_params = {'F': F, 'beta': beta, 'phi_age': phi_age, 'phi_weight': phi_weight, 'a_half': a_half,
                      'w_half': w_half, 'zeta': zeta, 'w_birth': w_birth, 'sigma_birth': sigma_birth,
                      'xi': xi, 'gamma': gamma, 'eta': eta, 'omega': omega, 'mu': mu}

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
        self.a = a
        self.fitness = 0
        self.w = w
        self.dead = False

        if w is None:
            self.w = random.gauss(self.w_birth, self.sigma_birth)
        else:
            self.w = w

    def update_weight(self, f):
        self.w += self.beta * f

    def calculate_fitness(self):
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
        self.a += 1
        self.w -= self.eta * self.w

    def death(self):
        prob = self.omega * (1 - self.fitness)
        if random.random() < prob or self.w == 0:
            return True
