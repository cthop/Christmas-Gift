import pygame


class Flash:
    def __init__(self, x, y, end_radius):
        self.x = x
        self.y = y
        self.end_radius = end_radius
        self.current_radius = 0
        self.brightness = 255

    def update(self):
        self.current_radius += 5
        self.brightness = max(0, 255 * (1 - self.current_radius / self.end_radius))

    def draw(self, screen):
        if self.current_radius < self.end_radius:
            surface = pygame.Surface((self.end_radius * 2, self.end_radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(surface, (self.brightness, self.brightness, self.brightness, self.brightness),
                               (self.end_radius, self.end_radius),
                               self.current_radius)
            screen.blit(surface, (self.x - self.end_radius, self.y - self.end_radius))

    def is_active(self):
        return self.current_radius < self.end_radius
