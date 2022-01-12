"""
Template for BioSim class.
"""

# The material in this file is licensed under the BSD 3-clause license
# https://opensource.org/licenses/BSD-3-Clause
# (C) Copyright 2021 Hans Ekkehard Plesser / NMBU
from island_class import Island
import matplotlib.pyplot as plt
import random

class BioSim:
    def __init__(self, island_map, ini_pop, seed,
                 vis_years=1, ymax_animals=None, cmax_animals=None, hist_specs=None,
                 img_dir=None, img_base=None, img_fmt='png', img_years=None,
                 log_file=None):

        self.island_map = island_map        # In use on graph
        self.ini_pop = ini_pop              # In use on graph
        self.seed = seed                    # In use on graph
        self.vis_years = vis_years
        self.ymax_animals = ymax_animals    # In use on graph
        self.cmax_aminals = cmax_animals
        self.hist_specs = hist_specs
        self.img_dir = img_dir
        self.img_base = img_base
        self.img_fmt = img_fmt
        self.img_years = img_years
        self.log_file = log_file

        self.years = 0
        self.herb = []
        self.carn = []

        self.island = Island(self.island_map)
        self.island.place_animals(self.ini_pop)
        self.coordinates = [i['loc'] for i in self.ini_pop]

        """
        :param island_map: Multi-line string specifying island geography
        :param ini_pop: List of dictionaries specifying initial population
        :param seed: Integer used as random number seed
        :param ymax_animals: Number specifying y-axis limit for graph showing animal numbers
        :param cmax_animals: Dict specifying color-code limits for animal densities
        :param hist_specs: Specifications for histograms, see below
        :param vis_years: years between visualization updates (if 0, disable graphics)
        :param img_dir: String with path to directory for figures
        :param img_base: String with beginning of file name for figures
        :param img_fmt: String with file type for figures, e.g. 'png'
        :param img_years: years between visualizations saved to files (default: vis_years)
        :param log_file: If given, write animal counts to this file

        If ymax_animals is None, the y-axis limit should be adjusted automatically.
        If cmax_animals is None, sensible, fixed default values should be used.
        cmax_animals is a dict mapping species names to numbers, e.g.,
           {'Herbivore': 50, 'Carnivore': 20}

        hist_specs is a dictionary with one entry per property for which a histogram shall be shown.
        For each property, a dictionary providing the maximum value and the bin width must be
        given, e.g.,
            {'weight': {'max': 80, 'delta': 2}, 'fitness': {'max': 1.0, 'delta': 0.05}}
        Permitted properties are 'weight', 'age', 'fitness'.

        If img_dir is None, no figures are written to file. Filenames are formed as

            f'{os.path.join(img_dir, img_base}_{img_number:05d}.{img_fmt}'

        where img_number are consecutive image numbers starting from 0.

        img_dir and img_base must either be both None or both strings.
        """

    # def set_animal_parameters(self, species, params):
    #     """
    #     Set parameters for animal species.
    #
    #     :param species: String, name of animal species
    #     :param params: Dict with valid parameter specification for species
    #     """
    #
    #     @classmethod
    #     def set_params(cls, new_params):
    #         """Set class parameters
    #         """
    #
    #         for key in new_params:
    #             if key not in ('???', '???'):
    #                 raise KeyError('Invalid parameter name: ' + key)
    #
    #         for key in new_params:
    #             if not 0 <= new_params[key]:
    #                 raise ValueError('All parametervalues must be positiv')
    #             cls.key = new_params[key]
    #
    #         if 'eta' in new_params:
    #             if not new_params['eta'] <= 1:
    #                 raise ValueError('eta must be in [0, 1].')
    #             cls.eta = new_params['eta']
    #
    #         if 'DeltaPhiMax' in new_params:
    #             if not 0 < new_params['DeltaPhiMax']:
    #                 raise ValueError('DeltaPhiMax must be higher than 0')
    #             cls.DeltaPhiMax = new_params['DeltaPhiMax']
    #
    #     @classmethod
    #     def get_params(cls):
    #         """Get class parameters"""
    #         return {'F': cls.F, 'beta': cls.beta, 'phi_age': cls.phi_age, 'phi_weight': cls.phi_weight,
    #                 'a_half': cls.a_half, 'w_half': cls.w_half, 'zeta': cls.zigma, 'w_birth': cls.w_birth,
    #                 'sigma_birth': cls.sigma_birth, 'xi': cls.xi, 'gamma': cls.gamma, 'eta': cls.eta,
    #                 'omega': cls.omega}
    #         # mu skal også inn her når de beveger seg

    def set_landscape_parameters(self, landscape, params):
        """
        Set parameters for landscape type.

        :param landscape: String, code letter for landscape
        :param params: Dict with valid parameter specification for landscape
        """
        pass

    def plot_map(self):
        """
        Plots island map

        Code authored by: Hans Ekkehard Plesser
        """
        # #                   R    G    B
        rgb_value = {'W': (0.0, 0.0, 1.0),  # blue
                     'L': (0.0, 0.6, 0.0),  # dark green
                     'H': (0.5, 1.0, 0.5),  # light green
                     'D': (1.0, 1.0, 0.5)}  # light yellow

        map_rgb = [[rgb_value[column] for column in row]
                   for row in self.island_map.splitlines()]

        map = plt.figure()

        ax_im = map.add_axes([0.1, 0.1, 0.7, 0.8])  # llx, lly, w, h

        ax_im.imshow(map_rgb)

        ax_im.set_xticks(range(len(map_rgb[0])))
        ax_im.set_xticklabels(range(1, 1 + len(map_rgb[0])))
        ax_im.set_yticks(range(len(map_rgb)))
        ax_im.set_yticklabels(range(1, 1 + len(map_rgb)))

        ax_lg = map.add_axes([0.85, 0.1, 0.1, 0.8])  # llx, lly, w, h
        ax_lg.axis('off')
        for ix, name in enumerate(('Water', 'Lowland', 'Highland', 'Desert')):
            ax_lg.add_patch(plt.Rectangle((0., ix * 0.2), 0.3, 0.1, edgecolor='none', facecolor=rgb_value[name[0]]))
            ax_lg.text(0.35, ix * 0.2, name, transform=ax_lg.transAxes)

        plt.show()

    def simulate(self, num_years):
        """
        Run simulation while visualizing the result.

        :param num_years: number of years to simulate
        """
        self.plot_map()
        random.seed(self.seed)

        num_herbs = [len(self.herb)]
        num_carns = []
        num_years_list = list(range(self.years, self.years + num_years+1))
        field = self.island.animals_loc[self.coordinates[0]]

        for year in range(num_years):
            field.reset_fodder()
            field.eating_herbivores()
            field.eating_carnivores()
            field.breeding()
            # print(len(animals))
            field.aging_and_loosing_weight()
            field.dying()
            self.herb = field.herb
            self.carn = field.carn

            num_herbs.append(len(self.herb))
            num_carns.append(len(self.carn))
            print(len(self.herb), len(self.carn))

        plt.figure()
        plt.plot(num_years_list, num_herbs)
        plt.ylim(0, self.ymax_animals)
        plt.show()

        self.years += num_years


    def add_population(self, population):
        """
        Add a population to the island

        :param population: List of dictionaries specifying population
        """
        self.island.place_animals(population)


    # @property
    # def year(self):
    #     """Last year simulated."""
    #
    # @property
    # def num_animals(self):
    #     """Total number of animals on island."""
    #   num_animals = len(herb) + len(carn)
    #
    # @property
    # def num_animals_per_species(self):
    #     """Number of animals per species in island, as dictionary."""
    #   return num_animals_per_species = {'Herbivores': len(self.herb), 'Carnivore': len(self.carn)
    #
    # def make_movie(self):
    #     """Create MPEG4 movie from visualization images saved."""
