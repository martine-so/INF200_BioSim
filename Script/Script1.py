"""For testing Herbivores and Lowland"""

from Herbivores import Herbivore
from Lowland import Lowland
import textwrap

geogr = """\
           WWW
           WLW
           WWW"""
geogr = textwrap.dedent(geogr)

ini_herbs = [{'loc': (2, 2),
              'pop': [{'species': 'Herbivore',
                       'age': 5,
                       'weight': 20}
                      for _ in range(50)]}]

coordinates = [i['loc'] for i in ini_herbs]

for i in coordinates:
    x, y = i
location = geogr.split()[x-1][y-1]
landtypes = {'L': Lowland}
if location in landtypes:
    landtype = landtypes[location]

years = 50
for i in ini_herbs:
    animals = [Herbivore(j['age'], j['weight']) for j in i['pop']]

for year in range(years):
    field = landtypes[location](animals)
    field.eating()
    field.breeding()
    # print(len(animals))
    field.aging()
    field.loose_weight()
    field.dying()
    animals = field.animals  # Får samme tall selv om denne kommenteres ut. Kan dette være kilden til feil tall??
    print(len(animals))  # Alle føder 2. året. WHYYYYYYY?!?!?!?!

