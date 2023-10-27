from parametres import *
import pygame
import math

class Player:
    def __init__(self):
        self.x, self.y = player_position
        self.angle = angle_of_player

    @property
    def get_position(self):
        return (self.x, self.y)

    def movement(self):                 #выстраиваем движение игрока в зависимости от нажатых клавиш
        sinA = math.sin(self.angle)
        cosA = math.cos(self.angle)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.x += speed_of_player * cosA
            self.y += speed_of_player * sinA
        if keys[pygame.K_s]:
            self.x += -speed_of_player * cosA
            self.y += -speed_of_player * sinA
        if keys[pygame.K_a]:
            self.x += speed_of_player * sinA
            self.y += -speed_of_player * cosA
        if keys[pygame.K_d]:
            self.x += -speed_of_player * sinA
            self.y += speed_of_player * cosA
        if keys[pygame.K_LEFT]:
            self.angle -= 0.02
        if keys[pygame.K_RIGHT]:
            self.angle += 0.02
