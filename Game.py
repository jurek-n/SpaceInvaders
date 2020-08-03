import pygame
from pygame.locals import *
from game_obj import Ship, Projectile, Enemy
from random import randint


class Game:
    def __init__(self):
        self._running = True
        self._display_surf = None
        self.size = self.width, self.height = 640, 400
        self.ship = Ship(200, 64, 64)
        self.bg_img = pygame.image.load('space_bg.jpg')
        self.icon_img = pygame.image.load('space_icon_32.png')
        self.keys = list()
        self.mouse = list()
        self.mouse_coord = tuple()
        self.enemies = list()
        self.enemies_tick = 400
        self._temp_e_t = 0
        self.clock = pygame.time.Clock()
        self.score = 0
        self.font = None
        self.font_2 = None
        self.text_score = None
        self.text_game_over = None
        self.text_menu = ["New Game", "Scoreboard", "Exit"]
        self.game_over = False
        self.game_over_tick = 600
        self._temp_g_o = 0
        self._menu = True
        self._menu_rect = [(220, 100, 200, 45), (220, 200, 200, 45), (220, 300, 200, 45)]
        self._menu_color_flag = [False, False, False]
        self._colors = ((255, 0, 0), (0, 128, 0))

    def __reset(self):
        self.enemies = []
        self.enemies_tick = 400
        self._temp_e_t = 0
        self.clock = pygame.time.Clock()
        self.score = 0
        self.game_over = False
        self.game_over_tick = 600
        self._temp_g_o = 0
        self.ship.health = 3

    def on_init(self):
        pygame.init()
        pygame.display.set_icon(self.icon_img)
        self._display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self._display_surf.blit(self.bg_img, (0, 0))
        self.font = pygame.font.SysFont('comicsans', 30, True, False)
        self.font_2 = pygame.font.SysFont('comicsans', 30, True, False)
        self._running = True
        return self._running

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False

    def __gen_enemy(self):
        temp = randint(25, self.height - 64)
        if self._temp_e_t == self.enemies_tick:
            self.enemies.append(Enemy(temp, 40, 64))
            self._temp_e_t = 0
        else:
            self._temp_e_t += 1

    def __draw_enemies(self):
        for enemy in self.enemies:
            if enemy.x > -40:
                enemy.move()
                enemy.draw(self._display_surf)
            else:
                self.enemies.pop(self.enemies.index(enemy))

    def __clear_enemy(self, enemy):
        self.enemies.pop(self.enemies.index(enemy))

    def __check_bullets(self):
        for bullet in self.ship.bullets:
            for enemy in self.enemies:
                if enemy.hit_box[1] < bullet.y < enemy.hit_box[1] + enemy.hit_box[3] and enemy.hit_box[0] < bullet.x < enemy.hit_box[0] + enemy.hit_box[2]:
                    enemy.hit(10)
                    self.ship.clear_bullet(bullet)
                    if enemy.health == 0:
                        self.__clear_enemy(enemy)
                        self.score += 1

    def __check_enemies(self):
        for enemy in self.enemies:
            if enemy.hit_box[0] < -20 or (self.ship.x + self.ship.width > enemy.hit_box[0] and self.ship.y - enemy.hit_box[3] < enemy.hit_box[1] < self.ship.y + self.ship.height):
                self.ship.hit()
                self.__clear_enemy(enemy)
                if self.ship.health == 0:
                    self.enemies.clear()
                    self.ship.bullets.clear()
                    self.game_over = True

    def on_loop(self):
        if not self.game_over and not self._menu:
            self.keys = pygame.key.get_pressed()
            if self.keys[pygame.K_UP] and self.ship.y > 25:
                self.ship.move(1)
            if self.keys[pygame.K_DOWN] and self.ship.y < self.height - self.ship.height:
                self.ship.move(-1)
            if self.keys[pygame.K_SPACE]:
                self.ship.shoot()
            self.__gen_enemy()
            self.__check_bullets()
            self.__check_enemies()
        if self._menu:
            self.mouse = pygame.mouse.get_pressed()
            self.mouse_coord = pygame.mouse.get_pos()
            for rect in self._menu_rect:
                temp = self._menu_rect.index(rect)
                if rect[0] < self.mouse_coord[0] < rect[0] + rect[2] and rect[1] < self.mouse_coord[1] < rect[1] + rect[3]:
                    self._menu_color_flag[temp] = True
                    if self.mouse[0] and temp == 0:
                        self._menu = False
                        self.game_over = False
                    if self.mouse[0] and temp == 1:
                        pass
                    if self.mouse[0] and temp == 2:
                        self._running = False
                        print(self._running)
                else:
                    self._menu_color_flag[self._menu_rect.index(rect)] = False

    def __draw_menu_rect(self, menu_bool):
        for i in range(len(self._menu_rect)):
            if self._menu_color_flag[i]:
                pygame.draw.rect(self._display_surf, self._colors[0], self._menu_rect[i])
                pygame.draw.rect(self._display_surf, (0, 0, 0), self._menu_rect[i], 5)
            else:
                pygame.draw.rect(self._display_surf, self._colors[1], self._menu_rect[i])
                pygame.draw.rect(self._display_surf, (0, 0, 0), self._menu_rect[i], 5)
            self.text_score = self.font.render(self.text_menu[i], 1, (0, 0, 0))
            self._display_surf.blit(self.text_score, (240, 102 * (i + 1)))

    def _menu_disp(self):
        self._display_surf.blit(self.bg_img, (0, 0))
        self.ship.draw(self._display_surf)
        self.__draw_menu_rect(self._menu_color_flag)

    def _game_disp(self):
        self._display_surf.blit(self.bg_img, (0, 0))
        self.ship.draw(self._display_surf)
        self.__draw_enemies()
        self.text_score = self.font.render("Score: " + str(self.score), 1, (0, 0, 0))
        self._display_surf.blit(self.text_score, (520, 5))

    def _game_over_disp(self):
        self._display_surf.blit(self.bg_img, (0, 0))
        self.text_game_over = self.font_2.render("You lose !!!", 1, (0, 0, 0))
        self._display_surf.blit(self.text_game_over, (250, 170))
        self.text_game_over = self.font_2.render("Your score: " + str(self.score), 1, (0, 0, 0))
        self._display_surf.blit(self.text_game_over, (270, 150))
        self.ship.draw(self._display_surf)
        self._temp_g_o += 1
        if self._temp_g_o == self.game_over_tick:
            self.__reset()
            self._menu = True

    def on_render(self):
        if self.game_over:
            self._game_over_disp()
        elif self._menu:
            self._menu_disp()
        elif not self.game_over and not self._menu:
            self._game_disp()
        pygame.display.update()

    @staticmethod
    def on_cleanup():
        pygame.quit()

    def on_execute(self):
        if not self.on_init():
            self._running = False
        while self._running:
            self.clock.tick(80)
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
        self.on_cleanup()
