
class Herbivore:


    def __init__(self, a, w):
        self.a = a
        self.w = w
        self.fitness = 0
        self.alive = True


    def update_weight(self, F, beta):
        self.w += beta * F








