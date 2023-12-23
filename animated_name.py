import pygame
import random

class AnimatedName:
    def __init__(self, name, start_position, duration, font_size, color=(255, 255, 255)):
        self.name = name
        self.position = start_position
        self.duration = duration
        self.start_time = pygame.time.get_ticks()
        self.font_size = font_size
        self.color = color
        self.visible = True

    def update(self):
        current_time = pygame.time.get_ticks()
        elapsed = current_time - self.start_time

        if elapsed > self.duration:
            self.visible = False

        self.position = (self.position[0], self.position[1] - random.uniform(1, 5))

    def draw(self, screen):
        if self.visible:
            font = pygame.font.Font(None, self.font_size)
            text = font.render(self.name, True, self.color)
            text_rect = text.get_rect(center=self.position)
            screen.blit(text, text_rect)
