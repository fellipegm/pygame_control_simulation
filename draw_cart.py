import pygame
from pygame.locals import *

import numpy as np

from helpers import draw_dotted_line, draw_horizontal_arrow, draw_pid_arrows, PROP_COEFF



class DrawCart:
    def __init__(self, screen, WIDTH_METERS, WIDTH, HEIGHT, cart_width, cart_height):
        self.screen = screen
        self.WIDTH_METERS = WIDTH_METERS
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        self.cart_width = cart_width
        self.cart_height = cart_height

        # Colors
        self.WHITE = (255, 255, 255)
        self.REFERENCE_COLOR = (200, 0, 0)
        self.CART_WHEEL_COLOR = (111, 0, 188)
        self.CART_COLOR = (47, 178, 255)

        # Initialize the font module
        pygame.font.init()

        # Choose a font (default pygame font here, size 24)
        self.font = pygame.font.Font(None, 24)

    def draw(self, SP, Cart, Controller, d):
        # Method code here
        # Draw cart
        cart_x = int(Cart.x/self.WIDTH_METERS * self.WIDTH)
        cart_y = self.HEIGHT // 1.2

        # Draw line above cart
        draw_dotted_line(self.screen, self.WHITE, 
                            (cart_x, cart_y), 
                            (cart_x, cart_y-90))
        pos = self.font.render(f"x = {Cart.x:.2f} m, v = {Cart.dx:0.2f} m/s", True, (255, 255, 255))
        self.screen.blit(pos, (cart_x, cart_y-90-15))

        # Draw reference line
        ref_x = SP/self.WIDTH_METERS * self.WIDTH # x position of SP line
        ref_y_start = self.HEIGHT // 1.2 # y start position of SP line
        ref_y_end = self.HEIGHT // 1.2  - 150  # y end position of SP line
        draw_dotted_line(self.screen, self.REFERENCE_COLOR, 
                            (ref_x, ref_y_start), 
                            (ref_x, ref_y_end))
        ref_display = self.font.render(f"SP = {SP:.2f} m", True, (255, 255, 255))
        self.screen.blit(ref_display, (ref_x, ref_y_end-15))

        # Cart wheels (you can adjust the size and positions if needed)
        wheel_radius = 6
        left_wheel_center = (cart_x + self.cart_width // 5, cart_y + self.cart_height)
        right_wheel_center = (cart_x + self.cart_width*4 // 5, cart_y + self.cart_height)
        pygame.draw.circle(self.screen, self.CART_WHEEL_COLOR, left_wheel_center, wheel_radius)
        pygame.draw.circle(self.screen, self.CART_WHEEL_COLOR, right_wheel_center, wheel_radius)

        # Cart base
        pygame.draw.rect(self.screen, self.CART_COLOR, (cart_x, cart_y, self.cart_width, self.cart_height))

        if np.sign(d[0]) > 0:
            draw_horizontal_arrow(self.screen, (255, 0, 10), 
                                    (cart_x+self.cart_width, cart_y+self.cart_height//2),
                                    (cart_x+self.cart_width+d[0]*PROP_COEFF, cart_y+self.cart_height//2))
        else:
            draw_horizontal_arrow(self.screen, (255, 0, 10), 
                                    (cart_x, cart_y+self.cart_height//2),
                                    (cart_x+d[0]*PROP_COEFF, cart_y+self.cart_height//2))
        # Draw the track
        track_y = cart_y + self.cart_height + wheel_radius # Same y-coordinate as the cart 
        pygame.draw.line(self.screen, self.WHITE, 
                            (0, track_y + int(self.HEIGHT-track_y)//2), 
                            (self.WIDTH, track_y + int(self.HEIGHT-track_y)//2), 
                            int(self.HEIGHT-track_y))
            

        draw_pid_arrows(self.screen, cart_x, cart_y - 90, Controller.P, Controller.I, Controller.D)

    def print_info(self, Cart, Controller, d, dt):
        # Render important variables
        timestep = self.font.render(f"dt = {dt:.2f} s", True, (255, 255, 255))
        acc = self.font.render(f"a = {Cart.ddx:.2f} m/s2", True, (255, 255, 255))
        PID = self.font.render(f"PID = {Controller.output:.2f} N", True, (255, 255, 255))
        error = self.font.render(f"e = {Controller.error:.2f} m", True, (255, 255, 255))
        dist = self.font.render(f"dist = {d[0]:.2f} N", True, (255, 255, 255))
        self.screen.blit(timestep, (10, 10))
        self.screen.blit(acc, (10, 30))
        self.screen.blit(PID, (10, 50))
        self.screen.blit(error, (10, 70))
        self.screen.blit(dist, (10, 90))

        Cont_text = self.font.render("Controller Parameters:", True, (255, 255, 255))
        Kp_text = self.font.render(f"Kp = {Controller.Kp:.2f}", True, (255, 255, 255))
        Ki_text = self.font.render(f"Ki = {Controller.Ki:.2f}", True, (255, 255, 255))
        Kd_text = self.font.render(f"Kd = {Controller.Kd:.2f}", True, (255, 255, 255))
        self.screen.blit(Cont_text, (150, 10))
        self.screen.blit(Kp_text, (150, 30))
        self.screen.blit(Ki_text, (150, 50))
        self.screen.blit(Kd_text, (150, 70))

        alt_sp_text = self.font.render("a: decrease SP,   d: increase SP", True, (255, 255, 255))
        alt_pert_text = self.font.render("<-: pert. p/ esquerda,   ->: pert. p/ direita", True, (255, 255, 255))
        alt_p_text = self.font.render("p: increase Kp,   o: decrease Kp", True, (255, 255, 255))
        alt_i_text = self.font.render("l: increase Ki,   k: decrease Ki", True, (255, 255, 255))
        alt_d_text = self.font.render("m: increase Kd,   n: decrease Kd", True, (255, 255, 255))
        self.screen.blit(alt_sp_text, (400, 10))
        self.screen.blit(alt_pert_text, (400, 30))
        self.screen.blit(alt_p_text, (400, 50))
        self.screen.blit(alt_i_text, (400, 70))
        self.screen.blit(alt_d_text, (400, 90))