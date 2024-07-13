import pygame
import numpy as np
from physics_model import ComputeCart
from control import PIDController
from draw_cart import DrawCart
from plotter import Plotter

# Initialize pygame
pygame.init()

# Colors
BLACK = (0, 0, 0)

# Initialize the clock
clock = pygame.time.Clock()

# Screen dimensions
WIDTH, HEIGHT = 800, 400
WIDTH_METERS = 5

# Plot dimensions
PLOT_WIDTH, PLOT_HEIGHT = 0, 0
PLOT1_POSITION = (WIDTH, 0)

FPS = 50 # Target FPS

# Cart parameters with respect to screen
cart_width = 50
cart_height = 30
# Physics parameters
m = 10 # Cart mass
F = 10.0  # Disturbance force when arrows are pressed
b = 10 # Friction coefficient

# Velocity to change the parameters
Kp_gain = 5/FPS
Ki_gain = 0.5/FPS
Kd_gain = 2/FPS

# Initial condition
x0 = np.array([0, WIDTH_METERS/2])
# Cart model initialization
Cart = ComputeCart(WIDTH, WIDTH_METERS, cart_width, b, m, 1/FPS, x0)

# SP initial value
SP = WIDTH_METERS/2

# Controller initialization
Controller = PIDController(0, 0, 0, SP, 1/FPS)

# Set up the display
screen = pygame.display.set_mode((WIDTH+PLOT_WIDTH, HEIGHT))
pygame.display.set_caption("Cart position control")

# # Configure the plotters
# count_plot = 0
# n_to_update = 0.2/(1/FPS) # update plot each 0.2 seconds
# Plot1 = Plotter(screen, 2, 2, PLOT1_POSITION)

# Drawings initialization
CartDrawings = DrawCart(screen, WIDTH_METERS, WIDTH, HEIGHT, cart_width, cart_height)

u = np.array([0])  # No force initially
d = np.array([0])  # No disturbance initially
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                d = np.array([-F])  # Apply left force
            elif event.key == pygame.K_RIGHT:
                d = np.array([F])   # Apply right force
            elif event.key == pygame.K_d:
                SP = SP + 0.5
            elif event.key == pygame.K_a:
                SP = SP - 0.5
        elif event.type == pygame.KEYUP:
            if event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                d = np.array([0])  # Remove force
        
    keys = pygame.key.get_pressed()
    if keys[pygame.K_p]:  # Example with left arrow key
        Controller.update_parameters(Controller.Kp + Kp_gain, Controller.Ki, Controller.Kd)
    if keys[pygame.K_o]: 
        if (Controller.Kp - Kp_gain) > 0:
                    Controller.update_parameters(Controller.Kp - Kp_gain, Controller.Ki, Controller.Kd)
        else:
            Controller.update_parameters(0.0, Controller.Ki, Controller.Kd)
    if keys[pygame.K_l]:
        Controller.update_parameters(Controller.Kp, Controller.Ki + Ki_gain, Controller.Kd)
    if keys[pygame.K_k]:
        if (Controller.Ki - Ki_gain) > 0:
            Controller.update_parameters(Controller.Kp, Controller.Ki - Ki_gain, Controller.Kd)
        else:
            Controller.update_parameters(Controller.Kp, 0.0, Controller.Kd)
    if keys[pygame.K_m]:
        Controller.update_parameters(Controller.Kp, Controller.Ki, Controller.Kd + Kd_gain)
    if keys[pygame.K_n]:
        if (Controller.Kd - Kd_gain) > 0:
            Controller.update_parameters(Controller.Kp, Controller.Ki, Controller.Kd - Kd_gain)
        else:
            Controller.update_parameters(Controller.Kp, Controller.Ki, 0.0)          

    # Maximum FPS and dt are the period between two calls from pygame
    # Calculate the actual dt from simulation
    dt = clock.tick(FPS)/1000
    
    # Compute the cart 
    Cart.compute_cart_state(u, d)
    
    # Compute the control action
    u = Controller.update_output(SP, Cart.x)

    screen.fill(BLACK)

    # if count_plot <= n_to_update:
    #     count_plot = count_plot + 1
    # else:
    #     Plot1.plot_data(np.array([0, 1]), np.array([1, 1]))
    #     count_plot = 0

    CartDrawings.draw(SP, Cart, Controller, d)
    CartDrawings.print_info(Cart, Controller, d, dt)
 
    pygame.display.flip()

pygame.quit()
