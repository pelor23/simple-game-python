# Here we import method exit() from module called sys
from sys import exit
import random

# Here we import two things: firstly the library called pygame;
# Secondly from pygame.locals we import the entire contents.
import pygame
from pygame.locals import *

# Here we set window size.
SCREEN_SIZE = (800, 600)
# Here we have constant, which stores pygame clock.
CLOCK = pygame.time.Clock()
# Variable - score - declaration
SCORE = 0
# Yellow color declaration
YELLOW = (255, 255, 0)
# Variable - life - declaration
LIFE = 3


# Here we have class Bullet
class Bullet:
    ## Here is method initializing coords of bullet and image of our bullet.
    def __init__(self, surface, x_coord, y_coord):
        self.surface = surface
        self.x = x_coord + 24
        self.y = y_coord
        self.image = pygame.image.load('laser.png')
        return

    ## Here is method which updates coords of this bullet.
    def update(self, y_amount=5):
        self.y -= y_amount
        self.surface.blit(self.image, (self.x, self.y))
        return


# Here we have class which creates enemy's bullets
class EnemyBullet:
    ## Here is method initializing coords of bullet and image of our bullet.
    def __init__(self, surface, x_coord, y_coord):
        self.surface = surface
        self.x = x_coord + 12
        self.y = y_coord
        self.image = pygame.image.load('laser.png')
        return


    ## Here is method which updates coords of this bullets.
    def update(self, y_amount=5):
        self.y += y_amount
        self.surface.blit(self.image, (self.x, self.y))
        return


# Here we have class which creates an instance of the enemy
class Enemy:
    ## Here is method initializing coords of enemies.
    def __init__(self, x_coord, y_coord, points):
        self.x = x_coord
        self.y = y_coord
        self.points = points
        self.image = pygame.image.load('enemy.png')
        self.speed = 3
        return

    ## Here is method which updates coords of our enemies.
    def update(self, surface, dirx, y_amount=0):
        self.x += (dirx * self.speed)
        self.y += y_amount
        surface.blit(self.image, (self.x, self.y))
        return


# Here is add loop generating matrix opponents.
def generate_enemies():
    matrix = []
    for y in range(5):
        if y == 0:
            points = 30
        elif y == 1 or y == 2:
            points = 20
        else:
            points = 10


        enemies = [Enemy(80 + (40 * x), 50 + (50 * y), points) for x in range(11)]
        matrix.append(enemies)
    return matrix


# Here is method which checks collision.
def check_collision(object1_x, object1_y, object2_x, object2_y):
    if ((object1_x > object2_x) and (object1_x < object2_x + 35) and
        (object1_y > object2_y) and (object1_y < object2_y + 35)
    ):
        return True
    return False


