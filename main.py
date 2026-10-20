import pygame
import random
import asyncio

pygame.init()
pygame.font.init()

WIDTH = 1000
HEIGHT = 800

WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pumpkin shooter")

BULLET = pygame.transform.scale(
    pygame.image.load("assets/bullet.png").convert_alpha(), (12, 24)
)
SHOOTER = pygame.transform.scale(
    pygame.image.load("assets/shooter.png").convert_alpha(), (60, 50)
)
PUMPKIN = pygame.transform.scale(
    pygame.image.load("assets/pumpkin.png").convert_alpha(), (60, 50)
)
SHULK = pygame.transform.scale(
    pygame.image.load("assets/shulk.png").convert_alpha(), (20, 20)
)
BONE = pygame.transform.scale(
    pygame.image.load("assets/bones.png").convert_alpha(), (20, 20)
)

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
        return self.y + self.img.get_height() < 0 or self.y > height

    def collision(self, obj):
        return is_collide(obj, self)


class Ship:
    COOLDOWN = 30

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
            bullet_x = self.x + self.get_width() // 2 - self.bullet_img.get_width() // 2
            bullet_y = self.y - self.bullet_img.get_height()

            bullet = Bullet(bullet_x, bullet_y, self.bullet_img)

            self.bullets.append(bullet)
            self.coolDown = 1

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))

        for bullet in self.bullets:
            bullet.draw(window)

    def get_width(self):
        return self.img.get_width()

    def get_height(self):
        return self.img.get_height()

    def move_bullets(self, vel, obj):
        self.cooldown()

        for bullet in self.bullets[:]:
            bullet.move(vel)

            if bullet.off_screen(HEIGHT):
                self.bullets.remove(bullet)

            elif bullet.collision(obj):
                obj.health -= 10
                self.bullets.remove(bullet)

    def cooldown(self):
        if self.coolDown >= self.COOLDOWN:
            self.coolDown = 0

        elif self.coolDown > 0:
            self.coolDown += 1


class Player(Ship):
    def __init__(self, x, y, health=100):
        super().__init__(x, y, health)

        self.img = SHOOTER
        self.bullet_img = BULLET

        self.mask = pygame.mask.from_surface(self.img)
        self.health = health

    def move_bullets(self, vel, objs):
        self.cooldown()

        for bullet in self.bullets[:]:
            bullet.move(vel)

            if bullet.off_screen(HEIGHT):
                self.bullets.remove(bullet)
                continue

            for obj in objs[:]:
                if bullet.collision(obj):
                    objs.remove(obj)
                    self.bullets.remove(bullet)
                    break


class Enemy(Ship):
    def __init__(self, x, y, health=100):
        super().__init__(x, y, health)

        self.img = PUMPKIN

        self.bullet_img = random.choice([SHULK, BONE])

        self.mask = pygame.mask.from_surface(self.img)
        self.next_shot = None

    def move(self, vel):
        self.y += vel

    def shoot(self):
        if self.coolDown == 0:
            bullet_x = self.x + self.get_width() // 2 - self.bullet_img.get_width() // 2

            bullet_y = self.y + self.get_height()

            bullet = Bullet(bullet_x, bullet_y, self.bullet_img)

            self.bullets.append(bullet)
            self.coolDown = 1


def is_collide(obj1, obj2):
    offset_x = int(obj2.x - obj1.x)
    offset_y = int(obj2.y - obj1.y)

    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) is not None


async def main():
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

    # restart_button = pygame.Rect(WIDTH // 2 - 120, HEIGHT // 2 + 80, 240, 60)
    player_bullet_vel = -7
    enemy_bullet_vel = 4

    def draw():
        WINDOW.blit(BG, (0, 0))

        lives_txt = main_font.render(f"lives: {Lives}", True, "white")
        level_txt = main_font.render(f"level: {Level}", True, "white")
        health_txt = main_font.render(f"Health: {max(0, ghost.health)}", True, "white")

        WINDOW.blit(lives_txt, (10, 10))
        WINDOW.blit(level_txt, (WIDTH - level_txt.get_width() - 10, 10))
        WINDOW.blit(health_txt, (10, 55))

        for enemy in enemies:
            enemy.draw(WINDOW)

        ghost.draw(WINDOW)

        if lost:
            lost_txt = lost_font.render("GAME OVER !", True, "red")
            restart_txt = main_font.render("Press R to Restart", True, "white")

            WINDOW.blit(
                lost_txt, lost_txt.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
            )

            WINDOW.blit(
                restart_txt, restart_txt.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
            )

        pygame.display.update()

    while run:
        clock.tick(FPS)
        await asyncio.sleep(0)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r and lost:
                    Level = 0
                    Lives = 3
                    wave_length = 3
                    enemies = []

                    ghost = Player(300, 530)

                    lost = False
                    lost_count = 0
        if not run:
            break

        if Lives <= 0 or ghost.health <= 0:
            lost = True

        if lost:
            draw()
            continue

        if len(enemies) == 0:
            Level += 1
            wave_length += 5

            for _ in range(wave_length):
                enemy = Enemy(
                    random.randrange(30, WIDTH - 100), random.randrange(-500, -50)
                )

                enemies.append(enemy)

        keys = pygame.key.get_pressed()

        if (keys[pygame.K_a] or keys[pygame.K_LEFT]) and ghost.x - ghost_vel >= 0:
            ghost.x -= ghost_vel

        if (
            keys[pygame.K_d] or keys[pygame.K_RIGHT]
        ) and ghost.x + ghost_vel + ghost.get_width() <= WIDTH:
            ghost.x += ghost_vel

        if (keys[pygame.K_w] or keys[pygame.K_UP]) and ghost.y - ghost_vel >= 0:
            ghost.y -= ghost_vel

        if (
            keys[pygame.K_s] or keys[pygame.K_DOWN]
        ) and ghost.y + ghost_vel + ghost.get_height() <= HEIGHT:
            ghost.y += ghost_vel

        if keys[pygame.K_SPACE]:
            ghost.shoot()

        for enemy in enemies[:]:
            enemy.move(enemy_vel)

            if enemy.y >= 0:
                now = pygame.time.get_ticks()

                if enemy.next_shot is None:
                    enemy.next_shot = now + random.randint(2000, 5000)
                elif now >= enemy.next_shot:
                    enemy.shoot()
                    enemy.next_shot = now + random.randint(2000, 5000)
            enemy.move_bullets(enemy_bullet_vel, ghost)
            if enemy.y + enemy.get_height() > HEIGHT:
                Lives -= 1
                enemies.remove(enemy)

        ghost.move_bullets(player_bullet_vel, enemies)
        draw()

    pygame.quit()


if __name__ == "__main__":
    asyncio.run(main())