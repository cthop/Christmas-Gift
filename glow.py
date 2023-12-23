import pygame


class Glow:
    def __init__(self, x, y, max_radius, color, num_layers=10):
        self.x = x
        self.y = y
        self.max_radius = max_radius
        self.color = color
        self.num_layers = num_layers

    def draw(self, surface):
        for i in range(self.num_layers, 0, -1):
            radius = self.max_radius * (i / self.num_layers)
            alpha = int(20 * (1 - (i / self.num_layers)))
            temp_surface = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(temp_surface, self.color + (alpha,), (radius, radius), radius)
            surface.blit(temp_surface, (self.x - radius, self.y - radius))