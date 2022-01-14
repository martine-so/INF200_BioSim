from island_class import Island
from herbivores_class import Herbivore
import textwrap
import pytest


def test_place_animals():
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


@pytest.fixture
def set_params(request):
    Island.set_params(request.param)
    yield
    Island.set_params(Island.default_params)

@pytest.mark.parameterize('set_params', [{'mu': 1}] , indirect=True)
def test_migrating():
    geogr = """\
                   WWWWW
                   WWLWW
                   WLLLW
                   WWLWW
                   WWWWW"""

    ini_herbs = [{'loc': (3, 3),
                  'pop': [{'species': 'Herbivore',
                           'age': 5,
                           'weight': 20}]}]
    geogr = textwrap.dedent(geogr)
    island = Island(geogr)
    island.place_animals(ini_herbs)
    initial_loc = island.animals_loc

    island.migrating()
    for loc in initial_loc:
    #assert len(initial_loc[loc].herb) != len(island.animals_loc[loc].herb)
     pass


def test_one_year():
    pass