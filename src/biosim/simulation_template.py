"""
Template for BioSim class.
"""

# The material in this file is licensed under the BSD 3-clause license
# https://opensource.org/licenses/BSD-3-Clause
# (C) Copyright 2021 Hans Ekkehard Plesser / NMBU

class BioSim:
    def __init__(self, island_map, ini_pop, seed,
                 vis_years=1, ymax_animals=None, cmax_animals=None, hist_specs=None,
                 img_dir=None, img_base=None, img_fmt='png', img_years=None,
                 log_file=None):

        self.island_map = island_map
        self.ini_pop = ini_pop
        self.seed = seed
        self.vis_years = vis_years
        self.ymax_animals = ymax_animals
        self.cmax_aminals = cmax_animals
        self.hist_specs = hist_specs
        self.img_dir = img_dir
        self.img_base = img_base
        self.img_fmt = img_fmt
        self.img_years = img_years
        self.log_file = log_file

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

    def set_animal_parameters(self, species, params):
        """
        Set parameters for animal species.

        :param species: String, name of animal species
        :param params: Dict with valid parameter specification for species
        """

        @classmethod
        def set_params(cls, new_params):
            """Set class parameters
            """

            for key in new_params:
                if key not in ('???', '???'):
                    raise KeyError('Invalid parameter name: ' + key)

            for key in new_params:
                if not 0 <= new_params[key]:
                    raise ValueError('All parametervalues must be positiv')
                cls.key = new_params[key]

            if 'eta' in new_params:
                if not new_params['eta'] <= 1:
                    raise ValueError('eta must be in [0, 1].')
                cls.eta = new_params['eta']

            if 'DeltaPhiMax' in new_params:
                if not 0 < new_params['DeltaPhiMax']:
                    raise ValueError('DeltaPhiMax must be higher than 0')
                cls.DeltaPhiMax = new_params['DeltaPhiMax']

        @classmethod
        def get_params(cls):
            """Get class parameters"""
            return {'F': cls.F, 'beta': cls.beta, 'phi_age': cls.phi_age, 'phi_weight': cls.phi_weight,
                    'a_half': cls.a_half, 'w_half': cls.w_half, 'zeta': cls.zigma, 'w_birth': cls.w_birth,
                    'sigma_birth': cls.sigma_birth, 'xi': cls.xi, 'gamma': cls.gamma, 'eta': cls.eta,
                    'omega': cls.omega}
            # mu skal også inn her når de beveger seg

    def set_landscape_parameters(self, landscape, params):
        """
        Set parameters for landscape type.

        :param landscape: String, code letter for landscape
        :param params: Dict with valid parameter specification for landscape
        """

    def simulate(self, num_years):
        """
        Run simulation while visualizing the result.

        :param num_years: number of years to simulate
        """

    def add_population(self, population):
        """
        Add a population to the island

        :param population: List of dictionaries specifying population
        """

    @property
    def year(self):
        """Last year simulated."""

    @property
    def num_animals(self):
        """Total number of animals on island."""

    @property
    def num_animals_per_species(self):
        """Number of animals per species in island, as dictionary."""

    def make_movie(self):
        """Create MPEG4 movie from visualization images saved."""
