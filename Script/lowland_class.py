from landscape_class import Landscape
#from carnivores_class import Carnivore
#from operator import attrgetter
import random


class Lowland(Landscape):
    """Lowland"""

    # parameters defined at class level
    f_max = 800

    default_params = {'f_max': f_max}

    @classmethod
    def set_params(cls, new_params):
        """Set class parameters
        """

        for key in new_params:
            if key not in 'f_max':
                raise KeyError('Invalid parameter name: ' + key)

        for key in new_params:
            if not 0 <= new_params[key]:
                raise ValueError('All parameter values must be positive')
            cls.key = new_params[key]

    @classmethod
    def get_params(cls):
        """Get class parameters"""
        return {'f_max': cls.f_max}

    def __init__(self, herb, carn):
        self.f_max = 800

        self.DeltaPhiMax = 10 # Carnivore

        self.fodder = self.f_max
        self.herb = herb
        self.carn = carn
        super().__init__(herb, carn)
