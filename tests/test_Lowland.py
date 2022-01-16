from landscape_class import Lowland
from landscape_class import Highland
from landscape_class import Desert
from animals_class import Herbivore
from animals_class import Carnivore


def test_add_animals_herb():
    """
    Checks that the method add_animals actually adds animals. Here it does so by adding one herbivore and
    checking that the number of herbivores is one more after calling the function.
    """
    field = Lowland()
    init_length = len(field.herb)
    pop = [{'species': 'Herbivore', 'age': 5, 'weight': 20}]
    field.add_animals(pop)
    assert len(field.herb) == init_length + 1


def test_add_animals_carn():
    """
    Checks that the method add_animals actually adds animals. Here it does so by adding one carnivore and
    checking that the number of carnivores is one more after calling the function.
    """
    field = Lowland()
    init_length = len(field.carn)
    pop = [{'species': 'Carnivore', 'age': 5, 'weight': 20}]
    field.add_animals(pop)
    assert len(field.carn) == init_length + 1


def test_reset_fodder_and_moved_f():
    """
    Tests that the amount of food available in a cell is reset every year.
    Here it tests for landscape type lowland where f_max=800 as default.
    """
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
    """
    This test checks that herbivores gain the amount of weight they are supposed to after eating.
    Here it gains beta=0.9 times F=10, so 9.
    """
    field = Lowland()
    field.herb.append(Herbivore(a=5, w=20))
    init_w = field.herb[0].w
    field.eating_herbivores()
    added_w = field.herb[0].beta * field.herb[0].F
    assert field.herb[0].w == init_w + added_w


def test_prob_carn_eating_a():
    """
    This test checks the probability of a carnivore eating. Here we put fitness for carnivore equal to 1
    and fitness for herbivore equal to 0.5.
    If carn.fitness-herb.fitness is over zero but under DeltaPhiMax=10 the probability is calculated by
    (carn.fitness - herb.fitness) / DeltaPhiMax.
    We calculated that it would be 0.05 for this instance.
    """
    field = Lowland()
    field.herb.append(Herbivore(a=5, w=20, fitness=0.5))
    field.carn.append(Carnivore(a=5, w=20, fitness=1))
    prob = field.prob_carn_eating(field.carn[0], field.herb[0])
    assert prob == 0.05


def test_prob_carn_eating_b():
    """
    This test checks the probability of a carnivore eating. Here we put fitness for carnivore equal to 1
    and fitness for herbivore equal to 0.
    If carn.fitness-herb.fitness is over zero but under DeltaPhiMax=0 the probability is calculated by
    (carn.fitness - herb.fitness) / DeltaPhiMax.
    Here it will not be between 0 and DeltaPhiMax.then we check if carn.fitness > herb.fitness.
    In this case it is. Then probability is equal to 1.
    """
    field = Lowland()
    field.herb.append(Herbivore(a=5, w=20, fitness=0))
    field.carn.append(Carnivore(a=5, w=20, fitness=1))
    field.DeltaPhiMax = 0
    prob = field.prob_carn_eating(field.carn[0], field.herb[0])
    assert prob == 1


def test_prob_carn_eating_zero():
    """
    This test checks the probability of a carnivore eating. Here we put fitness for carnivore equal to 0.5
    and fitness for herbivore equal to 1.
    If carn.fitness-herb.fitness is over zero but under DeltaPhiMax=0 the probability is calculated by
    (carn.fitness - herb.fitness) / DeltaPhiMax.
    Here it will not be between 0 and DeltaPhiMax.Then we check if carn.fitness > herb.fitness.
    Here the herbivore has a higher fitness than the carnivore. Then probability of carnivore eating should be equal
    to zero. The test shows that it is.
    """
    field = Lowland()
    field.herb.append(Herbivore(a=5, w=20, fitness=1))
    field.carn.append(Carnivore(a=5, w=20, fitness=0.5))
    prob = field.prob_carn_eating(field.carn[0], field.herb[0])
    assert prob == 0


def test_eating_carnivores_herbs_dying():
    """
    Testing that Herbivores being eaten does die and is removed from herbivore list.
    """
    field = Highland()
    field.herb.extend([Herbivore(a=5, w=40, fitness=0), Herbivore(a=5, w=20, fitness=0)])
    field.carn.append(Carnivore(a=5, w=20, fitness=1))
    field.DeltaPhiMax = 0
    field.eating_carnivores()
    assert len(field.herb) == 0


def test_eating_carnivores_not_eat_too_much():
    """
    This test checks that a carnivore only eats till full even when there are more food available. We put carnivores
    fitness equal to 1, herbivores fitness equal to 0 and DeltaPhiMax=0. That way the carnivore will kill all then
    herbivores until it is full. Here f is default 50. Available food is 60. We check that it only eats 50 and
    therefore the weight only changes by 50 times beta, where beta is 0.75.
    """
    field = Highland()
    field.herb.extend([Herbivore(a=5, w=40, fitness=0), Herbivore(a=5, w=20, fitness=0)])
    field.carn.append(Carnivore(a=5, w=20, fitness=1))
    field.DeltaPhiMax = 0

    carn_start_weight = field.carn[0].w
    added_weight = (field.herb[0].w + (field.herb[1].w-10)) * field.carn[0].beta
    field.eating_carnivores()
    assert field.carn[0].w == carn_start_weight + added_weight


def test_eating_carnivores_gaining_weight():
    """
    Testing that carnivore gains weight and the right amount of weight.
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
    """
    This test checks that after a year the herbivores has aged a year.
    """
    field = Desert()
    field.herb.extend([Herbivore(a=5, w=20), Herbivore(a=7, w=20)])
    init_a = [herb.a for herb in field.herb]
    field.aging_and_loosing_weight()
    for i in range(len(init_a)):
        assert init_a[i] == field.herb[i].a - 1


def test_migrating_animal():
    """
    This test sets the params mu=1 and fitness=1 so that the herbivore has to move. Then we check the initial location
    to see that it is empty, because the herbivore moved to a neighboring cell.
    """
    field = Lowland()
    field.herb.append(Herbivore(a=5, w=20, fitness=1))
    field.herb[0].mu = 1
    loc = (3, 3)
    dict = {(2, 3): Lowland(), (3, 2): Lowland(), (3, 3): field, (3, 4): Lowland(), (4, 3): Lowland()}
    newDict = dict[loc].migrating_animal(loc, dict)
    assert len(newDict[loc].herb) == 0


def test_breeding():
    """
    This test sets the params gamma=1 and fitness=1 so that the probability of breeding is equal to 1.
    Since both herbivores has a probability of breeding equal to one the number of herbivores should double.
    """
    field = Lowland()
    field.herb.extend([Herbivore(a=10, w=40, fitness=1), Herbivore(a=10, w=40, fitness=1)])
    field.herb[0].gamma = 1
    field.herb[1].gamma = 1
    field.breeding()
    assert len(field.herb) == 4


def test_dying():
    """
    This test checks that the herbivores is removed from the list of herbivores if they die.
    We put the weight of the herbivores equal to zero, then they should both die. We check that the length of the
    list of herbivores is equal to zero since both die.
    """
    field = Lowland()
    field.herb.extend([Herbivore(a=5, w=0), Herbivore(a=5, w=0)])
    field.dying()
    assert len(field.herb) == 0

