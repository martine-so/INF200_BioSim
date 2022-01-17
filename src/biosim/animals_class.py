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
            if key not in ('F', 'beta', 'phi_age', 'phi_weight', 'a_half', 'w_half', 'zeta', 'w_birth',
                           'sigma_birth', 'xi', 'gamma', 'eta', 'omega', 'mu', 'DeltaPhiMax'):
                raise KeyError('Invalid parameter name: ' + key)

            if not 0 <= new_params[key]:
                raise ValueError('All parameter values must be positive')

            if key == 'eta':
                if not new_params['eta'] <= 1:
                    raise ValueError('eta must be in [0, 1].')

            if key == 'DeltaPhiMax':
                if not 0 < new_params['DeltaPhiMax']:
                    raise ValueError('DeltaPhiMax must be higher than 0')
        cls.default_params.update(new_params)

    def __init__(self, a=0, w=None, fitness=0):
        """
        When object i created, if no initial weight is given, a random weight within set values is given
        the new animal. If initial age, weight or fitness is attempted to be set as negative,
        value error is raised.

        :param a: age of an animal. Zero as default value.
        :param w: Weight of an animal.
        :param fitness: Animals fitness with zero as default value.
                        Used mostly when running tests
        """
        self.a = a
        self.fitness = fitness
        self.dead = False
        self.moved = False

        if w is None:
            self.w = random.gauss(self.w_birth, self.sigma_birth)
        else:
            self.w = w

        if self.w < 0 or self.a < 0 or self.fitness < 0:
            raise ValueError('Weight and age must be positive')

    def update_weight(self, f):
        """
        Updates an animal's weight adding given parameter beta multiplied by food eaten
        that year

        :param f: amount of food eaten by an animal that year
        """
        self.w += self.beta * f

    def calculate_fitness(self):
        """"
        Calculates and updates an animals fitness as a number between 0 and 1 based on
        """
        if self.w <= 0:
            self.fitness = 0

        else:
            self.fitness = (1/(1 + math.exp(self.phi_age * (self.a - self.a_half)))) * \
                           (1/(1 + math.exp(-self.phi_weight * (self.w - self.w_half))))

    def breeding(self, num_of_animals):
        """
        Creates class element of the same type as self. Checks if animal fills requirements
        for giving birth. Method returns animal class element if it gives birth, if not it returns None

        :param num_of_animals: Number of animals in same place as self animal
        :type: int

        :return: Newborn if animal can and will give birth. If not; None
        :rtype: Newborn is animal class object of the same type as animal giving birth
        """
        newborn = type(self)()
        if self.w < self.zeta * (self.w_birth + self.sigma_birth) or self.w < self.xi * newborn.w:
            return None

        prob = min(1, self.gamma * self.fitness * (num_of_animals - 1))
        if random.random() < prob:
            self.w -= self.xi * newborn.w
            return newborn
        else:
            return None

    def migrating(self):
        """
        Checks if animal has moved before. If not, the method calculates the probability for moving.
        If a generated random number is lower than calculated probability, the method is to return True

        :return: True, if requirements are met
        """
        if self.moved is False:
            prob = self.mu * self.fitness
            if random.random() < prob:
                return True

    def update_a_and_w(self):
        """
        Updates the age of an animal by 1 and decreases weight by latest weight times set parameter eta
        """
        self.a += 1
        self.w -= self.eta * self.w

    def death(self):
        """
        Calculates probability for animal dying based on it's fitness.
        If random number between 0 and 1 is lower than probability, og the animals weight is zero,
        the method returns True

        :return: True, if requirements are met
        """
        prob = self.omega * (1 - self.fitness)
        if random.random() < prob or self.w == 0:
            return True


class Herbivore(Animals):
    """How Herbivores behave"""

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

    def __init__(self, a=0, w=None, fitness=0):
        """
        :param a: age of an animal. Zero as default value.
        :type a: int
        :param w: Weight of an animal.
        :param fitness: Animals fitness
        """
        super().__init__(a, w, fitness)


class Carnivore(Animals):
    """How Carnivores behave"""

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
    DeltaPhiMax = 10

    default_params = {'F': F, 'beta': beta, 'phi_age': phi_age, 'phi_weight': phi_weight, 'a_half': a_half,
                      'w_half': w_half, 'zeta': zeta, 'w_birth': w_birth, 'sigma_birth': sigma_birth,
                      'xi': xi, 'gamma': gamma, 'eta': eta, 'omega': omega, 'mu': mu, 'DeltaPhiMax': DeltaPhiMax}

    def __init__(self, a=0, w=None, fitness=0):
        """
        :param a: Age of an animal. Zero as default value.
        :param w: Weight of an animal.
        :param fitness: Animals fitness
        """
        super().__init__(a, w, fitness)