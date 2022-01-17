"""
Template for BioSim class.
"""

# The material in this file is licensed under the BSD 3-clause license
# https://opensource.org/licenses/BSD-3-Clause
# (C) Copyright 2021 Hans Ekkehard Plesser / NMBU
from biosim.island_class import Island
from biosim.animals_class import Herbivore, Carnivore
from biosim.landscape_class import Lowland, Highland, Desert
from biosim.graphics_code import Graphics


class BioSim:
    def __init__(self, island_map, ini_pop, seed,
                 vis_years=1, ymax_animals=None, cmax_animals=None, hist_specs=None,
                 img_dir=None, img_base=None, img_fmt='png', img_years=None,
                 log_file=None):

        row_len = len(island_map.split()[0])
        for row in island_map.split():
            if len(row) != row_len:
                raise ValueError('Inconsistent length on map rows')
            for col in row:
                if col not in {'L', 'W', 'D', 'H'}:
                    raise ValueError('Invalid landscape type')
            if row[0] != 'W'  and row[-1] != 'W':
                raise ValueError('Boundary must be W')
        for col in island_map.split()[0]:
            if col != 'W':
                raise ValueError('Boundary must be W')
        for col in island_map.split()[-1]:
            if col != 'W':
                raise ValueError('Boundary must be W')


        self.island_map = island_map        # In use on graph
        self.ini_pop = ini_pop              # In use on graph
        self.seed = seed                    # In use on graph
        self.vis_years = vis_years
        self.img_dir = img_dir
        self.img_base = img_base
        self.img_fmt = img_fmt
        self.img_years = img_years
        self.log_file = log_file
        self.hist_specs = hist_specs

        self.cmax_herb = 200
        self.cmax_carn = 50
        if cmax_animals is not None:
            if 'Herbivore' in cmax_animals:
                self.cmax_herb = cmax_animals['Herbivore']
            if 'Carnivore' in cmax_animals:
                self.cmax_carn = cmax_animals['Carnivore']

        self.years = 0
        self._final_year = 0
        self.herb = []
        self.carn = []

        if ymax_animals is None:
            self.ymax_animals = 6000
        else:
            self.ymax_animals = ymax_animals  # In use on graph

        self._graphics = Graphics(img_dir=self.img_dir, img_fmt=self.img_fmt, island_map=self.island_map)
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

    def set_animal_parameters(self, species, params):
        """
        Set parameters for animal species.

        :param species: String, name of animal species
        :param params: Dict with valid parameter specification for species
        """

        if species == 'Herbivore':
            Herbivore.set_params(params)
        elif species == 'Carnivore':
            Carnivore.set_params(params)


    def set_landscape_parameters(self, landscape, params):
        """
        Set parameters for landscape type.

        :param landscape: String, code letter for landscape
        :param params: Dict with valid parameter specification for landscape
        """
        if landscape == 'L':
            Lowland.set_params(params)
        elif landscape == 'H':
            Highland.set_params(params)
        elif landscape == 'D':
            Desert.set_params(params)



    def num_animals_plot(self):
        numHerbs = 0
        numCarns = 0
        for loc in self.island.animals_loc:
            numCarns += len(self.island.animals_loc[loc].carn)
            numHerbs += len(self.island.animals_loc[loc].herb)

        return numHerbs, numCarns

    def simulate(self, num_years):
        """
        Run simulation while visualizing the result.

        :param num_years: number of years to simulate
        """
        self._final_year = self.years + num_years
        if self.vis_years > 0:
            if self.img_years is None:
                self.img_years = self.vis_years

            if self.img_years % self.vis_years != 0:
                raise ValueError('img_steps must be multiple of vis_steps')

            self._graphics.setup(self.ymax_animals, self._final_year, self.img_years)

            while self.years < self._final_year:
                self.island.one_year()
                self.years += 1
                numHerbs, numCarns = self.num_animals_plot()

                if self.years % self.vis_years == 0:
                    self._graphics.update(self.hist_specs, self.years, self.cmax_herb, self.cmax_carn,
                                          self.island, numHerbs, numCarns, self.vis_years)
        else:
            while self.years < self._final_year:
                self.island.one_year()
                self.years += 1

    def add_population(self, population):
        """
        Add a population to the island

        :param population: List of dictionaries specifying population
        """
        self.island.place_animals(population)


    @property
    def year(self):
        """Last year simulated."""
        return self._final_year

    @property
    def num_animals(self):
        """Total number of animals on island."""
        numHerbs, numCarns = self.num_animals_plot()
        return numHerbs + numCarns

    @property
    def num_animals_per_species(self):
        """Number of animals per species in island, as dictionary."""
        numHerbs, numCarns = self.num_animals_plot()
        return {'Herbivore': numHerbs, 'Carnivore': numCarns}

    def make_movie(self):
        """
                Creates MPEG4 movie from visualization images saved.

                .. :note:
                    Requires ffmpeg for MP4 and magick for GIF

                The movie is stored as img_base + movie_fmt.
                """

        self._graphics.make_movie()
