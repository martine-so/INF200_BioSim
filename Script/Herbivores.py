import math
import random


class Herbivore:

    params = {'beta': 0.9, 'phi_age': 0.6, 'phi_weight': 0.1, 'a_half': 40, 'w_half': 10,
              'zeta': 3.5, 'w_birth': 8, 'sigma_birth': 1.5, 'xi': 1.2, 'gamma': 0.2, 'eta': 0.05, 'omega': 0.4}
    @classmethod
    def set_params(cls, new_params):
        """Set class parameters
        """

        for key in new_params:
            if key not in ('beta', 'phi_age', 'phi_weight', 'a_half', 'w_half', 'zeta', 'w_birth',
                           'sigma_birth', 'xi', 'gamma', 'eta', 'omega'):
                raise KeyError('Invalid parameter name: ' + key)

        for key in new_params:
            if not 0 <= new_params[key]:
                raise ValueError('All parametervalues must be positiv')
            cls.key = new_params[key]

        if 'eta' in new_params:
            if not new_params['eta'] <= 1:
                raise ValueError('eta must be in [0, 1].')
            cls.eta = new_params['eta']

        if 'DeltaPhiMax' in new_params:
            if not 0 < new_params['DeltaPhiMax']:
                raise ValueError('DeltaPhiMax must be higher than 0')
            cls.DeltaPhiMax = new_params['DeltaPhiMax']

    @classmethod
    def get_params(cls):
        """Get class parameters"""
        return {'F': cls.F, 'beta': cls.beta, 'phi_age': cls.phi_age, 'phi_weight': cls.phi_weight,
                'a_half': cls.a_half, 'w_half': cls.w_half, 'zeta': cls.zigma, 'w_birth': cls.w_birth,
                'sigma_birth': cls.sigma_birth, 'xi': cls.xi, 'gamma': cls.gamma, 'eta': cls.eta,
                'omega': cls.omega}
        # mu skal også inn her når de beveger seg

    def __init__(self, a=0, w=8, seed=100):
        self.a = a
        self.w = w
        self.fitness = 0
        self.alive = True
        self.baby = False
        random.seed(seed)

        self.beta = 0.9
        self.phi_age = 0.6
        self.phi_weight = 0.1
        self.a_half = 40
        self.w_half = 10
        self.zeta = 3.5
        self.w_birth = 8
        self.sigma_birth = 1.5
        self.xi = 1.2
        self.gamma = 0.2
        self.eta = 0.05
        self.omega = 0.4
        self.F = 10

    def update_weight(self, f):
        self.w += self.beta * f

    def calculate_fitness(self):
        if self.w <= 0:
            self.fitness = 0

        else:
            self.fitness = (1/(1 + math.exp(self.phi_age * (self.a - self.a_half)))) * \
                           (1/(1 + math.exp(-self.phi_weight * (self.w - self.w_half))))


    def breeding(self, N):
        if self.w < self.zeta * (self.w_birth + self.sigma_birth):
            probability = 0
        elif self.w < self.xi * self.w_birth:  # xi * babys vekt. Vet ikke helt hva babys vekt er?
            probability = 0
        else:
            probability = min(1, self.gamma * self.fitness * (N - 1))

        if random.random() < probability:
            self.baby = True
            self.w -= self.xi * self.w_birth
        else:
            self.baby = False

    def update_a(self):
        self.a += 1

    def loose_weight(self):
        self.w -= self.eta * self.w

    def death(self):
        if self.w == 0:
            self.alive = False
        else:
            probability = self.omega * (1 - self.fitness)
            if random.random() < probability:
                self.alive = False
