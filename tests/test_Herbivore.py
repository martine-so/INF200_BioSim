from biosim.animals_class import Herbivore
from biosim.animals_class import Carnivore
import pytest


def test_set_params_not_in_new_params():
    """
    This test checks that KeyError is raised if param is not in new_params.
    Here we tested it with a typo in w_birth
    """
    with pytest.raises(KeyError):
        Herbivore().set_params({'w_birt': 8})


def test_set_params_():
    """
    This test checks that parameter gets changed.
    """
    herb = Herbivore()
    herb.set_params({'w_birth': 20})
    assert herb.default_params['w_birth'] == 20


def test_set_params_negative():
    """
    This test checks that setting params as negative values raises ValueError.
    """
    with pytest.raises(ValueError):
        Carnivore().set_params({'beta': -2})


def test_set_params_eta():
    """
    This test checks that setting the param eat as a value of outside of [0,1] raises ValueError.
    """
    with pytest.raises(ValueError):
        Herbivore().set_params({'eta': 3})


def test_set_params_deltaphimax():
    """
    This test checks that setting the param DeltaPhiMax as a value of zero or less raises ValueError.
    """
    with pytest.raises(ValueError):
        Carnivore().set_params({'DeltaPhiMax': 0})


def test_a_w_fitness_is_negative():
    """
    Tests that value error is raised if any the animals attributes initial values
    is attempted to be set as a negative number
    """
    with pytest.raises(ValueError):
        herb1 = Herbivore(a=-1)
        herb2 = Herbivore(w=-1)
        herb3 = Herbivore(fitness=-1)

def test_init_herb_a_default():
    """
    Tests that a new herbivore gets default values if nothing else is given.
    Default value for herbivore age is zero, since newborns are zero years.
    """
    herb = Herbivore()
    assert herb.a == 0


def test_init_herb_a_defined():
    """
    Tests that a new herbivore gets given age value. Here age is set to 5
    """
    herb = Herbivore(a=5, w=20)
    assert herb.a == 5


def test_init_herb_w_default():
    """
    Tests that a new herbivore gets default values if nothing else is given.
    """
    herb = Herbivore()
    assert herb.w is not None


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


def test_init_carn_w_default():
    """
    Tests that a new carnivore gets default values if nothing else is given.
    """
    carn = Carnivore()
    assert carn.w is not None


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
    """
    Checks that fitness for herbivore equals zero if weight is zero or less.
    """
    carn = Carnivore()
    if carn.w < 0:
        carn.calculate_fitness()
        assert carn.fitness == 0


def test_calculate_fitness_carn_weight_positive():
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
    # herb.calculate_fitness()
    herb.fitness = 1
    Herbivore.set_params({'gamma': 1})
    breeding = herb.breeding(2)
    assert breeding is not None


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
    """
    Checks that herbivore looses the amount of weight it is supposed to.
    looses eta=0.05 * weight=10. Here it looses 0.5.
    """
    herb = Herbivore(a=2, w=10)
    herb.update_a_and_w()
    assert herb.w == 9.5


def test_update_a_and_w_carn_a():
    """
    Checks that carnivore ages one year every year.
    """
    carn = Carnivore()
    for n in range(2):
        carn.update_a_and_w()
        assert carn.a == n + 1


def test_update_a_and_w_carn_w():
    """
    Checks that carnivore looses the amount of weight it is supposed to every year.
    looses eta=0.125 * weight=10. Here it looses 1.25.
    """
    carn = Carnivore(a=2, w=10)
    carn.update_a_and_w()
    assert carn.w == 8.75


def test_death_herb_w_zero():
    """
    Checks that herbivores dies if weight is zero or less
    """
    herb = Herbivore(a=20, w=0)
    assert herb.death() is True


def test_death_herb_dies():
    """
    Checks that herbivores die when probability is set to 1
    """
    herb = Herbivore(a=5, w=20)
    herb.fitness = 0
    herb.omega = 1
    assert herb.death() is True


def test_death_carn_w_zero():
    """
    Checks that carnivores dies if weight equals zero or less.
    """
    carn = Carnivore(a=20, w=0)
    assert carn.death() is True


def test_death_carn_dies():
    """
    Checks that herbivores die when probability is set to 1
    """
    carn = Carnivore(a=5, w=20)
    carn.fitness = 0
    carn.omega = 1
    assert carn.death() is True

def test_migrating_herb():
    """
    Checks that animals move when probability is 1 and they have not moved before
    """
    herb = Herbivore()
    Herbivore.set_params({'mu': 1})
    herb.fitness = 1
    assert herb.migrating() is True

def test_migrating_herb_same_year():
    """
    Checks that animals do not move if attribute moved is True
    """
    herb = Herbivore()
    herb.moved = True
    assert herb.migrating() is not True

def test_migrating_carn():
    """
    Checks that animals move when probability is 1 and they have not moved before
    """
    carn = Carnivore()
    Carnivore.set_params({'mu': 1})
    carn.fitness = 1
    assert carn.migrating() is True

def test_migrating_carn_same_year():
    """
    Checks that animals do not move if attribute moved is True
    """
    carn = Carnivore()
    carn.moved = True
    assert carn.migrating() is not True
