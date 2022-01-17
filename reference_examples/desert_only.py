"""
Island with only desert cells and herbivores only to see how fast they die without food.
"""


__author__ = ''


import textwrap
from biosim.simulation import BioSim

geogr = """\
           WWWWW
           WDDDW
           WDDDW
           WDDDW
           WWWWW"""

geogr = textwrap.dedent(geogr)

ini_herbs = [{'loc': (3, 3),
              'pop': [{'species': 'Herbivore',
                       'age': 5,
                       'weight': 30}
                      for _ in range(50)]}]

for seed in range(100, 103):
    sim = BioSim(geogr, ini_herbs, seed=seed,
                 img_dir='results', img_base=f'mono_hc_{seed:05d}', img_years=300)
    sim.simulate(50)
