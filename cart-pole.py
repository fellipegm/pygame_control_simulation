
import pygame
import numpy as np

# Initialize pygame
pygame.init()

# Colors
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)

# Initialize the font module
pygame.font.init()

# Choose a font (default pygame font here, size 24)
font = pygame.font.Font(None, 24)

# Initialize the clock
clock = pygame.time.Clock()

# Screen dimensions
WIDTH, HEIGHT = 800, 400

FPS = 50

# Cart-Pendulum parameters
l = 100  # pendulum length
cart_width = 50
cart_height = 30
m_cart = 1.0
m_pole = 0.1
g = 9.81
F = 10.0  # Force applied when key is pressed

# System matrices (considering the non-linear equations)
def compute_x_dot(x, u):
    theta = x[2, 0]
    theta_dot = x[3, 0]
    
    d2theta = (g * np.sin(theta) + np.cos(theta) * (-u[0, 0] - m_pole * l * theta_dot**2 * np.sin(theta)) / (m_cart + m_pole)) / (l * (4/3 - m_pole * np.cos(theta)**2 / (m_cart + m_pole)))
    dx = x[1, 0]
    d2x = (u[0, 0] + m_pole * l * (theta_dot**2 * np.sin(theta) - d2theta * np.cos(theta))) / (m_cart + m_pole)
    
    return np.array([[dx], [d2x], [theta_dot], [d2theta]])

# Initial condition
x = np.array([[0], [0], [0.1], [0]])  # Small deviation in theta to start with


# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pendulum on Cart (No Control)")

u = np.array([[0]])  # No force initially
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                u = np.array([[-F]])  # Apply left force
            elif event.key == pygame.K_RIGHT:
                u = np.array([[F]])   # Apply right force
        elif event.type == pygame.KEYUP:
            if event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                u = np.array([[0]])  # Remove force

    # FPS máximo e dt é o tempo entre uma chamada e outra
    dt = clock.tick(FPS)/1000
    # Update state using Forward Euler
    x_dot = compute_x_dot(x, u)
    x = x + x_dot * dt

    # Clear screen
    screen.fill(BLACK)

    # Draw cart and pendulum
    cart_x = int(WIDTH / 2 + x[0, 0])
    cart_y = HEIGHT // 2
    pendulum_x = int(cart_x + l * np.sin(x[2, 0]))
    pendulum_y = int(cart_y - l * np.cos(x[2, 0]))

    pygame.draw.rect(screen, GRAY, (cart_x - cart_width // 2, cart_y - cart_height // 2, cart_width, cart_height))
    pygame.draw.line(screen, GRAY, (cart_x, cart_y), (pendulum_x, pendulum_y), 2)
    
    # Render the elapsed time
    text_surface = font.render(f"dt = {dt:.2f} s", True, (255, 255, 255))
    screen.blit(text_surface, (10, 10))

    pygame.display.flip()

pygame.quit()
