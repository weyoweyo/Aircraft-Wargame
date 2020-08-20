import random
import pygame

INTERFACE_RECT = pygame.Rect(0, 0, 480, 600)
FRAME_PER_SEC = 60
CREATE_ENEMY_EVENT = pygame.USEREVENT
CENTER_HERO = 100
HERO_FIRE_EVENT = pygame.USEREVENT + 1
ENEMY_SPEED_MIN = 2
ENEMY_SPEED_MAX = 4


class GameSprite(pygame.sprite.Sprite):
    def __init__(self, image_name, speed=1):
        super().__init__()

        self.image = pygame.image.load(image_name)
        self.rect = self.image.get_rect()
        self.speed = speed

    def update(self):
        self.rect.y += self.speed


class Background(GameSprite):
    # is_alt: True, self.rect.y = -self.rect.height,
    # which means put another background image above
    # is_alt: False, put background image at (0,0)
    def __init__(self,  is_alt=False):
        super().__init__("./images/background.png")
        if is_alt:
            self.rect.y = -self.rect.height

    # override
    def update(self):
        # inheritance
        super().update()
        if self.rect.y >= INTERFACE_RECT.height:
            self.rect.y = -self.rect.height


class Enemy(GameSprite):
    def __init__(self):
        enemy_image = ["./images/enemy1.png", "./images/enemy2.png"]
        super().__init__(enemy_image[random.randint(0, 1)])
        self.speed = random.randint(ENEMY_SPEED_MIN, ENEMY_SPEED_MAX)

        # bottom == 0 means y == -height
        self.rect.bottom = 0

        # enemy aircraft move also horizontally
        max_x = INTERFACE_RECT.width - self.rect.width
        self.rect.x = random.randint(0, max_x)

        self.bullets = pygame.sprite.Group()

    # override
    def update(self):
        # make sure enemy aircraft move vertically
        super().update()
        if self.rect.y >= INTERFACE_RECT.height:
            self.kill()

    def __del__(self):
        pass


class Hero(GameSprite):
    def __init__(self):
        super().__init__("./images/me1.png", 0)
        # initialize the position of hero
        self.rect.centerx = INTERFACE_RECT.centerx
        self.rect.bottom = INTERFACE_RECT.bottom - CENTER_HERO

        self.bullets = pygame.sprite.Group()

    # override
    def update(self):
        self.rect.x += self.speed
        # hero can not be out of interface
        if self.rect.x < 0:
            self.rect.x = 0
        # right = x + width of hero
        elif self.rect.right > INTERFACE_RECT.right:
            self.rect.right = INTERFACE_RECT.right

    def fire(self):
        for i in (0, 1, 2):
            bullet_image = ["./images/bullet2.png", "./images/bullet1.png"]
            bullet = Bullet(bullet_image[random.randint(0, 1)], -2)

            # initialize position
            bullet.rect.bottom = self.rect.y - 20*i
            bullet.rect.centerx = self.rect.centerx

            self.bullets.add(bullet)


class Bullet(GameSprite):
    def update(self):
        super().update()
        if self.rect.bottom < 0:
            self.kill()

    def __del__(self):
        pass
