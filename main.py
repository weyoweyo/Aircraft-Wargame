import pygame
from aircraft_sprites import *

ENEMY_FREQ = 1000
FIRE_FREQ = 500


class AircraftGame(object):
    def __init__(self):
        print("Initializing...")
        self.interface = pygame.display.set_mode(INTERFACE_RECT.size)
        self.clock = pygame.time.Clock()
        self.__create_sprites()
        pygame.time.set_timer(CREATE_ENEMY_EVENT, ENEMY_FREQ)
        pygame.time.set_timer(HERO_FIRE_EVENT, FIRE_FREQ)

    def __create_sprites(self):
        bg1 = Background()
        bg2 = Background(True)
        self.back_group = pygame.sprite.Group(bg1, bg2)

        self.enemy_group = pygame.sprite.Group()

        self.hero = Hero()
        self.hero_group = pygame.sprite.Group(self.hero)

    def start_game(self):
        print("Game starts!")
        while True:
            self.clock.tick(FRAME_PER_SEC)
            self.__event_handler()
            self.__check_collide()
            self.__update_sprites()
            pygame.display.update()

    def __event_handler(self):
        for event in pygame.event.get():
            # Exit
            if event.type == pygame.QUIT:
                AircraftGame.__game_over()

            # Enemy
            elif event.type == CREATE_ENEMY_EVENT:
                enemy = Enemy()
                # create an enemy aircraft per second
                self.enemy_group.add(enemy)

            # Fire:
            elif event.type == HERO_FIRE_EVENT:
                self.hero.fire()

            # Hero
            key_pressed = pygame.key.get_pressed()
            if key_pressed[pygame.K_RIGHT]:
                self.hero.speed = 2
            elif key_pressed[pygame.K_LEFT]:
                self.hero.speed = -2
            else:
                self.hero.speed = 0

    def __check_collide(self):
        # Bullets kill enemy aircraft
        pygame.sprite.groupcollide(self.hero.bullets, self.enemy_group, True, True)
        # Enemy aircraft kill hero
        enemies = pygame.sprite.spritecollide(self.hero, self.enemy_group, True)
        if len(enemies) > 0:
            self.hero.kill()
            AircraftGame.__game_over()

    def __update_sprites(self):
        self.back_group.update()
        self.back_group.draw(self.interface)

        self.enemy_group.update()
        self.enemy_group.draw(self.interface)

        self.hero_group.update()
        self.hero_group.draw(self.interface)
        self.hero.bullets.update()
        self.hero.bullets.draw(self.interface)

    @staticmethod
    def __game_over():
        print("Game Over!")
        pygame.quit()
        exit()


if __name__ == '__main__':
    game = AircraftGame()
    game.start_game()