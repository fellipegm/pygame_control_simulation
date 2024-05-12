import pygame
from pygame.locals import *
import numpy as np
from helpers import draw_dotted_line, draw_horizontal_arrow, draw_pid_arrows, PROP_COEFF
from control import PIDController

# Initialize pygame
pygame.init()

# Colors
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
CART_COLOR = (47, 178, 255)
CART_WHEEL_COLOR = (111, 0, 188)
LIGHT_GRAY = (230, 230, 230)
WHITE = (255, 255, 255)
ARROW_COLOR = (255, 50, 50)
REFERENCE_COLOR = (200, 0, 0)


# Initialize the font module
pygame.font.init()

# Choose a font (default pygame font here, size 24)
font = pygame.font.Font(None, 24)

# Initialize the clock
clock = pygame.time.Clock()

# Screen dimensions
WIDTH, HEIGHT = 800, 400
PLOT_WIDTH = 400
LARGURA, ALTURA = 5, 1

MAX_ARROW_LENGTH = 100

ARROW_THICKNESS = 3
ARROWHEAD_SIZE = 10

FPS = 50


# Parâmetros do carrinho
cart_width = 50
cart_height = 30
m = 10
F = 10.0  # Disturbance force when arrows are pressed
b = 10

Kp_gain = 5/FPS
Ki_gain = 0.5/FPS
Kd_gain = 2/FPS




# Computa a aceleração
def compute_ddot_x(x, u, d):
    dx = x[0]
    
    # Força de atrito
    Fat = b*dx
    ddx = (d[0] + u[0] - Fat)/m
    
    return np.array([ddx, dx])



# Initial condition
x = np.array([0, LARGURA/2])
# Reference value
ref = LARGURA/2

Controller = PIDController(0, 0, 0, ref, 1/FPS)

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Controle de posição de carrinho")

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
                ref = ref + 0.5
            elif event.key == pygame.K_a:
                ref = ref - 0.5
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

    # FPS máximo e dt é o tempo entre uma chamada e outra em segundos
    dt = clock.tick(FPS)/1000
    # Update state using Forward Euler
    x_dot = compute_ddot_x(x, u, d)
    x = x + x_dot * dt
    
    u = Controller.update_output(ref, x[1])

    # Limites da tela
    if (x[1] < 0):
        x[0] = -x[0]*m*0.05
        x[1] = 0
    elif (x[1] > LARGURA - cart_width/WIDTH*LARGURA):
        x[0] = -x[0]*m*0.05
        x[1] = LARGURA - cart_width/WIDTH*LARGURA
    
    # Clear screen
    screen.fill(BLACK)

    # Draw cart
    cart_x = int(x[1]/LARGURA * WIDTH)
    cart_y = HEIGHT // 1.2


    # Draw line above cart
    draw_dotted_line(screen, WHITE, 
                     (cart_x, cart_y), 
                     (cart_x, cart_y-90))
    pos = font.render(f"x = {x[1]:.2f} m, v = {x[0]:0.2f}", True, (255, 255, 255))
    screen.blit(pos, (cart_x, cart_y-90-15))
    
    # Draw reference line
    ref_x = ref/LARGURA * WIDTH # x position of SP line
    ref_y_start = HEIGHT // 1.2 # y start position of SP line
    ref_y_end = HEIGHT // 1.2  - 150  # y end position of SP line
    draw_dotted_line(screen, REFERENCE_COLOR, 
                     (ref_x, ref_y_start), 
                     (ref_x, ref_y_end))
    ref_display = font.render(f"SP = {ref:.2f} m", True, (255, 255, 255))
    screen.blit(ref_display, (ref_x, ref_y_end-15))

    # Cart wheels (you can adjust the size and positions if needed)
    wheel_radius = 6
    left_wheel_center = (cart_x + cart_width // 5, cart_y + cart_height)
    right_wheel_center = (cart_x + cart_width*4 // 5, cart_y + cart_height)
    pygame.draw.circle(screen, CART_WHEEL_COLOR, left_wheel_center, wheel_radius)
    pygame.draw.circle(screen, CART_WHEEL_COLOR, right_wheel_center, wheel_radius)

    # Cart base
    pygame.draw.rect(screen, CART_COLOR, (cart_x, cart_y, cart_width, cart_height))

    if np.sign(d[0]) > 0:
        draw_horizontal_arrow(screen, (255, 0, 10), 
                              (cart_x+cart_width, cart_y+cart_height//2),
                              (cart_x+cart_width+d[0]*PROP_COEFF, cart_y+cart_height//2))
    else:
        draw_horizontal_arrow(screen, (255, 0, 10), 
                              (cart_x, cart_y+cart_height//2),
                              (cart_x+d[0]*PROP_COEFF, cart_y+cart_height//2))
    # Draw the track
    track_y = cart_y + cart_height + wheel_radius # Same y-coordinate as the cart 
    pygame.draw.line(screen, WHITE, 
                     (0, track_y + int(HEIGHT-track_y)//2), 
                     (WIDTH, track_y + int(HEIGHT-track_y)//2), 
                     int(HEIGHT-track_y))
        
    
    draw_pid_arrows(screen, cart_x, cart_y - 90, Controller.P, Controller.I, Controller.D)

    # Render important variables
    timestep = font.render(f"dt = {dt:.2f} s", True, (255, 255, 255))
    acc = font.render(f"a = {x_dot[0]:.2f} m/s2", True, (255, 255, 255))
    PID = font.render(f"PID = {u[0]:.2f} N", True, (255, 255, 255))
    error = font.render(f"e = {Controller.error:.2f} m", True, (255, 255, 255))
    dist = font.render(f"pert = {d[0]:.2f} N", True, (255, 255, 255))
    screen.blit(timestep, (10, 10))
    screen.blit(acc, (10, 30))
    screen.blit(PID, (10, 50))
    screen.blit(error, (10, 70))
    screen.blit(dist, (10, 90))

    Cont_text = font.render("Parâmetros do controlador:", True, (255, 255, 255))
    Kp_text = font.render(f"Kp = {Controller.Kp:.2f}", True, (255, 255, 255))
    Ki_text = font.render(f"Ki = {Controller.Ki:.2f}", True, (255, 255, 255))
    Kd_text = font.render(f"Kd = {Controller.Kd:.2f}", True, (255, 255, 255))
    screen.blit(Cont_text, (150, 10))
    screen.blit(Kp_text, (150, 30))
    screen.blit(Ki_text, (150, 50))
    screen.blit(Kd_text, (150, 70))

    alt_sp_text = font.render("a: diminui SP,   d: aumenta SP", True, (255, 255, 255))
    alt_pert_text = font.render("<-: pert. p/ esquerda,   ->: pert. p/ direita", True, (255, 255, 255))
    alt_p_text = font.render("p: aumenta Kp,   o: diminui Kp", True, (255, 255, 255))
    alt_i_text = font.render("l: aumenta Ki,   k: diminui Ki", True, (255, 255, 255))
    alt_d_text = font.render("m: aumenta Kd,   n: diminui Kd", True, (255, 255, 255))
    screen.blit(alt_sp_text, (400, 10))
    screen.blit(alt_pert_text, (400, 30))
    screen.blit(alt_p_text, (400, 50))
    screen.blit(alt_i_text, (400, 70))
    screen.blit(alt_d_text, (400, 90))
 
    pygame.display.flip()

pygame.quit()
