import pygame
import time
import random

pygame.init()
pygame.font.init()
WIDTH = 800
HEIGHT = 600
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pumpkin shooter")

# load images

BULLET = pygame.image.load("assets/bullet.png")
SHOOTER = pygame.image.load("assets/shooter.png")
PUMPKIN = pygame.image.load("assets/pumpkin.png")
BG = pygame.transform.scale(pygame.image.load("assets/bg.jpg"), (WIDTH, HEIGHT))


def main():
    run = True
    FPS = 60
    clock = pygame.time.Clock()
    Level = 1
    Lives = 3
    main_font = pygame.font.SysFont("comicsans", 40)

    def draw():
        WINDOW.blit(BG, (0, 0))
        # drawing text
        lives_txt = main_font.render(f"lives:{Lives}", 1, "white")
        Level_txt = main_font.render(f"level:{Level}", 1, "white")

        WINDOW.blit(lives_txt, (10, 10))
        WINDOW.blit(Level_txt, (WIDTH - Level_txt.get_width() - 10, 10))

        pygame.display.update()

    while run:
        clock.tick(FPS)
        draw()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False


main()
