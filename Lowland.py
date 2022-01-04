
class Lowland:

    def __init__(self, f_max, animals):
        self.fodder = f_max
        self.animals = animals

    def eating(self, F):
        if F < self.fodder:
            f = self.fodder
        else:
            f = F
        return f