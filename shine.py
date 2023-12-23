import math
import random

import pygame


class Shine:
    def __init__(self, x, y, size_range=(0, 10), color=(255, 255, 255)):
        self.x, self.y = x, y
        self.size = size_range[0]
        self.max_size = random.uniform(1, size_range[1])
        self.shrinking = False
        self.dead = False
        self.color = color
        self.num_rays = 5

    def update(self):
        if self.shrinking:
            if self.size > 0:
                self.size -= 1
            else:
                self.dead = True
        else:
            if self.size < self.max_size:
                self.size += 1
            else:
                self.shrinking = True

    def draw(self, screen):
        if not self.dead:
            for i in range(self.num_rays):
                angle = (math.pi * 2 / self.num_rays) * i
                dx = self.size * math.cos(angle)
                dy = self.size * math.sin(angle)
                end_x = self.x + dx
                end_y = self.y + dy
                pygame.draw.line(screen, self.color, (self.x, self.y), (end_x, end_y), 2)
