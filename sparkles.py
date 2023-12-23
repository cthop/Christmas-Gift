import random
from particle import Particle


class Sparkles:
    def __init__(self, tracked_object):
        self.tracked_object = tracked_object
        self.particles = []

    def emit(self, rate):
        # Generate new particles
        if random.random() < rate:
            return
        for _ in range(random.randint(2, 5)):
            particle = Particle(self.tracked_object.x, self.tracked_object.y)
            self.particles.append(particle)

    def update(self, delta_time, rate=0.7):
        self.emit(rate)  # Emit new particles
        for particle in self.particles:
            particle.update(delta_time)
        self.particles = [p for p in self.particles if p.lifespan > 0]

    def draw(self, screen):
        for particle in self.particles:
            particle.draw(screen)
