import pygame
import time
import random

pygame.init()

WIDTH = 800
HEIGHT = 600
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pumpkin shooter")

# load images

BULLET = pygame.image.load("assets/bullet.png")
SHOOTER = pygame.image.load("assets/shooter.png")
PUMPKIN = pygame.image.load("assets/pumpkin.png")
BG = pygame.image.load("assets/bg.jpg")


def main():
    run = True
    FPS = 60
    clock = pygame.time.Clock()
    
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                
main()