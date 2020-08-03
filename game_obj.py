import pygame
from pygame.locals import *


class Ship(object):
    def __init__(self, y, width, height):
        self.x = 0
        self.y = y
        self.width = width
        self.height = height
        self.vel = 2
        self.img = pygame.image.load("pngwave.png")
        self.heart_img = pygame.image.load("heart_20.png")
        self.hit_box = (self.x, self.y, self.width, self.height)
        self.health = 3
        self.bullets = []
        self.bullet_tick = 0
        self._temp_b_t = 0

    def move(self, dir_flag):
        if dir_flag == 1:
            self.y -= self.vel
        elif dir_flag == -1:
            self.y += self.vel
        self.hit_box = (self.x, self.y, self.width, self.height)

    def shoot(self):
        if self._temp_b_t == self.bullet_tick:
            self.bullets.append(Projectile(self.y))
            self._temp_b_t += 1
        else:
            self._temp_b_t += 1
            if self._temp_b_t == 15:
                self._temp_b_t = self.bullet_tick

    def draw(self, win):
        win.blit(self.img, (self.x, self.y))
        if self.health > 0:
            for i in range(self.health):
                win.blit(self.heart_img, (5 + (i * 20), 5))
        # pygame.draw.rect(win, (255, 0, 0), self.hit_box, 2)
        self.__draw_bullets(win)

    def __draw_bullets(self, win):
        for bullet in self.bullets:
            if bullet.x < 640:
                bullet.move()
                bullet.draw(win)
            else:
                self.clear_bullet(bullet)

    def clear_bullet(self, bullet):
        self.bullets.pop(self.bullets.index(bullet))

    def hit(self):
        self.health -= 1


class Projectile(object):
    def __init__(self, y, color=(255, 255, 255), radius=3):
        self.x = 64
        self.y = y + 32
        self.color = color
        self.radius = radius
        self.vel = 5
        self.tick = 3

    def move(self):
        self.x += self.vel

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)


class Enemy(object):
    def __init__(self, y, width, height):
        self.x = 640
        self.y = y
        self.width = width
        self.height = height
        self.vel = 1
        self.img = pygame.image.load("spaceship_enemy_64.png")
        self.hit_box = (self.x, self.y, self.width, self.height)
        self.health = 40
        self.health_bar_red = (self.x, self.y - 10, 40, 10)
        self.health_bar_green = (self.x, self.y - 10, self.health, 20)

    def move(self):
        self.x -= self.vel
        self.hit_box = (self.x, self.y, self.width, self.height)
        self.health_bar_red = (self.x, self.y - 10, 40, 10)
        self.health_bar_green = (self.x, self.y - 10, self.health, 10)

    def draw(self, win):
        win.blit(self.img, (self.x, self.y))
        # pygame.draw.rect(win, (255, 0, 0), self.hit_box)
        pygame.draw.rect(win, (255, 0, 0), self.health_bar_red)
        pygame.draw.rect(win, (0, 128, 0), self.health_bar_green)
        pygame.draw.rect(win, (0, 0, 0), self.health_bar_red, 1)

    def hit(self, dmg):
        if self.health - dmg < 0:
            self.health = 0
        else:
            self.health -= dmg
