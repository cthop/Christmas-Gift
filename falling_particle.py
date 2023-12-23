import random

import pygame


class FallingParticle:
    def __init__(self, x, y, color, speed):
        self.x = x
        self.y = y
        self.color = color
        self.speed = speed

    def update(self, screen_width, screen_height):
        self.y += self.speed
        if self.y > screen_height:
            self.y = -10
            self.x = random.randint(0, screen_width)

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), 3)
