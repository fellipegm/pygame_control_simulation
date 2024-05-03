import pygame
import numpy as np

PROP_COEFF = 4

# Initialize the font module
pygame.font.init()
font = pygame.font.Font(None, 20)

def draw_dotted_line(surface, color, start_pos, end_pos, width=1, dash_length=4):
    x1, y1 = start_pos
    x2, y2 = end_pos
    dx = x2 - x1
    dy = y2 - y1

    distance = max(abs(dx), abs(dy))
    for i in range(0, int(distance), dash_length):
        x = int(x1 + i / distance * dx)
        y = int(y1 + i / distance * dy)
        pygame.draw.line(surface, color, (x, y), (x, y), width)


def draw_pid_arrows(screen, x, y, P, I, D):
    MAX_ARROW_LENGTH = 100
    
    # Calculate P arrow parameters
    P_arrow_start = (x, y + 20)  # Start above the cart
    P_arrow_length = min(MAX_ARROW_LENGTH, abs(P) * PROP_COEFF)  # Limit the length
    P_arrow_end = (x + int(np.sign(P) * P_arrow_length), P_arrow_start[1])
    # Draw P arrow
    draw_horizontal_arrow(screen, (255, 50, 50), P_arrow_start, P_arrow_end)
    P_text = font.render(f"P = {P:.1f} N", True, (255, 255, 255))
    if P > 0:
        screen.blit(P_text, (P_arrow_end[0]+20, P_arrow_start[1]-10))
    else:
        screen.blit(P_text, (P_arrow_end[0]-80, P_arrow_start[1]-10))

    # Calculate I arrow parameters
    I_arrow_start = (x, P_arrow_start[1] + 20)  # Start above the cart
    I_arrow_length = min(MAX_ARROW_LENGTH, abs(I) * PROP_COEFF)  # Limit the length
    I_arrow_end = (x + int(np.sign(I) * I_arrow_length), I_arrow_start[1])
    # Draw I arrow
    draw_horizontal_arrow(screen, (50, 255, 50), I_arrow_start, I_arrow_end)
    I_text = font.render(f"I = {I:.1f} N", True, (255, 255, 255))
    if I > 0:
        screen.blit(I_text, (I_arrow_end[0]+20, I_arrow_start[1]-10))
    else:
        screen.blit(I_text, (I_arrow_end[0]-80, I_arrow_start[1]-10))

    # Calculate D arrow parameters
    D_arrow_start = (x, I_arrow_start[1] + 20)  # Start above the cart
    D_arrow_length = min(MAX_ARROW_LENGTH, abs(D) * PROP_COEFF)  # Limit the length
    D_arrow_end = (x + int(np.sign(D) * D_arrow_length), D_arrow_start[1])
    # Draw D arrow
    draw_horizontal_arrow(screen, (50, 255, 255), D_arrow_start, D_arrow_end)
    D_text = font.render(f"D = {D:.1f} N", True, (255, 255, 255))
    if D > 0:
        screen.blit(D_text, (D_arrow_end[0]+20, D_arrow_start[1]-10))
    else:
        screen.blit(D_text, (D_arrow_end[0]-80, D_arrow_start[1]-10))


def draw_horizontal_arrow(screen, color, start_pos, end_pos, head_length=15, head_width=10):
    """Draws a horizontal arrow with a triangular head pointing to the right.

    Args:
        screen (pygame.Surface): The surface to draw the arrow on.
        color (tuple): The color of the arrow (R, G, B format).
        start_pos (tuple): The starting point of the arrow (x, y).
        end_pos (tuple): The ending point of the arrow (x, y).
        head_length (int, optional): Length of the arrowhead. Defaults to 15.
        head_width (int, optional): Width of the arrowhead base. Defaults to 10.
    """
    if abs(start_pos[0] - end_pos[0]) > 1:
        # Draw the line
        pygame.draw.line(screen, color, start_pos, end_pos, 2)  # Adjust width as needed

        # Calculate arrowhead points (head always points to the right)
        arrowhead_top = (end_pos[0], end_pos[1] - head_width // 2)
        arrowhead_bottom = (end_pos[0], end_pos[1] + head_width // 2)
        if (end_pos[0] - start_pos[0]) > 0:
            arrowhead_end = (end_pos[0]+head_length, end_pos[1])
        else:
            arrowhead_end = (end_pos[0]-head_length, end_pos[1])
        # Draw the arrowhead
        pygame.draw.polygon(screen, color, [arrowhead_end, arrowhead_top, arrowhead_bottom])