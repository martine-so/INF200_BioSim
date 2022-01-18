from biosim.island import Island
from biosim.animals import Herbivore
import textwrap
import pytest


def test_place_animals():
    """
    Testing class method in island for placing animals on given coordinates on the island
    """
    geogr = """\
                   WWWWW
                   WWLWW
                   WLLLW
                   WWLWW
                   WWWWW"""

    ini_herbs = [{'loc': (1, 7),
                  'pop': [{'species': 'Herbivore',
                           'age': 5,
                           'weight': 20}
                          for _ in range(10)]}]
    geogr = textwrap.dedent(geogr)
    island = Island(geogr)

    with pytest.raises(ValueError):
        island.place_animals(ini_herbs)


def test_migrating():
    """
    Testing the animals migrate on the island when parameters are manipulated to guarantee migration for animals
    """
    geogr = """\
                   WWWWW
                   WWLWW
                   WLLLW
                   WWLWW
                   WWWWW"""

    ini_herbs = [{'loc': (3, 3),
                  'pop': [{'species': 'Herbivore', 'age': 5, 'weight': 20}
                          for _ in range(10)]}]

    geogr = textwrap.dedent(geogr)
    island = Island(geogr)
    island.place_animals(ini_herbs)
    initial_num_animals = len(island.animals_loc[(3, 3)].herb)

    Herbivore.set_params({'mu': 1})
    for herb in island.animals_loc[(3, 3)].herb:
        herb.fitness = 1
    island.migrating()
    assert initial_num_animals != len(island.animals_loc[(3, 3)].herb)


def test_matrix():
    """
    Testing the matrix has dimentions corresponding with the given island
    """
    geogr = """\
                       WWWWW
                       WWLWW
                       WLLLW
                       WWLWW
                       WWWWW"""

    geogr = textwrap.dedent(geogr)
    island = Island(geogr)
    herb_matrix, carn_matrix = island.matrix()

    for row in herb_matrix:
        assert len(row) == len(geogr.split()[0])


def test_age_fitness_weight_herb():
    """
    Test for checking that age, fitness and weight for every animal placed on island is appended to
    lists for age, weight and fitness based on species
    """
    geogr = """\
                       WWWWW
                       WWLWW
                       WLLLW
                       WWLWW
                       WWWWW"""

    ini_herbs = [{'loc': (3, 3),
                  'pop': [{'species': 'Herbivore', 'age': 5, 'weight': 20}
                          for _ in range(10)]}]

    geogr = textwrap.dedent(geogr)
    island = Island(geogr)
    island.place_animals(ini_herbs)

    num_herbs = len(island.animals_loc[(3, 3)].herb)
    num_carns = len(island.animals_loc[(3, 3)].carn)
    age_herb, weight_herb, fitness_herb = island.age_fitness_weight_herb()
    age_carn, weight_carn, fitness_carn = island.age_fitness_weight_carn()
    assert len(age_herb) == num_herbs and len(age_carn) == num_carns
