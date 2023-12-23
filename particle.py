import colorsys
import math
import random

import pygame


class Particle:
    def __init__(self, x, y, size=5):
        self.x = x
        self.y = y
        self.size = size
        self.color = self.randomize_brightness((255, 215, 0))  # Golden yellow/white color
        self.lifespan = random.uniform(1, 30)  # Lifespan in seconds
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(2, 5)
        self.velocity = [speed * math.cos(angle), speed * math.sin(angle)]
        self.gravity = 0.1  # Gravity effect
        self.drag = 0.99  # Drag effect

    def randomize_brightness(self, color):
        """ Randomize the brightness of the given color using HLS color space """
        # Convert RGB color to a scale of 0-1
        r, g, b = [x / 255.0 for x in color]

        # Convert RGB to HLS
        h, l, s = colorsys.rgb_to_hls(r, g, b)

        # Randomize the lightness while keeping the hue and saturation constant
        l = max(0.0, min(1.0, l * random.uniform(0.8, 1.2)))

        # Convert back to RGB
        new_r, new_g, new_b = colorsys.hls_to_rgb(h, l, s)

        # Convert back to the scale of 0-255
        return int(new_r * 255), int(new_g * 255), int(new_b * 255)

    def update(self, delta_time):
        # Apply velocity to position
        self.x += self.velocity[0] * delta_time
        self.y += self.velocity[1] * delta_time

        # Apply gravity
        self.velocity[1] += self.gravity

        # Apply drag
        self.velocity[0] *= self.drag
        self.velocity[1] *= self.drag

        # Decrease lifespan
        self.lifespan -= delta_time

        # Randomize color brightness
        self.color = self.randomize_brightness(self.color)

        # Decrease size
        self.size = max(0, self.size - (0.1 * delta_time))

    def draw(self, screen):
        if self.lifespan > 0:
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), int(self.size))