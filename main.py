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


class Ship:
    def __init__(self, x, y, health=100):
        self.x = x
        self.y = y
        self.health = health
        self.img = None
        self.bullet = None
        self.coolDown = 0 

    def draw(self, window):
        window.blit(self.img,(self.x,self.y))
    def get_width(self):
        return self.get_width()
    def get_height(self):
        return self.get_height()
    
    
class Player(Ship):
    def __init__(self, x, y, health=100):
        super().__init__(x, y, health)
        self.img = SHOOTER
        self.bullet = BULLET

def main():
    run = True
    FPS = 60
    clock = pygame.time.Clock()
    Level = 1
    Lives = 3
    main_font = pygame.font.SysFont("comicsans", 40)
    ghost = Player(300, 530)
    ghost_vel = 5

    def draw():
        WINDOW.blit(BG, (0, 0))
        # drawing text
        lives_txt = main_font.render(f"lives:{Lives}", 1, "white")
        Level_txt = main_font.render(f"level:{Level}", 1, "white")

        WINDOW.blit(lives_txt, (10, 10))
        WINDOW.blit(Level_txt, (WIDTH - Level_txt.get_width() - 10, 10))
        ghost.draw(WINDOW)
        pygame.display.update()

    while run:
        clock.tick(FPS)
        draw()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys = pygame.key.get_pressed()
        if (keys[pygame.K_a] or keys[pygame.K_LEFT]) and ghost.x - ghost_vel > 0:
            ghost.x -= ghost_vel
        if (keys[pygame.K_d] or keys[pygame.K_RIGHT]) and ghost.x + ghost_vel < WIDTH:
            ghost.x += ghost_vel
        if (keys[pygame.K_w] or keys[pygame.K_UP]) and ghost.y - ghost_vel > 0:
            ghost.y -= ghost_vel
        if (keys[pygame.K_s] or keys[pygame.K_DOWN]) and ghost.y - ghost_vel < HEIGHT:
            ghost.y += ghost_vel


main()
