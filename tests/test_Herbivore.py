from Herbivores import Herbivore


def test_update_weight():
     h = Herbivore()
     w=20
     f=10
     h.update_weight()
     assert w == 29 #??

def test_calculate_fitness():
    h= Herbivore()
    if h.w < 0:
        assert h.fitness == 0

def test_breeding():
    pass

def test_update_a():
    h = Herbivore()
    for n in range(5):
        h.update_a()
        assert h.a == n + 1
