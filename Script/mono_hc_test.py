"""
Island with single lowland cell, first herbivores only, later carnivores.
"""


__author__ = 'Hans Ekkehard Plesser, NMBU'


import textwrap
from sim_herb_and_carn import BioSim

geogr = """\
           WWWWW
           WWLWW
           WLDLW
           WWLLW
           WWWWW"""
geogr = textwrap.dedent(geogr)

ini_herbs = [{'loc': (3, 3),
              'pop': [{'species': 'Herbivore',
                       'age': 5,
                       'weight': 20}
                      for _ in range(50)]}]
ini_carns = [{'loc': (3, 3),
              'pop': [{'species': 'Carnivore',
                       'age': 5,
                       'weight': 20}
                      for _ in range(20)]}]

#for seed in range(100, 103):
seed = 100
sim = BioSim(geogr, ini_herbs, seed=seed,
             img_dir='results', img_base=f'mono_hc_{seed:05d}', img_years=300)
sim.simulate(50)
sim.add_population(ini_carns)
sim.simulate(251)
