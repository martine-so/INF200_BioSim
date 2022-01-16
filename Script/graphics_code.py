"""
:mod:`randvis.graphics` provides graphics support for RandVis.

.. note::
   * This module requires the program ``ffmpeg`` or ``convert``
     available from `<https://ffmpeg.org>` and `<https://imagemagick.org>`.
   * You can also install ``ffmpeg`` using ``conda install ffmpeg``
   * You need to set the  :const:`_FFMPEG_BINARY` and :const:`_CONVERT_BINARY`
     constants below to the command required to invoke the programs
   * You need to set the :const:`_DEFAULT_FILEBASE` constant below to the
     directory and file-name start you want to use for the graphics output
     files.

"""

import matplotlib.pyplot as plt
import numpy as np
import subprocess
import os

# Update these variables to point to your ffmpeg and convert binaries
# If you installed ffmpeg using conda or installed both softwares in
# standard ways on your computer, no changes should be required.
_FFMPEG_BINARY = 'ffmpeg'
_MAGICK_BINARY = 'magick'

# update this to the directory and file-name beginning
# for the graphics files
_DEFAULT_GRAPHICS_DIR = os.path.join('../..', 'data')
_DEFAULT_GRAPHICS_NAME = 'dv'
_DEFAULT_IMG_FORMAT = 'png'
_DEFAULT_MOVIE_FORMAT = 'mp4'   # alternatives: mp4, gif


