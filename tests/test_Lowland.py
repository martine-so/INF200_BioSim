from lowland_class import Lowland
from landscape_class import Landscape
from herbivores_class import Herbivore
from carnivores_class import Carnivore

def test_eating_herbivores():
    field = Lowland()
    field.herb.extend(Herbivore(a=5, w=20))
    field.eating_herbivores()
    # assert field.herb.w == 29
    pass

def test_prob_carn_eating():
    # field.carn.extend(Carnivore(a=5, w=20))
    pass

def test_eating_carnivores():
    pass

def test_aging_and_loosing_weight_a():
    pass

def test_aging_and_loosing_weight_w():
    pass

def test_breeding():
    pass

def test_loose_weight():
    pass

def test_dying():
    pass

