import pygame
import time
import random

pygame.init()
pygame.font.init()
WIDTH = 1000
HEIGHT = 800
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pumpkin shooter")

# load images
BULLET = pygame.image.load("assets/bullet.png").convert_alpha()
SHOOTER = pygame.transform.scale(
    pygame.image.load("assets/shooter.png").convert_alpha(), (60, 50)
)
PUMPKIN = pygame.transform.scale(
    pygame.image.load("assets/pumpkin.png").convert_alpha(), (60, 50)
)
SHULK = pygame.image.load("assets/shulk.png").convert_alpha()
BONE = pygame.image.load("assets/bones.png").convert_alpha()

BG = pygame.transform.scale(
    pygame.image.load("assets/bg.jpg").convert(), (WIDTH, HEIGHT)
)


class Bullet:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))

    def move(self, vel):
        self.y += vel

    def off_screen(self, height):
        return self.y + self.img.get_height() >= 0 and self.y <= height

    def collision(self, obj):
        return is_collide(obj, self)


class Ship:
    def __init__(self, x, y, health=100):
        self.x = x
        self.y = y
        self.health = health
        self.img = None
        self.bullet_img = None
        self.bullets = []
        self.coolDown = 0

    def shoot(self):
        if self.coolDown == 0:
            bullet = Bullet(self.x, self.y, self.bullet_img)
            self.bullets.append(bullet)
            self.coolDown = 1

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))

    def get_width(self):
        return self.img.get_width()

    def get_height(self):
        return self.img.get_height()

    def move_bullets(self, vel):
        self.coolDown()
        for bullet in self.bullets[:]:
            bullet.move(vel)
            if not bullet.off_screen(HEIGHT):
                self.bullets.remove(bullet)

    def cooldown(self):
        if self.coolDown > 0:
            self.coolDown += 1

        if self.coolDown >= 30:
            self.coolDown = 0


class Player(Ship):
    def __init__(self, x, y, health=100):
        super().__init__(x, y, health)
        self.img = SHOOTER
        self.bullet = BULLET
        self.mask = pygame.mask.from_surface(self.img)
        self.health = health


class Enemy(Ship):
    def __init__(self, x, y, health=100):
        super().__init__(
            x,
            y,
            health,
        )
        self.img = PUMPKIN
        self.bullet_img = random.choice([SHULK, BULLET, BONE])
        self.mask = pygame.mask.from_surface(self.img)

    def move(self, vel):
        self.y += vel


def is_collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y

    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) is not None


def main():
    run = True
    FPS = 60
    clock = pygame.time.Clock()
    Level = 0
    Lives = 3
    main_font = pygame.font.SysFont("comicsans", 40)
    lost_font = pygame.font.SysFont("comicsans", 100)
    ghost = Player(300, 530)
    ghost_vel = 5

    enemy_vel = 1
    wave_length = 3
    enemies = []
    lost = False
    lost_count = 0
    
    
    player_bullet_vel = -7
    enemy_bullet_vel = 4

    def draw():
        WINDOW.blit(BG, (0, 0))
        # drawing text
        lives_txt = main_font.render(f"lives:{Lives}", 1, "white")
        Level_txt = main_font.render(f"level:{Level}", 1, "white")

        WINDOW.blit(lives_txt, (10, 10))
        WINDOW.blit(Level_txt, (WIDTH - Level_txt.get_width() - 10, 10))

        for enemy in enemies:
            enemy.draw(WINDOW)
        ghost.draw(WINDOW)
        if lost:
            lost_txt = lost_font.render("You lost !!", 1, "red")
            WINDOW.blit(lost_txt, (WIDTH / 2 - lost_txt.get_width() / 2, HEIGHT / 2))
        pygame.display.update()

    while run:
        clock.tick(FPS)

        draw()
        if Lives <= 0 or ghost.health <= 0:
            lost = True
            lost_count += 1

        if lost:
            if lost_count > FPS * 2:
                run = False
            else:
                continue

        if len(enemies) == 0:
            Level += 1
            wave_length += 5
            for _ in range(wave_length):
                enemy = Enemy(
                    random.randrange(30, WIDTH - 100), random.randrange(-500, -50)
                )
                enemies.append(enemy)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys = pygame.key.get_pressed()
        if (keys[pygame.K_a] or keys[pygame.K_LEFT]) and ghost.x - ghost_vel > 0:
            ghost.x -= ghost_vel
        if (
            keys[pygame.K_d] or keys[pygame.K_RIGHT]
        ) and ghost.x + ghost_vel + ghost.get_width() < WIDTH:
            ghost.x += ghost_vel
        if (keys[pygame.K_w] or keys[pygame.K_UP]) and ghost.y - ghost_vel > 0:
            ghost.y -= ghost_vel
        if (
            keys[pygame.K_s] or keys[pygame.K_DOWN]
        ) and ghost.y + ghost_vel + ghost.get_height() < HEIGHT:
            ghost.y += ghost_vel

        for enemy in enemies[:]:
            enemy.move(enemy_vel)
            if enemy.y + enemy.get_height() > HEIGHT:
                Lives -= 1
                enemies.remove(enemy)


main()
