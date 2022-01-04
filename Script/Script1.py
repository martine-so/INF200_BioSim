#For testing Herbivores and Lowland

from Herbivores import Herbivore
from Lowland import Lowland
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
years = 10
beta = 0.9
phi_age = 0.6
phi_weight = 0.1
a_half = 40
w_half = 10
zeta = 3.5
w_birth = 8
sigma_birth = 1.5
xi = 1.2
gamma = 0.2
eta = 0.05
omega = 0.4

for i in ini_herbs:
    animals = [Herbivore(j['age'], j['weight']) for j in i['pop']]

for year in range(years):
    lowlandfield = Lowland(f_max, animals)
    lowlandfield.eating(F, beta, phi_age, phi_weight, a_half, w_half)
    lowlandfield.breeding(zeta, w_birth, sigma_birth, xi, gamma)
    lowlandfield.aging()
    lowlandfield.loose_weight(eta)
    lowlandfield.dying(omega)
    animals = lowlandfield.animals
    print(len(animals))


#f_herb = Lowland.fodder(f_max, animals)
