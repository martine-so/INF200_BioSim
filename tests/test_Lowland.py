from lowland_class import Lowland
from landscape_class import Landscape
from herbivores_class import Herbivore
from carnivores_class import Carnivore


def test_add_animals_herb():
    field = Lowland()
    init_length = len(field.herb)
    pop = [{'species': 'Herbivore', 'age': 5, 'weight': 20}]
    field.add_animals(pop)
    assert len(field.herb) == init_length + 1

def test_add_animals_carn():
    field = Lowland()
    init_length = len(field.carn)
    pop = [{'species': 'Carnivore', 'age': 5, 'weight': 20}]
    field.add_animals(pop)
    assert len(field.carn) == init_length + 1


def test_reset_fodder_and_moved_f():
    field = Lowland()
    field.fodder = 500
    field.reset_fodder_and_moved()
    assert field.fodder == field.f_max


def test_reset_fodder_and_moved_m():
    """
    Checks that moved attribute is reset to False.
    Here we only test for Herbivore since code for resetting attribute is the same for carnivore
    and herbivore.
    """
    field = Lowland()
    field.herb.append(Herbivore(a=5, w=20))
    field.herb[0].moved = True
    field.reset_fodder_and_moved()
    assert field.herb[0].moved is False


def test_eating_herbivores():
    field = Lowland()
    field.herb.append(Herbivore(a=5, w=20))
    field.eating_herbivores()
    assert field.herb[0].w == 29


def test_prob_carn_eating_A():
    field = Lowland()
    field.herb.append(Herbivore(a=5, w=20))
    field.carn.append(Carnivore(a=5, w=20))
    field.carn[0].fitness = 1
    field.herb[0].fitness = 0.5
    prob = field.prob_carn_eating(field.carn[0], field.herb[0])
    assert prob == 0.05


def test_prob_carn_eating_B():
    field = Lowland()
    field.herb.append(Herbivore(a=5, w=20))
    field.carn.append(Carnivore(a=5, w=20))
    field.DeltaPhiMax = 0.5
    field.carn[0].fitness = 1
    field.herb[0].fitness = 0.25
    prob = field.prob_carn_eating(field.carn[0], field.herb[0])
    assert prob == 1


def test_prob_carn_eating_zero():
    field = Lowland()
    field.herb.append(Herbivore(a=5, w=20))
    field.carn.append(Carnivore(a=5, w=20))
    field.carn[0].fitness = 0.5
    field.herb[0].fitness = 1
    prob = field.prob_carn_eating(field.carn[0], field.herb[0])
    assert prob == 0


def test_eating_carnivores():
    field = Lowland()
    field.herb.append(Herbivore(a=5, w=20))
    field.carn.append(Carnivore(a=5, w=20))
    pass


def test_aging_and_loosing_weight_a():
    field = Lowland()
    field.herb.extend([Herbivore(a=5, w=20), Herbivore(a=5, w=20)])
    init_a = [herb.a for herb in field.herb]
    field.aging_and_loosing_weight()
    for i in range(len(init_a)):
        assert init_a[i] == field.herb[i].a - 1


def test_aging_and_loosing_weight_w():
    pass

def test_breeding():
    pass

def test_loose_weight():
    pass

def test_dying():
    pass

