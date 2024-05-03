import matplotlib
matplotlib.use("Agg")
import matplotlib.backends.backend_agg as agg
import pylab
import numpy as np
import pygame


class Plotter:
    def __init__(self, t_max, FPS, position, size):
        self.t = np.zeros((t_max*FPS,1))
        self.e = np.zeros((t_max*FPS,1))

        self.fig = pylab.figure(figsize=[2, 2], # Inches
                        dpi=100,        # 100 dots per inch, so the resulting buffer is 400x400 pixels
                        )
        self.ax = self.fig.gca()

        self.position = position

    def update(self, screen, t, e):
        self.ax.plot(self.t, self.e)
        self.ax.grid('minor')
        
        canvas = agg.FigureCanvasAgg(self.fig)
        canvas.draw()
        renderer = canvas.get_renderer()
        raw_data = renderer.tostring_rgb()

        surf = pygame.image.fromstring(raw_data, (200, 200), "RGB")
        screen.blit(surf, self.position)