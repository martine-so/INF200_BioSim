import random
from animals_class import Animals


class Carnivore(Animals):
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
    mu = 0.4

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
        """Get class parameters"""
        return {'F': cls.F, 'beta': cls.beta, 'phi_age': cls.phi_age, 'phi_weight': cls.phi_weight,
                'a_half': cls.a_half, 'w_half': cls.w_half, 'zeta': cls.zeta, 'w_birth': cls.w_birth,
                'sigma_birth': cls.sigma_birth, 'xi': cls.xi, 'gamma': cls.gamma, 'eta': cls.eta,
                'omega': cls.omega, 'mu': cls.mu}

    def __init__(self, a=0, w=None):
        self.a = a
        self.fitness = 0
        self.w = w

        if w is None:
            self.w = random.gauss(self.w_birth, self.sigma_birth)
        else:
            self.w = w
        super().__init__(a, w)