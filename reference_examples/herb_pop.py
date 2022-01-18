"""
Island with lowland cells and herbivores only. To see what number the population stabilises at.
With f_max at 800 and f (the amount a herbivore wants to eat) at 10 one cell has enough food to feed 80 herbivores.
With a 3x3 island you should have enough food for 9*80 = 720 herbivores every year.
Yet the example shows it stabilises at a much higher number.
"""


import textwrap
from biosim.simulation import BioSim

geogr = """\
           WWWWW
           WLLLW
           WLLLW
           WLLLW
           WWWWW"""

geogr = textwrap.dedent(geogr)

ini_herbs = [{'loc': (2, 2),
              'pop': [{'species': 'Herbivore',
                       'age': 5,
                       'weight': 20}
                      for _ in range(50)]}]


sim = BioSim(geogr, ini_herbs, seed=100, img_dir='results', img_years=300)
sim.simulate(201)
