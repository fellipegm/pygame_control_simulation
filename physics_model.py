import numpy as np


class ComputeCart:
    def __init__(self, WIDTH, WIDTH_METERS, cart_width, b, m, dt, x0):
        self.WIDTH = WIDTH
        self.WIDTH_METERS = WIDTH_METERS
        self.cart_width = cart_width
        self.dot_x = np.array([0, 0]) # [ddx, dx]
        self.x = x0[1]
        self.dx = x0[0]
        self.ddx = 0
        self.b = b
        self.m = m
        self.dt = dt

    # Computes the dx and x in a vector
    def compute_cart_state(self, u, d):
        # Friction force
        Fat = self.b*self.dx
        # Acceleration
        self.ddx = (d[0] + u[0] - Fat)/self.m
        # Velocity
        self.dx = self.dx + self.ddx*self.dt
        # Integrate de acceleration
        self.x = self.x + self.dx*self.dt
        # Limites da tela
        if (self.x < 0):
            self.dx = -self.dx*self.m*0.05
            self.x = 0
        elif (self.x > self.WIDTH_METERS - self.cart_width/self.WIDTH*self.WIDTH_METERS):
            self.dx = -self.dx*self.m*0.05
            self.x = self.WIDTH_METERS - self.cart_width/self.WIDTH*self.WIDTH_METERS