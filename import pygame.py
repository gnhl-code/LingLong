import pygame
import time

pygame.init()

WIDTH, HEIGHT = 800, 200
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rainbow Text Animation")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

font = pygame.font.Font(None, 72)  # Choose a font and size
text = "RAINBOW!"
rainbow_colors = [
    pygame.Color("red"),
    pygame.Color("orange"),
    pygame.Color("yellow"),
    pygame.Color("green"),
    pygame.Color("blue"),
    pygame.Color("indigo"),
    pygame.Color("violet"),
]

color_index = 0
animation_speed = 0.1  # Adjust for faster/slower animation

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(BLACK)

    color = rainbow_colors[color_index]
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(text_surface, text_rect)

    pygame.display.flip()

    time.sleep(animation_speed)  # Delay for animation speed

    color_index = (color_index + 1) % len(rainbow_colors)  # Cycle through colors

pygame.quit()