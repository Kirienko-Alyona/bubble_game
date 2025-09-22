import pygame
import random
from settings import WIDTH, HEIGHT


class ObstacleGenerator:
    def __init__(self, bubble_radius, finish_y, finish_height, gap_x, gap_width, count=5):
        self.bubble_radius = bubble_radius
        self.finish_y = finish_y
        self.finish_height = finish_height
        self.gap_x = gap_x
        self.gap_width = gap_width
        self.count = count

        self.min_distance = bubble_radius * 4
        self.min_y = finish_y + finish_height
        self.max_y = HEIGHT - bubble_radius * 6
        self.gap_zone_top = finish_y
        self.gap_zone_bottom = finish_y + finish_height + bubble_radius * 4
        self.max_attempts = 1000

    def generate(self):
        obstacles = []
        attempts = 0

        while len(obstacles) < self.count and attempts < self.max_attempts:
            attempts += 1
            size = random.randint(40, 80)
            x = random.randint(0, WIDTH - size)
            y = random.randint(self.min_y, self.max_y - size)
            new_rect = pygame.Rect(x, y, size, size)

            if self._is_in_gap(new_rect):
                continue

            if self._is_valid(new_rect, obstacles):
                obstacles.append(new_rect)

        return obstacles

    def _is_in_gap(self, rect):
        in_gap_x = self.gap_x < rect.centerx < self.gap_x + self.gap_width
        in_gap_y = self.gap_zone_top <= rect.centery <= self.gap_zone_bottom
        return in_gap_x and in_gap_y

    def _is_valid(self, new_rect, obstacles):
        for obs in obstacles:
            dx = new_rect.centerx - obs.centerx
            dy = new_rect.centery - obs.centery
            dist = (dx**2 + dy**2) ** 0.5
            if dist < self.min_distance + max(new_rect.width, obs.width) / 2:
                return False
        return True
