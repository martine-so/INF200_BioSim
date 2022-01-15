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

    def __init__(self, img_dir=None, img_name=None, img_fmt=None):
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
        self._img_step = 1

        # the following will be initialized by _setup_graphics
        self._fig = None
        self._map_ax = None
        self._animals_graph_ax = None
        self._animals_graph_line = None
        self._heatPlot_herb_ax = None
        self._img_heatPlot_herb_axis = None
        self._heatPlot_carn_ax = None
        self._img_heatPlot_carn_axis = None
        self._histAge_ax = None
        self._histWeight_ax = None
        self._histFitness_ax = None

    def update(self, step, sys_map, sys_mean):
        """
        Updates graphics with current data and save to file if necessary.

        :param step: current time step
        :param sys_map: current system status (2d array)
        :param sys_mean: current mean value of system
        """

        self._update_heat_plot_herb(...)
        self._update_heat_plot_carn(...)
        self.count_plot(...)
        self._update_animal_graph(step, sys_mean)
        self._update_hist_age(...)
        self._update_hist_weight(...)
        self._update_hist_fitness(...)
        self._fig.canvas.flush_events()  # ensure every thing is drawn
        plt.pause(1e-6)  # pause required to pass control to GUI

        self._save_graphics(step)

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

    def setup(self, final_step, img_step):
        """
        Prepare graphics.

        Call this before calling :meth:`update()` for the first time after
        the final time step has changed.

        :param final_step: last time step to be visualised (upper limit of x-axis)
        :param img_step: interval between saving image to file
        """

        self._img_step = img_step

        # create new figure window
        if self._fig is None:
            self._fig = plt.figure()

        # Add left subplot for images created with imshow().
        # We cannot create the actual ImageAxis object before we know
        # the size of the image, so we delay its creation.
        if self._map_ax is None:
            self._map_ax = self._fig.add_subplot(3, 3, 1)
            self._map_ax.plot_map(self._map_ax, map)  # MÅ LEGGE TIL MAPPET HER!!!!

        # Add right subplot for line graph of mean.
        if self._animals_graph_ax is None:
            self._animals_graph_ax = self._fig.add_subplot(3, 3, 3)
            # self._animals_graph_ax.set_ylim(-0.05, 0.05)

        if self._heatPlot_herb_ax is None:
            self._heatPlot_herb_ax = self._fig.add_subplot(3, 3, 4)
            self._img_heatPlot_herb_axis = None

        if self._heatPlot_carn_ax is None:
            self._heatPlot_carn_ax = self._fig.add_subplot(3, 3, 6)
            self._img_heatPlot_herb_axis = None

        if self._histAge_ax is None:
            self._histAge_ax = self._fig.add_subplot(3, 3, 7)

        if self._histWeight_ax is None:
            self._histWeight_ax = self._fig.add_subplot(3, 3, 8)

        if self._histFitness_ax is None:
            self._histFitness_ax = self._fig.add_subplot(3, 3, 9)

        # needs updating on subsequent calls to simulate()
        # add 1 so we can show values for time zero and time final_step

        # self._animals_graph_ax.set_xlim(0, final_step+1)
        #
        # if self._animals_graph_line is None:
        #     animals_plot = self._animals_graph_ax.plot(np.arange(0, final_step+1),
        #                                    np.full(final_step+1, np.nan))
        #     self._animals_graph_line = animals_plot[0]
        # else:
        #     x_data, y_data = self._animals_graph_line.get_data()
        #     x_new = np.arange(x_data[-1] + 1, final_step+1)
        #     if len(x_new) > 0:
        #         y_new = np.full(x_new.shape, np.nan)
        #         self._animals_graph_line.set_data(np.hstack((x_data, x_new)),
        #                                  np.hstack((y_data, y_new)))

    def count_plot(self):
        # axes for text
        axt = self._fig.add_axes([0.4, 0.8, 0.2, 0.2])  # llx, lly, w, h
        axt.axis('off')  # turn off coordinate system

        template = 'Count: {:5d}'
        txt = axt.text(0.5, 0.5, template.format(0),
                       horizontalalignment='center',
                       verticalalignment='center',
                       transform=axt.transAxes)  # relative coordinates

        plt.pause(0.01)  # pause required to make figure visible

        # for k in range(years):
        #     txt.set_text(template.format(k))
        #     plt.pause(0.1)  # pause required to make update visible
        #
        # plt.show()

    def plot_map(self, plot, island_map):
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
                   for row in island_map.splitlines()]

        ax_im = plot.inset_axes([0.1, 0.1, 0.7, 0.8])  # llx, lly, w, h

        ax_im.imshow(map_rgb)

        ax_im.set_xticks(range(len(map_rgb[0])))
        ax_im.set_xticklabels(range(1, 1 + len(map_rgb[0])))
        ax_im.set_yticks(range(len(map_rgb)))
        ax_im.set_yticklabels(range(1, 1 + len(map_rgb)))

        ax_lg = plot.inset_axes([0.85, 0.1, 0.1, 0.8])  # llx, lly, w, h
        ax_lg.axis('off')
        for ix, name in enumerate(('Water', 'Lowland', 'Highland', 'Desert')):
            ax_lg.add_patch(plt.Rectangle((0., ix * 0.2), 0.3, 0.1, edgecolor='none', facecolor=rgb_value[name[0]]))
            ax_lg.text(0.35, ix * 0.2, name, transform=ax_lg.transAxes)

    def _update_heat_plot_herb(self, sys_map):
        """
        Update heat plot for herbivores

        :param sys_map: ...
        """
        if self._img_heatPlot_herb_axis is not None:
            self._img_heatPlot_herb_axis.set_data(sys_map)
        else:
            self._img_heatPlot_herb_axis = self._heatPlot_herb_ax.imshow(sys_map,
                                                                         interpolation='nearest',
                                                                         vmin=-0.25, vmax=0.25)
            plt.colorbar(self._img_heatPlot_herb_axis, ax=self._heatPlot_herb_ax,
                         orientation='horisontal')

        # if self._img_axis is not None:
        #     self._img_axis.set_data(sys_map)
        # else:
        #     self._img_axis = self._map_ax.imshow(sys_map,
        #                                          interpolation='nearest',
        #                                          vmin=-0.25, vmax=0.25)
        #     plt.colorbar(self._img_axis, ax=self._map_ax,
        #                  orientation='horizontal')

    def _update_heat_plot_carn(self, sys_map):
        """
        Updates heat plot for carnivores
        :param sys_map: ...
        """
        if self._img_heatPlot_carn_axis is not None:
            self._img_heatPlot_carn_axis.set_data(sys_map)
        else:
            self._img_heatPlot_carn_axis = self._heatPlot_carn_ax.imshow(sys_map,
                                                                         interpolation='nearest',
                                                                         vmin=-0.25, vmax=0.25)
            plt.colorbar(self._img_heatPlot_carn_axis, ax=self._heatPlot_carn_ax,
                         orientation='horisontal')

        # if self._img_axis is not None:
        #     self._img_axis.set_data(sys_map)
        # else:
        #     self._img_axis = self._map_ax.imshow(sys_map,
        #                                          interpolation='nearest',
        #                                          vmin=-0.25, vmax=0.25)
        #     plt.colorbar(self._img_axis, ax=self._map_ax,
        #                  orientation='horizontal')

    def _update_animal_graph(self, step, mean):
        pass
        # y_data = self._animals_graph_line.get_ydata()
        # y_data[step] = mean
        # self._animals_graph_line.set_ydata(y_data)

    def _update_hist_age(self):
        pass

    def _update_hist_weight(self):
        pass

    def _update_hist_fitness(self):
        pass

    def _save_graphics(self, step):
        """
        Saves graphics to file if file name given.
        Code authored by: Hans Ekkehard Plesser
        """

        if self._img_base is None or step % self._img_step != 0:
            return

        plt.savefig('{base}_{num:05d}.{type}'.format(base=self._img_base,
                                                     num=self._img_ctr,
                                                     type=self._img_fmt))
        self._img_ctr += 1
