from herbivores_class import Herbivore


def test_update_weight():
     a = 0
     w = 20
     f = 10
     h = Herbivore(a, w)
     h.update_weight(f)
     assert h.w == 29

def test_calculate_fitness():
    h= Herbivore()
    if h.w < 0:
        assert h.fitness == 0

def test_breeding():
    pass

def test_update_a_and_w():
    h = Herbivore()
    for n in range(5):
        h.update_a_and_w()
        assert h.a == n + 1
