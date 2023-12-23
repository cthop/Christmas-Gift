import random
import math
from ball import Ball

TWO_PI = 2 * math.pi


class IdleBall(Ball):
    def __init__(self, x, y, color, size, angle_step=0.01):
        super().__init__(x, y, color, size)
        self.angle = random.uniform(0, 1)
        self.angle_step = angle_step

        self.original_x = x
        self.original_y = y
        self.original_angle_step = angle_step

        self.size_x, self.size_y = 100, 100

    def update(self):
        # Increment the angle
        self.angle += self.angle_step
        # Calculate the new x and y positions
        self.x = self.original_x + math.sin(self.angle * TWO_PI) * self.size_x
        self.y = self.original_y + math.cos(self.angle * TWO_PI) * math.sin(self.angle * TWO_PI) * self.size_y

        if self.angle > 1:
            self.angle -= 1
            self.angle_step = self.original_angle_step + random.uniform(-0.3 * self.angle_step, 0.3 * self.angle_step)
            self.size_x = random.uniform(50, 150)
            self.size_y = random.uniform(50, 150)
