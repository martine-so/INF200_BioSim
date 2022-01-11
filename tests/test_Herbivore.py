from herbivores_class import Herbivore
from carnivores_class import Carnivore
from animals_class import Animals


def test_update_weight_herb():
     herb = Herbivore(a=0, w=20)
     herb.update_weight(f=10)
     assert herb.w == 29


def test_update_weight_carn():
    carn = Carnivore(a=0, w=20)
    carn.update_weight(f=50)
    assert carn.w == 57.5


def test_calculate_fitness_herb_weight_under_zero():
    herb= Herbivore()
    if herb.w < 0:
        assert herb.fitness == 0


def test_calculate_fitness_herb_weight_positive():
    herb = Herbivore(a=40, w=10)
    assert herb.fitness == 0  # skal vist være null?? Er det mattekunskaper det står i? 0.25??


def test_calculate_fitness_carn():
    carn= Carnivore()
    if carn.w < 0:
        assert carn.fitness == 0


def test_breeding():
    pass


def test_update_a_and_w():
    h = Herbivore()
    for n in range(5):
        h.update_a_and_w()
        assert h.a == n + 1
