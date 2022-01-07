import math
import random

class Carnivore:
    """How Carnivores work"""

    # Parameters defined at class level
    F = 50
    beta = 0.75
    phi_age = 0.3
    phi_weight = 0.4
    a_half = 40
    w_half = 4
    zeta = 3.5
    w_birth = 6
    sigma_birth = 1
    xi = 1.1
    gamma = 0.8
    eta = 0.125
    omega = 0.8

    default_params = {'F': F, 'beta': beta, 'phi_age': phi_age, 'phi_weight': phi_weight, 'a_half': a_half,
                      'w_half': w_half, 'zeta': zeta, 'w_birth': w_birth, 'sigma_birth': sigma_birth,
                      'xi': xi, 'gamma': gamma, 'eta': eta, 'omega': omega}

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
                raise ValueError('All parameter values must be positive')
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
                'a_half': cls.a_half, 'w_half': cls.w_half, 'zeta': cls.zeta, 'w_birth': cls.w_birth,
                'sigma_birth': cls.sigma_birth, 'xi': cls.xi, 'gamma': cls.gamma, 'eta': cls.eta,
                'omega': cls.omega}
        # mu skal også inn her når de beveger seg

    def __init__(self, a=0, w=6, seed=100):
        self.a = a
        self.w = w
        self.seed = seed
        self.fitness = 0
        self.alive = True
        self.baby = False
        self.newborn_weight = 0
        random.seed(self.seed)

    def update_weight(self, f):
        self.w += self.beta * f

    def calculate_fitness(self):
        if self.w <= 0:
            self.fitness = 0

        else:
            self.fitness = (1/(1 + math.exp(self.phi_age * (self.a - self.a_half)))) * \
                           (1/(1 + math.exp(-self.phi_weight * (self.w - self.w_half))))

    def breeding(self, N):
        self.newborn_weight = random.gauss(self.w_birth, self.sigma_birth)
        if self.w < self.zeta * (self.w_birth + self.sigma_birth):
            probability = 0
        elif self.w < self.xi * self.newborn_weight:  # xi * babys vekt. Vet ikke helt hva babys vekt er?
            probability = 0
        else:
            probability = min(1, self.gamma * self.fitness * (N - 1))

        if random.random() < probability:
            self.baby = True
            self.w -= self.xi * self.newborn_weight
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

