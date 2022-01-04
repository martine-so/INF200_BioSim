#For testing Herbivores and Lowland

#from Herbivores import Herbivore
#from Lowlands import Lowland
import textwrap

geogr = """\
           WWW
           WLW
           WWW"""
geogr = textwrap.dedent(geogr)

print(geogr)

ini_herbs = [{'loc': (2, 2),
              'pop': [{'species': 'Herbivore',
                       'age': 5,
                       'weight': 20}
                      for _ in range(50)]}]

coordinates = [i['loc'] for i in ini_herbs]
print(coordinates)

## Finner ut at vi står i Lowland:
f_max = 800
F = 10

for i in ini_herbs:
    for j in i['pop']:
        animals = [Herbivore(j['age'], j['weight'])]


#f_herb = Lowland.fodder(f_max, animals)
