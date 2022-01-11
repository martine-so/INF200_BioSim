from herbivores_class import Herbivore
from carnivores_class import Carnivore


def test_init_herb_a_default():
    """
    Tests that a new herbivore gets default values if nothing else is given.
    Default value for herbivore age is zero. Since newborns are zero years.
    """
    herb = Herbivore()
    assert herb.a == 0


def test_init_herb_a_defined():
    """
    Tests that a new herbivore gets given age value. Here age is set to 5
    """
    herb = Herbivore(a=5, w=20)
    assert herb.a == 5


def test_init_herb_w_default():  # Må se på dette
    """
    Tests that a new herbivore gets default values if nothing else is given.
    """
    pass


def test_init_herb_w_defined():
    """
    Tests that a new herbivore gets given weight value. Here weight is set to 20.
    """
    herb = Herbivore(a=0, w=20)
    assert herb.w == 20


def test_init_herb_fitness_default():
    """
    Tests that a new herbivore gets default values if nothing else is given.
    Default value for herbivore fitness is zero.
    """
    herb = Herbivore()
    assert herb.fitness == 0


def test_init_herb_dead_default():
    """
    Tests that a new herbivore gets default values if nothing else is given.
    Herbivore default value for dead is False.
    """
    herb = Herbivore()
    assert herb.dead is False


def test_init_carn_a_default():
    """
    Tests that a new carnivore gets default values if nothing else is given.
    Default value for carnivores age is zero. That makes newborns zero years old.
    """
    carn = Carnivore()
    assert carn.a == 0


def test_init_carn_a_defined():
    """
    Tests that a new carnivore gets given age. Here age is set to 5 years.
    """
    carn = Carnivore(a=5, w=20)
    assert carn.a == 5


def test_init_carn_w_default():  # må se på dette
    """
    Tests that a new carnivore gets default values if nothing else is given.
    """
    pass


def test_init_carn_w_defined():
    """
    Tests that a new carnivore gets given weight. Here weight is set to 20.
    """
    carn = Carnivore(a=0, w=20)
    assert carn.w == 20


def test_init_carn_fitness_default():
    """
    Tests that a new carnivore gets default values if nothing else is given.
    Default value for fitness is zero for carnivores.
    """
    carn = Carnivore()
    assert carn.fitness == 0


def test_init_carn_dead_default():
    """
    Tests that a new carnivore gets default values if nothing else is given.
    Default value for dead is False for carnivore.
    """
    carn = Carnivore()
    assert carn.dead is False


def test_update_weight_herb():
    """
    Tests the function that makes Herbivores gain weight as they eat.
    If they eat f=10 times beta=0.9 as default. The weight should go up by 9.
    """
    herb = Herbivore(a=0, w=20)
    herb.update_weight(f=10)
    assert herb.w == 29


def test_update_weight_carn():
    """
    Tests the function that makes carnivores gain weight as they eat.
    If they eat f=50 times beta=0.75 as default. The weight should go up by 37.5.
    """
    carn = Carnivore(a=0, w=20)
    carn.update_weight(f=50)
    assert carn.w == 57.5


def test_calculate_fitness_herb_weight_under_zero():
    """
    Checks that fitness for herbivore equals zero if weight is zero or less.
    """
    herb = Herbivore()
    if herb.w < 0:
        herb.calculate_fitness()
        assert herb.fitness == 0


def test_calculate_fitness_herb_weight_positive():
    """
    Checks that fitness gets calculated right for herbivore if weight is positive.
    Here we calculated by hand that if a=a_half and w=w_half fitness should be 0.25.
    """
    herb = Herbivore(a=40, w=10)
    herb.calculate_fitness()
    assert herb.fitness == 0.25


def test_calculate_fitness_carn_zero():
    carn = Carnivore()
    if carn.w < 0:
        carn.calculate_fitness()
        assert carn.fitness == 0


def test_calculate_fitness_carn_weigth_positive():
    """
    Checks that fitness gets calculated right for carnivore if weight is positive.
    Here we calculated by hand that if a=a_half and w=w_half fitness should be 0.25.
    """
    carn = Carnivore(a=40, w=4)
    carn.calculate_fitness()
    assert carn.fitness == 0.25


def test_breeding_herb_none():
    """
    Checks that newborns don't give birth.
    """
    herb = Herbivore()
    breeding = herb.breeding(2)
    assert breeding is None


def test_breeding_herb_works():
    """
    Checks that if probability is one the herbivore gives birth.
    Here we put number of animals as 20 to make sure probability became one.
    Probability is gamma * fitness * (num_of_animals in cell - 1) or 1 if the equation is over one.
    """
    herb = Herbivore(a=10, w=40)
    herb.calculate_fitness()
    breeding = herb.breeding(20)
    assert breeding


def test_breeding_carn_none():
    """
    Checks that carnivores dont give birth if they are newborn
    """
    carn = Carnivore()
    breeding = carn.breeding(2)
    assert breeding is None


def test_breeding_carn_works():
    """
    Checks that if probability is one the carnivore gives birth.
    Here we put number of carnivores as 20 to make sure probability became one.
    Probability is gamma * fitness * (num_of_animals in cell - 1) or 1 if the equation is over one.
    """
    carn = Carnivore(a=10, w=40)
    carn.calculate_fitness()
    breeding = carn.breeding(20)
    assert breeding


def test_update_a_and_w_herb_a():
    """
    Checks that herbivores age ones every year.
    """
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


def test_death_herb_w_zero():
    herb = Herbivore(a=20, w=0)
    assert herb.death() is True


def test_death_herb_dies():  # se på dette
    pass


def test_death_carn_w_zero():
    carn = Carnivore(a=20, w=0)
    assert carn.death() is True


def test_death_carn_dies():  # se på dette
    pass
