

import pygame
import random
import os


pygame.init()
pygame.mixer.init()

# Constants
# --------------------------------------------------
WIDTH, HEIGHT = 800, 500
WHITE = (255, 255, 255)
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)
numbers = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']

# Screen setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Slot Machine")

# Slot Class
class Slot:
    def __init__(self, x, y, w, h):
        self.rect = pygame.Rect(x, y, w, h)
        self.symbol = "?"  # Default
        self.color = (0, 0, 0)

    def draw(self, surf, font, color):
        pygame.draw.rect(surf, color, self.rect, 3)
        text = font.render(self.symbol, True, color)
        text_rect = text.get_rect(center=self.rect.center)
        surf.blit(text, text_rect)

    def roll(self):
        self.symbol = random.choice(numbers)

# Spin Button Class
class Spin:
    def __init__(self, x, y, w, h):
        self.rect = pygame.Rect(x, y, w, h)
        self.clicked = False

    def draw(self, surf, font, col, hover_col, text="Spin"):
        pos = pygame.mouse.get_pos()
        is_hover = self.rect.collidepoint(pos)
        pygame.draw.rect(surf, hover_col if is_hover else col, self.rect)
        text_surf = font.render(text, True, (0, 0, 0))
        text_rect = text_surf.get_rect(center=self.rect.center)
        surf.blit(text_surf, text_rect)

    def is_clicked(self, event):
        return (
        event.type == pygame.MOUSEBUTTONDOWN
        and event.button == 1  # Only left mouse button
        and self.rect.collidepoint(event.pos)
    )

# Create instances OUTSIDE the loop
slot1 = Slot(200, 100, 100, 200)
slot2 = Slot(350, 100, 100, 200)
slot3 = Slot(500, 100, 100, 200)
spin_button = Spin(300, 350, 200, 75)
alert_okay_button = Spin(350, 400, 100, 50)  # Button for "Okay" in alert

# Jackpot popup state
show_jackpot = False

# Load jackpot music (assumes jackpot.mp3 in project folder)
JACKPOT_MUSIC = "assets\[EDIT] Hakari Dance.mp3"
music_loaded = False
if os.path.exists(JACKPOT_MUSIC):
    try:
        pygame.mixer.music.load(JACKPOT_MUSIC)
        music_loaded = True
    except Exception as e:
        print(f"Could not load jackpot music: {e}")

# Load jackpot animation frames (assumes frames/frame_0001.png ... exist)
JACKPOT_FRAMES = []
JACKPOT_FRAME_FOLDER = "frames"
JACKPOT_FRAME_RATE = 60  # frames per second
if os.path.exists(JACKPOT_FRAME_FOLDER):
    for fname in sorted(os.listdir(JACKPOT_FRAME_FOLDER)):
        if fname.endswith(".png") or fname.endswith(".jpg"):
            img = pygame.image.load(os.path.join(JACKPOT_FRAME_FOLDER, fname)).convert()
            JACKPOT_FRAMES.append(pygame.transform.scale(img, (WIDTH, HEIGHT)))


# Main game loop
running = True
# For jackpot animation
jackpot_frame_idx = 0
jackpot_last_update = 0
jackpot_playing = False

while running:
    screen.fill(WHITE)


    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # If jackpot animation is playing, only allow closing it
        if show_jackpot:
            if alert_okay_button.is_clicked(event):
                show_jackpot = False
                jackpot_playing = False
                # Stop music when jackpot popup is dismissed
                if music_loaded:
                    pygame.mixer.music.stop()
        else:
            if spin_button.is_clicked(event):
                # 10% probability for all slots to be the same
                if random.random() < 0.05:
                    same_symbol = random.choice(numbers)
                    slot1.symbol = same_symbol
                    slot2.symbol = same_symbol
                    slot3.symbol = same_symbol
                else:
                    slot1.roll()
                    slot2.roll()
                    slot3.roll()
                # Only show jackpot if all symbols match and not '?'
                if (slot1.symbol == slot2.symbol == slot3.symbol and slot1.symbol != "?"):
                    show_jackpot = True
                    jackpot_frame_idx = 0
                    jackpot_last_update = pygame.time.get_ticks()
                    jackpot_playing = True if JACKPOT_FRAMES else False
                    # Play music when jackpot starts
                    if music_loaded:
                        pygame.mixer.music.play(-1)  # loop until stopped

    # Draw slot and button only if not showing jackpot
    if not show_jackpot:
        slot1.draw(screen, font, (0, 0, 0))
        slot2.draw(screen, font, (0, 0, 0))
        slot3.draw(screen, font, (0, 0, 0))
        spin_button.draw(screen, font, (255, 223, 0), (255, 165, 0))

    # Draw jackpot popup if needed
    if show_jackpot:
        # Play jackpot animation if frames are loaded
        if jackpot_playing and JACKPOT_FRAMES:
            now = pygame.time.get_ticks()
            if now - jackpot_last_update > 1000 // JACKPOT_FRAME_RATE:
                jackpot_frame_idx = (jackpot_frame_idx + 1) % len(JACKPOT_FRAMES)
                jackpot_last_update = now
            screen.blit(JACKPOT_FRAMES[jackpot_frame_idx], (0, 0))
        else:
            # fallback: just fill with a color
            pygame.draw.rect(screen, (0, 0, 0), (0, 0, WIDTH, HEIGHT))
        # Draw the Okay button on top
        alert_okay_button.draw(screen, font, (255, 223, 0), (255, 165, 0), "Okay")

    pygame.display.update()
    clock.tick(60)

pygame.quit()
