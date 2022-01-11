from herbivores_class import Herbivore
from carnivores_class import Carnivore


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
        herb.calculate_fitness()
        assert herb.fitness == 0


def test_calculate_fitness_herb_weight_positive():
    herb = Herbivore(a=40, w=10)
    herb.calculate_fitness()
    assert herb.fitness == 0.25


def test_calculate_fitness_carn_zero():
    carn = Carnivore()
    if carn.w < 0:
        carn.calculate_fitness()
        assert carn.fitness == 0

def test_calculate_fitness_carn_weigth_positive():
    carn = Carnivore(a=40, w=4)
    carn.calculate_fitness()
    assert carn.fitness == 0.25


def test_breeding_herb():
    herb = Herbivore()
    breeding = herb.breeding(2)
    assert breeding is None


def test_breeding_carn():
    carn = Carnivore()
    breeding = carn.breeding(2)
    assert breeding is None


def test_update_a_and_w_herb_a():
    herb = Herbivore()
    for n in range(5):
        herb.update_a_and_w()
        assert herb.a == n + 1


def test_update_a_and_w_herb_w():
    herb = Herbivore(a=2, w=10)
    herb.update_a_and_w()
    assert herb.w == 9.5


def test_update_a_and_w_carn_a():
    carn = Carnivore()
    for n in range(2):
        carn.update_a_and_w()
        assert carn.a == n + 1


def test_update_a_and_w_carn_w():
    carn = Carnivore(a=2, w=10)
    carn.update_a_and_w()
    assert carn.w == 8.75
