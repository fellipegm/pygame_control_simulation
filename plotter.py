import matplotlib
matplotlib.use("Agg")
import matplotlib.backends.backend_agg as agg
import pylab
import numpy as np
import pygame


class Plotter:
    """Class to plot data in pygame canvas"""
    def __init__(self, screen, width, height, position, n_update):
        """Args:
            screen (pyplot screen): screen to plot
            width (int): width of the plot
            height (int): height of the plot
            position (int,int): position of the plot
        """
        self.screen = screen
        self.width = width
        self.height = height
        self.position = position
        self.n_update = n_update

    def plot_data(self, x, y):
        """Plot data from two numpy arrays
        Args:
            x (numpy float array): x axis data
            y (numpy float array): y axis data
        """
        fig = pylab.figure(figsize=(self.width, self.height), dpi=20)
        canvas = agg.FigureCanvasAgg(fig)
        ax = fig.add_subplot(111)
        ax.plot(x, y)
        canvas.draw()
        renderer = canvas.get_renderer()
        raw_data = renderer.tostring_rgb()
        size = canvas.get_width_height()
        pylab.close()
        plot_surface = pygame.image.fromstring(raw_data, size, "RGB")
        self.screen.blit(plot_surface, self.position)