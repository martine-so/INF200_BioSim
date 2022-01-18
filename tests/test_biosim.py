import pytest
from biosim.simulation import BioSim
from biosim.animals import Herbivore

def test_set_animal_parameters():
    """
    Testing that setting new parameters for given animal species works properly
    """
    ini_pop = [{'loc': (2, 2),
              'pop': [{'species': 'Herbivore',
                       'age': 5,
                       'weight': 20}
                      for _ in range(50)]}]

    bio_sim = BioSim(island_map="WWWW\nWLHW\nWWWW", ini_pop=ini_pop, seed=1, vis_years=0)
    bio_sim.set_animal_parameters('Herbivore', {'w_birth': 6})

    assert bio_sim.island.animals_loc[(2, 2)].herb[0].default_params["w_birth"] == 6

def test_set_landscape_parameters():
    """
    Testing that setting new parameters for given landscape type works properly
    """
    bio_sim = BioSim(island_map="WWWW\nWLHW\nWWWW", ini_pop=[], seed=1, vis_years=0)
    bio_sim.set_landscape_parameters('L', {'f_max': 500})
    assert bio_sim.island.animals_loc[(2, 2)].default_params['f_max'] == 500

def test_num_animals_plot():
    """
    Testing that method for finding amount of herbivores and carnivores separately
    works, by checking if correct amount is returned for given species
    """
    ini_pop = [{'loc': (2, 2),
                'pop': [{'species': 'Herbivore',
                         'age': 5,
                         'weight': 20}
                        for _ in range(50)]}]
    bio_sim = BioSim(island_map="WWWW\nWLHW\nWWWW", ini_pop=ini_pop, seed=1, vis_years=0)
    herbs_on_island = 0
    for loc in bio_sim.island.animals_loc:
        herbs_on_island += len(bio_sim.island.animals_loc[loc].herb)
    numHerbs, numCarns = bio_sim.num_animals_plot()
    assert herbs_on_island == numHerbs

def test_simulate_and_property_year():
    """
    Testing that year count is correct, even when visualization is not wanted for simulation
    Also testing that year property shows last year simulated
    """
    bio_sim = BioSim(island_map="WWWW\nWLHW\nWWWW", ini_pop=[], seed=1, vis_years=0)
    bio_sim.simulate(num_years=5)
    assert bio_sim.years == 5 and bio_sim.year == 5

def test_add_population():
    pass


def test_property_num_animals():
    """
    Testing num_animals property is the correct total amount of animals on the island
    """
    ini_pop = [{'loc': (2, 2),
                'pop': [{'species': 'Herbivore',
                         'age': 5,
                         'weight': 20}
                        for _ in range(50)]}]
    bio_sim = BioSim(island_map="WWWW\nWLHW\nWWWW", ini_pop=ini_pop, seed=1, vis_years=0)
    numHerbs, numCarns = bio_sim.num_animals_plot()
    assert bio_sim.num_animals == numHerbs + numCarns

def test_property_num_animals_per_species():
    """
    Testing num_animals_per_species property returns a dictionary with species as key,
    and amount of animals for each species as key values
    """
    ini_pop = [{'loc': (2, 2),
                'pop': [{'species': 'Herbivore',
                         'age': 5,
                         'weight': 20}
                        for _ in range(50)]}]
    bio_sim = BioSim(island_map="WWWW\nWLHW\nWWWW", ini_pop=ini_pop, seed=1, vis_years=0)
    numHerbs, numCarns = bio_sim.num_animals_plot()
    assert bio_sim.num_animals_per_species == {'Herbivore': numHerbs, 'Carnivore': numCarns}