class Graphics:
    """Provides graphics support for RandVis."""

    def __init__(self, img_dir=None, img_name=None, img_fmt=None, island_map=None):
        """
        :param img_dir: directory for image files; no images if None
        :type img_dir: str
        :param img_name: beginning of name for image files
        :type img_name: str
        :param img_fmt: image file format suffix
        :type img_fmt: str
        """

        if img_name is None:
            img_name = _DEFAULT_GRAPHICS_NAME

        if img_dir is not None:
            self._img_base = os.path.join(img_dir, img_name)
        else:
            self._img_base = None

        self._img_fmt = img_fmt if img_fmt is not None else _DEFAULT_IMG_FORMAT

        self._img_ctr = 0
        self._img_year = 1

        # the following will be initialized by _setup_graphics
        self._fig = None
        self.island_map = island_map
        self._map_ax = None
        self._animals_graph_ax = None
        self._herb_graph_line = None
        self._carn_graph_line = None
        self._heatPlot_herb_ax = None
        self._img_heatPlot_herb_axis = None
        self._heatPlot_carn_ax = None
        self._img_heatPlot_carn_axis = None
        self._histAge_ax = None
        self._histWeight_ax = None
        self._histFitness_ax = None

    def update(self, hist_specs, year, cmax_herb, cmax_carn,
               island, numHerbs, numCarns):
        """
        Updates graphics with current data and save to file if necessary.

        :param hist_specs:
        :param year: current year
        :param cmax_herb:
        :param cmax_carn:
        :param island:
        :param numHerbs: array with numbers of herbivores in each island cell (2d array)
        :param numCarns: array with numbers of carnivores in each island cell (2d array)
        """
        herb_matrix, carn_matrix = island.matrix()
        age_herb, weight_herb, fitness_herb = island.age_fitness_weigth_herb()
        age_carn, weight_carn, fitness_carn = island.age_fitness_weigth_carn()

        self._update_heat_plot_herb(herb_matrix, cmax_herb)
        self._update_heat_plot_carn(carn_matrix, cmax_carn)
        self.count_plot(year)
        self._update_animal_graph(year, numHerbs, numCarns)
        self._update_hist_age(hist_specs, age_herb, age_carn)
        self._update_hist_weight(hist_specs, weight_herb, weight_carn)
        self._update_hist_fitness(hist_specs, fitness_herb, fitness_carn)
        self._fig.canvas.flush_events()  # ensure every thing is drawn
        plt.pause(1e-6)  # pause required to pass control to GUI

        self._save_graphics(year)

    def make_movie(self, movie_fmt=None):
        """
        Creates MPEG4 movie from visualization images saved.

        .. :note:
            Requires ffmpeg for MP4 and magick for GIF

        The movie is stored as img_base + movie_fmt

        Code authored by: Hans Ekkehard Plesser
        """

        if self._img_base is None:
            raise RuntimeError("No filename defined.")

        if movie_fmt is None:
            movie_fmt = _DEFAULT_MOVIE_FORMAT

        if movie_fmt == 'mp4':
            try:
                # Parameters chosen according to http://trac.ffmpeg.org/wiki/Encode/H.264,
                # section "Compatibility"
                subprocess.check_call([_FFMPEG_BINARY,
                                       '-i', '{}_%05d.png'.format(self._img_base),
                                       '-y',
                                       '-profile:v', 'baseline',
                                       '-level', '3.0',
                                       '-pix_fmt', 'yuv420p',
                                       '{}.{}'.format(self._img_base, movie_fmt)])
            except subprocess.CalledProcessError as err:
                raise RuntimeError('ERROR: ffmpeg failed with: {}'.format(err))
        elif movie_fmt == 'gif':
            try:
                subprocess.check_call([_MAGICK_BINARY,
                                       '-delay', '1',
                                       '-loop', '0',
                                       '{}_*.png'.format(self._img_base),
                                       '{}.{}'.format(self._img_base, movie_fmt)])
            except subprocess.CalledProcessError as err:
                raise RuntimeError('ERROR: convert failed with: {}'.format(err))
        else:
            raise ValueError('Unknown movie format: ' + movie_fmt)

    def setup(self, ymax_animals, final_year, img_step):
        """
        Prepare graphics.

        Call this before calling :meth:`update()` for the first time after
        the final time step has changed.

        :param ymax_animals: y-limit on animal count graph
        :param final_year: last time step to be visualised (upper limit of x-axis)
        :param img_step: interval between saving image to file
        """

        self._img_step = img_step
        plt.style.use('default')

        # create new figure window
        if self._fig is None:
            self._fig = plt.figure(figsize=(12,8))

            # axes for text
            axt = self._fig.add_axes([0.4, 0.8, 0.2, 0.2])  # llx, lly, w, h
            axt.axis('off')  # turn off coordinate system

            self.template = 'Year: {:5d}'
            self.txt = axt.text(0.5, 0.5, self.template.format(0),
                                horizontalalignment='center',
                                verticalalignment='center',
                                transform=axt.transAxes)  # relative coordinates


        # Add left subplot for images created with imshow().
        # We cannot create the actual ImageAxis object before we know
        # the size of the image, so we delay its creation.
        if self._map_ax is None:
            self._map_ax = self._fig.add_subplot(3, 3, 1)
            self._map_ax.title.set_text('Island')
            self._map_ax.axis('off')
            self._map_ax = self.plot_map(self._map_ax, self.island_map)


        # Add right subplot for line graph of mean.
        if self._animals_graph_ax is None:
            self._animals_graph_ax = self._fig.add_subplot(3, 3, 3)
            self._animals_graph_ax.title.set_text('Animal count')
            self._animals_graph_ax.set_xlim(0, final_year + 1)
            self._animals_graph_ax.set_ylim(0, ymax_animals)
        elif self._animals_graph_ax is not None:
            self._animals_graph_ax.set_xlim(0, final_year + 1)

        if self._heatPlot_herb_ax is None:
            self._heatPlot_herb_ax = self._fig.add_subplot(3, 2, 3)
            self._heatPlot_herb_ax.title.set_text('Herbivore distribution')
            self._img_heatPlot_herb_axis = None

        if self._heatPlot_carn_ax is None:
            self._heatPlot_carn_ax = self._fig.add_subplot(3, 2, 4)
            self._heatPlot_carn_ax.title.set_text('Carnivore distribution')
            self._img_heatPlot_herb_axis = None

        if self._histAge_ax is None:
            self._histAge_ax = self._fig.add_subplot(3, 3, 7)
            self._histAge_ax.title.set_text('Age')

        if self._histWeight_ax is None:
            self._histWeight_ax = self._fig.add_subplot(3, 3, 8)
            self._histWeight_ax.title.set_text('Weight')

        if self._histFitness_ax is None:
            self._histFitness_ax = self._fig.add_subplot(3, 3, 9)
            self._histFitness_ax.title.set_text('Fitness')

        plt.pause(0.01)  # pause required to make figure visible

        # needs updating on subsequent calls to simulate()
        # add 1 so we can show values for time zero and time final_step

        # self._animals_graph_ax.set_xlim(0, final_year+1)

        # Graph for Herbivores
        if self._herb_graph_line is None:
            herb_plot = self._animals_graph_ax.plot(np.arange(0, final_year+1),
                                           np.full(final_year+1, np.nan), label='Herbivores')
            self._herb_graph_line = herb_plot[0]
        else:
            x_data, y_data = self._herb_graph_line.get_data()
            x_new = np.arange(x_data[-1] + 1, final_year+1)
            if len(x_new) > 0:
                y_new = np.full(x_new.shape, np.nan)
                self._herb_graph_line.set_data(np.hstack((x_data, x_new)),
                                                np.hstack((y_data, y_new)))

        # Graph for Herbivores
        if self._carn_graph_line is None:
            carn_plot = self._animals_graph_ax.plot(np.arange(0, final_year + 1),
                                                       np.full(final_year + 1, np.nan), label='Carnivores')
            self._carn_graph_line = carn_plot[0]
        else:
            x_data, y_data = self._carn_graph_line.get_data()
            x_new = np.arange(x_data[-1] + 1, final_year + 1)
            if len(x_new) > 0:
                y_new = np.full(x_new.shape, np.nan)
                self._carn_graph_line.set_data(np.hstack((x_data, x_new)),
                                                  np.hstack((y_data, y_new)))

    def count_plot(self, year):
        self.txt.set_text(self.template.format(year))
        plt.pause(0.1)  # pause required to make update visible
        #
        # plt.show()

    def plot_map(self, subplot, island_map):
        """
        Plots island map

        Code authored by: Hans Ekkehard Plesser

        :param subplot: subplot to plot map in
        :param island_map: ...
        """
        # #                   R    G    B
        rgb_value = {'W': (0.0, 0.0, 1.0),  # blue
                     'L': (0.0, 0.6, 0.0),  # dark green
                     'H': (0.5, 1.0, 0.5),  # light green
                     'D': (1.0, 1.0, 0.5)}  # light yellow

        map_rgb = [[rgb_value[column] for column in row]
                   for row in island_map.splitlines()]

        ax_im = subplot.inset_axes([0.1, 0.1, 0.7, 0.8])  # llx, lly, w, h

        ax_im.imshow(map_rgb)

        ax_im.set_xticks(range(len(map_rgb[0])))
        ax_im.set_xticklabels(range(1, 1 + len(map_rgb[0])))
        ax_im.set_yticks(range(len(map_rgb)))
        ax_im.set_yticklabels(range(1, 1 + len(map_rgb)))

        ax_lg = subplot.inset_axes([0.85, 0.1, 0.1, 0.8])  # llx, lly, w, h
        ax_lg.axis('off')
        for ix, name in enumerate(('Water', 'Lowland', 'Highland', 'Desert')):
            ax_lg.add_patch(plt.Rectangle((0., ix * 0.2), 0.3, 0.1, edgecolor='none', facecolor=rgb_value[name[0]]))
            ax_lg.text(0.35, ix * 0.2, name, transform=ax_lg.transAxes)

    def _update_heat_plot_herb(self, herb_matrix, cmax):
        """
        Update heat plot for herbivores

        :param herb_matrix: ...
        :param cmax: ...
        """
        if self._img_heatPlot_herb_axis is not None:
            self._img_heatPlot_herb_axis.set_data(herb_matrix)
        else:
            self._img_heatPlot_herb_axis = self._heatPlot_herb_ax.imshow(herb_matrix,
                                                                         interpolation='nearest',
                                                                         vmin=0, vmax=cmax)
            plt.colorbar(self._img_heatPlot_herb_axis, ax=self._heatPlot_herb_ax,
                         orientation='vertical')

    def _update_heat_plot_carn(self, carn_matrix, cmax):
        """
        Updates heat plot for carnivores
        :param carn_matrix: ...
        :param cmax: ...
        """
        if self._img_heatPlot_carn_axis is not None:
            self._img_heatPlot_carn_axis.set_data(carn_matrix)
        else:
            self._img_heatPlot_carn_axis = self._heatPlot_carn_ax.imshow(carn_matrix,
                                                                         interpolation='nearest',
                                                                         vmin=0, vmax=cmax)
            plt.colorbar(self._img_heatPlot_carn_axis, ax=self._heatPlot_carn_ax,
                         orientation='vertical')

    def _update_animal_graph(self, year, numHerbs, numCarns):
        y_data_herb = self._herb_graph_line.get_ydata()
        y_data_herb[year] = numHerbs
        self._herb_graph_line.set_ydata(y_data_herb)

        y_data_carn = self._carn_graph_line.get_ydata()
        y_data_carn[year] = numCarns
        self._carn_graph_line.set_ydata(y_data_carn)

    def _update_hist_age(self, hist_specs, age_herb, age_carn):
        self._histAge_ax.clear()
        self._histAge_ax.title.set_text('Age')
        if 'age' in hist_specs:
            x_lim = hist_specs['age']['max']
            width = hist_specs['age']['delta']
        else:
            x_lim = 40
            width = 2

        n = int(x_lim / width)
        # Herbs:
        self._histAge_ax.set_xlim(0, x_lim)
        self._histAge_ax.hist(age_herb, n, label='Herbivores', histtype='step')
        # Carns
        self._histAge_ax.hist(age_carn, n,  label='Carnivores', histtype='step')

    def _update_hist_weight(self, hist_specs, weight_herb, weight_carn):
        self._histWeight_ax.clear()
        self._histWeight_ax.title.set_text('Weight')
        if 'weight' in hist_specs:
            x_lim = hist_specs['weight']['max']
            width = hist_specs['weight']['delta']
        else:
            x_lim = 100
            width = 2

        n = int(x_lim/width)
        # Herbs:
        self._histWeight_ax.set_xlim(0, x_lim)
        self._histWeight_ax.hist(weight_herb, n, label='Herbivores', histtype='step')
        # Carns
        self._histWeight_ax.hist(weight_carn, n, label='Carnivores', histtype='step')

    def _update_hist_fitness(self, hist_specs, fitness_herb, fitness_carn):
        self._histFitness_ax.clear()
        self._histFitness_ax.title.set_text('Fitness')
        if 'fitness' in hist_specs:
            x_lim = hist_specs['fitness']['max']
            width = hist_specs['fitness']['delta']
        else:
            x_lim = 1
            width = 0.05

        n = int(x_lim / width)

        # Herbs:
        self._histFitness_ax.set_xlim(0, x_lim)
        self._histFitness_ax.hist(fitness_herb, n, label='Herbivores', histtype='step')
        # Carns
        self._histFitness_ax.hist(fitness_carn, n,  label='Carnivores', histtype='step')
        self._histFitness_ax.legend(loc='best', bbox_to_anchor=(1, 0.5), title='Animal',
                                    fancybox=True, shadow=True)

    def _save_graphics(self, year):
        """
        Saves graphics to file if file name given.
        Code authored by: Hans Ekkehard Plesser

        :param:
        """

        if self._img_base is None or year % self._img_year != 0:
            return

        plt.savefig('{base}_{num:05d}.{type}'.format(base=self._img_base,
                                                     num=self._img_ctr,
                                                     type=self._img_fmt))
        self._img_ctr += 1
