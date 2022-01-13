from lowland_class import Lowland
from highland_class import Highland
from desert_class import Desert
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
    field.herb.append(Herbivore(a=5, w=20, fitness=0.5))
    field.carn.append(Carnivore(a=5, w=20, fitness=1))
    prob = field.prob_carn_eating(field.carn[0], field.herb[0])
    assert prob == 0.05


def test_prob_carn_eating_B():
    field = Lowland()
    field.herb.append(Herbivore(a=5, w=20, fitness=0))
    field.carn.append(Carnivore(a=5, w=20, fitness=1))
    field.DeltaPhiMax = 0
    prob = field.prob_carn_eating(field.carn[0], field.herb[0])
    assert prob == 1


def test_prob_carn_eating_zero():
    field = Lowland()
    field.herb.append(Herbivore(a=5, w=20, fitness=1))
    field.carn.append(Carnivore(a=5, w=20, fitness=0.5))
    prob = field.prob_carn_eating(field.carn[0], field.herb[0])
    assert prob == 0


def test_eating_carnivores_Herbs_dying():
    """
    Testing that Herbivores being eaten does die and is removed from herbivore list
    """
    field = Highland()
    field.herb.extend([Herbivore(a=5, w=40, fitness=0), Herbivore(a=5, w=20, fitness=0)])
    field.carn.append(Carnivore(a=5, w=20, fitness=1))
    field.DeltaPhiMax = 0
    field.eating_carnivores()
    assert len(field.herb) == 0

def test_eating_carnivores_Not_eat_too_much():
    field = Highland()
    field.herb.extend([Herbivore(a=5, w=40, fitness=0), Herbivore(a=5, w=20, fitness=0)])
    field.carn.append(Carnivore(a=5, w=20, fitness=1))
    field.DeltaPhiMax = 0

    carn_start_weight = field.carn[0].w
    added_weight = (field.herb[0].w + (field.herb[1].w-10)) * field.carn[0].beta
    field.eating_carnivores()
    assert field.carn[0].w == carn_start_weight + added_weight

def test_eating_carnivores_Herbs_dying():
    """
    Testing that Herbivores being eaten does die
    :return:
    """
    field = Highland()
    field.herb.append(Herbivore(a=5, w=20, fitness=0))
    field.carn.append(Carnivore(a=5, w=20, fitness=1))
    field.DeltaPhiMax = 0

    carn_start_weight = field.carn[0].w
    added_weight = field.herb[0].w * field.carn[0].beta
    field.eating_carnivores()
    assert field.carn[0].w == carn_start_weight + added_weight

def test_aging_and_loosing_weight_a():
    field = Desert()
    field.herb.extend([Herbivore(a=5, w=20), Herbivore(a=5, w=20)])
    init_a = [herb.a for herb in field.herb]
    field.aging_and_loosing_weight()
    for i in range(len(init_a)):
        assert init_a[i] == field.herb[i].a - 1

def test_migrating_animal():
    field = Lowland()
    field.herb.append(Herbivore(a=5, w=20, fitness=1))
    field.herb[0].mu = 1
    loc = (3, 3)
    dict = {(2, 3): Lowland(), (3, 2): Lowland(), (3, 3): field, (3, 4): Lowland(), (4, 3): Lowland()}
    newDict = dict[loc].migrating_animal(loc, dict)
    assert len(newDict[loc].herb) == 0

def test_breeding():
    field = Lowland()
    field.herb.extend([Herbivore(a=10, w=40, fitness=1), Herbivore(a=10, w=40, fitness=1)])
    field.herb[0].gamma = 1
    field.herb[1].gamma = 1
    field.breeding()
    assert len(field.herb) == 4

def test_dying():
    field = Lowland()
    field.herb.extend([Herbivore(a=5, w=0), Herbivore(a=5, w=0)])
    field.dying()
    assert len(field.herb) == 0

