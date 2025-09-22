import pygame
import random


class Particle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = random.randint(2, 5)
        self.color = random.choice([
            (255, 0, 0), (255, 255, 0), (0, 255, 0),
            (0, 255, 255), (0, 0, 255), (255, 0, 255)
        ])
        self.speed_x = random.uniform(-3, 3)
        self.speed_y = random.uniform(-3, 3)
        self.life = 60

    def update(self):
        self.x += self.speed_x
        self.y += self.speed_y
        self.life -= 1
        self.radius = max(0, self.radius - 0.05)

    def draw(self, surface):
        if self.life > 0:
            pygame.draw.circle(surface, self.color, (int(
                self.x), int(self.y)), int(self.radius))
