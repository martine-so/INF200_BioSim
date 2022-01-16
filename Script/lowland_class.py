from landscape_class import Landscape


class Lowland(Landscape):
    """Lowland"""

    # parameters defined at class level
    f_max = 800

    default_params = {'f_max': f_max}

    def __init__(self):
        self.fodder = self.f_max

        super().__init__()