# Here is our main class.
class SpaceInvadersGame(object):
    ## Here is the method responsible for initializing and setting the pygame library and display windows.
    def __init__(self, score=SCORE, life=LIFE):
        pygame.init()
        flag = DOUBLEBUF
        self.surface = pygame.display.set_mode(SCREEN_SIZE, flag)
        self.surface.fill((0, 0, 0))
        gamefont = pygame.font.Font(None, 15)
        self.bullets_array = []
        self.enemies_matrix = generate_enemies()
        self.enemies_bullets = []
        self.score = score
        self.life = life


        hello_label = gamefont.render("Press ENTER to start the game", 1, (255, 255, 0))
        self.surface.blit(hello_label, (100, 100))
        self.draw_player()
        pygame.display.flip()

        while True:
            for event in pygame.event.get():
                if event.type == KEYDOWN and event.key == K_RETURN:
                    self.gamestate = 1
                    self.loop()
                if (event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE)):
                    exit()


    ## Method for game over screen
    def game_over_scren(self):
        gamefont = pygame.font.Font(None, 15)
        label = gamefont.render("Press Y if you would like to restart game, N to exit the game", 1, YELLOW)
        score = gamefont.render("You finished with score: {}".format(self.score), 1, YELLOW)
        self.surface.fill((0, 0, 0))
        self.surface.blit(label, (100, 100))
        self.surface.blit(score, (100, 120))
        pygame.display.flip()

        while True:
            for event in pygame.event.get():
                if event.type == KEYDOWN and event.key == K_y:
                    SpaceInvadersGame()
                if (event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE) or
                        (event.type == KEYDOWN and event.key == K_n)):
                    exit()


     # Method which reload the board
    def continue_screen(self):
        gamefont = pygame.font.Font(None, 15)
        label = gamefont.render("Press ENTER if you would like to continue", 1, YELLOW)
        score = gamefont.render("Your score: {}".format(self.score), 1, YELLOW)
        self.surface.fill((0, 0, 0))
        self.surface.blit(label, (100, 100))
        self.surface.blit(score, (100, 120))
        pygame.display.flip()

        while True:
            for event in pygame.event.get():
                if event.type == KEYDOWN and event.key == K_RETURN:
                    SpaceInvadersGame(score=self.score, life=self.life)
                if (event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE) or
                        (event.type == KEYDOWN and event.key == K_n)):
                    exit()


    ## Here is the method, which is responsible for the termination of the game and exit to the main system.
    def game_exit(self):
        """ This function interrupts the action of the game and exit to the system"""
        exit()


     ## Here we add new method, which set our user.
    def draw_player(self):
        self.player = pygame.image.load("space_ship.png")
        self.speed = 1.2
        self.player_x = SCREEN_SIZE[0]/2 - 25
        self.player_y = SCREEN_SIZE[1] - 75


    ## Here we add method, which is responsible for updating player position.
    def move(self, dirx, diry):
        self.player_x = self.player_x + (dirx * self.speed)
        self.player_y = self.player_y + (diry * self.speed)


    ## This is the main loop of the game, which supports the shutdown event and escape key.
    ## Here also will be located service of our game and events
    def loop(self):
        """ Main loop of the game """
        can_shoot = True
        fire_wait = 500
        enemy_can_shoot = True
        enemy_fire_wait = 1500
        moving = False
        gamefont = pygame.font.Font(None, 20)

        while self.gamestate == 1:
            for event in pygame.event.get():
                if (event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE)):
                    self.game_exit()
            keys = pygame.key.get_pressed()

            if keys[K_RIGHT] and self.player_x < SCREEN_SIZE[0] - 50:
                self.move(1, 0)

            if keys[K_LEFT] and self.player_x > 0:
                self.move(-1, 0)

            if keys[K_SPACE] and can_shoot:
                bullet = Bullet(self.surface, self.player_x, self.player_y)
                self.bullets_array.append(bullet)
                can_shoot = False

            if not self.life:
                self.gamestate = 0

            if not can_shoot and fire_wait <= 0:
                can_shoot = True
                fire_wait = 500

            fire_wait -= CLOCK.tick(60)
            enemy_fire_wait -= CLOCK.tick(60)

            self.surface.fill((0, 0, 0))
            self.surface.blit(self.player, (self.player_x, self.player_y))

            for enemies in self.enemies_matrix:
                for enemy in enemies:
                    if enemies[-1].x > 765:
                        dirx = -1
                        moving = True
                        enemy.update(self.surface, 0, 5)
                    elif enemies[0].x < 0:
                        dirx = 1
                        moving = True
                        enemy.update(self.surface, 0, 5)
                    elif not moving:
                        dirx = 1
                    enemy.update(self.surface, dirx)

            if enemy_can_shoot:
                flat_list = [enemy for enemies in self.enemies_matrix for enemy in enemies]
                random_enemy = random.choice(flat_list)
                enemy_bullet = EnemyBullet(self.surface, random_enemy.x, random_enemy.y)
                self.enemies_bullets.append(enemy_bullet)
                enemy_can_shoot = False

            if not enemy_can_shoot and enemy_fire_wait <= 0:
                enemy_fire_wait = 1500
                enemy_can_shoot = True

            for enemy_bullet in self.enemies_bullets:
                enemy_bullet.update()
                if enemy_bullet > 600:
                    self.enemies_bullets.remove(enemy_bullet)

                if (check_collision(enemy_bullet.x, enemy_bullet.y, self.player_x, self.player_y) and
                    enemy_bullet in self.enemies_bullets
                ):
                    self.enemies_bullets.remove(enemy_bullet)
                    self.life -= 1

            for bullet in self.bullets_array:
                bullet.update()
                if bullet.y < 0:
                    self.bullets_array.remove(bullet)

                for enemies in self.enemies_matrix:
                    for enemy in enemies:
                        if (check_collision(bullet.x, bullet.y, enemy.x, enemy.y)
                            and bullet in self.bullets_array
                        ):
                            self.score += enemy.points
                            enemies.remove(enemy)
                            self.bullets_array.remove(bullet)

            score_label = gamefont.render("Score: {}".format(self.score), 1, YELLOW)
            self.surface.blit(score_label, (25, 575))

            life_label = gamefont.render("Life: {}".format(self.life), 1, YELLOW)
            self.surface.blit(life_label, (750, 575))

            pygame.display.flip()

            if not any(self.enemies_matrix):
                self.continue_screen()

        self.game_over_scren()


if __name__ == '__main__':
    SpaceInvadersGame()
