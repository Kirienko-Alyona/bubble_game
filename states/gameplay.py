import pygame
import random
from settings import *
from sprites import Particle
from levels import ObstacleGenerator


class Game:
    def __init__(self, screen, assets, game):
        self.screen = screen
        self.assets = assets
        self.game = game
        self.game_over = False
        self.victory = False
        self.passed_finish = False
        self.fade_alpha = 0
        self.fade_speed = 5
        self.particles = []

        self.font = assets["font"]
        self.bubble_radius = 20
        self.bubble_mask = self.create_circle_mask(self.bubble_radius)
        self.bubble_size = self.bubble_radius * 2
        self.bubble_sprite = pygame.transform.smoothscale(
            assets["bubble"], (self.bubble_size, self.bubble_size))
        self.bubble_x = WIDTH // 2
        self.bubble_y = HEIGHT - self.bubble_radius - 10
        self.bubble_speed_y = -2
        self.bubble_speed_x = 0
        self.bubble_acceleration = 1

        self.gap_width = self.bubble_radius * 4
        self.gap_x = random.randint(50, WIDTH - self.gap_width - 50)
        self.finish_y = 30
        self.finish_height = 10

        generator = ObstacleGenerator(
            self.bubble_radius, self.finish_y, self.finish_height, self.gap_x, self.gap_width)
        self.obstacles = generator.generate()

        self.button_rect = pygame.Rect(
            WIDTH // 2 - 100, HEIGHT // 2 + 60, 200, 50)

    def create_circle_mask(self, radius):
        size = radius * 2
        surface = pygame.Surface((size, size), pygame.SRCALPHA)
        pygame.draw.circle(surface, (255, 255, 255, 255),
                           (radius, radius), radius)
        return pygame.mask.from_surface(surface)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if self.game_over and (
                    event.type == pygame.MOUSEBUTTONDOWN and self.button_rect.collidepoint(event.pos) or
                    event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN):
                self.game.set_state('gameplay')

    def update(self):
        if self.game_over:
            return

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.bubble_speed_x = -self.bubble_acceleration
        elif keys[pygame.K_RIGHT]:
            self.bubble_speed_x = self.bubble_acceleration
        else:
            self.bubble_speed_x = 0

        bubble_speed_y_current = 0 if keys[pygame.K_LCTRL] or keys[pygame.K_RCTRL] else self.bubble_speed_y
        self.bubble_x += self.bubble_speed_x
        self.bubble_y += bubble_speed_y_current
        self.bubble_x = max(self.bubble_radius, min(
            WIDTH - self.bubble_radius, self.bubble_x))

        if not self.passed_finish and self.bubble_y - self.bubble_radius <= self.finish_y + self.finish_height:
            if not (self.gap_x < self.bubble_x < self.gap_x + self.gap_width):
                self.game_over = True
                self.victory = False
            else:
                self.passed_finish = True

        if self.passed_finish and self.bubble_y + self.bubble_radius < 0:
            self.game_over = True
            self.victory = True
            for _ in range(100):
                self.particles.append(Particle(WIDTH // 2, HEIGHT // 2))

        for obs in self.obstacles:
            obs_surface = pygame.Surface((obs.width, obs.height))
            obs_surface.fill(RED)
            obs_mask = pygame.mask.from_surface(obs_surface)
            offset = (int(obs.left - (self.bubble_x - self.bubble_radius)),
                      int(obs.top - (self.bubble_y - self.bubble_radius)))
            if self.bubble_mask.overlap(obs_mask, offset):
                self.game_over = True
                self.victory = False
                break

    def draw(self):
        if self.screen:  # перевірка, чи surface ще існує
            self.screen.blit(self.assets["background"], (0, 0))
        self.fade_alpha = min(255, self.fade_alpha + self.fade_speed)

        if self.game_over and not self.victory:
            self.screen.blit(self.assets["defeat"], (0, 0))
        elif self.victory:
            self.screen.blit(self.assets["victory"], (0, 0))

        self.screen.blit(self.bubble_sprite, (self.bubble_x -
                         self.bubble_radius, self.bubble_y - self.bubble_radius))

        for obs in self.obstacles:
            pygame.draw.rect(self.screen, RED, obs)

        pygame.draw.rect(self.screen, GREEN, (0, self.finish_y,
                         self.gap_x, self.finish_height))
        pygame.draw.rect(self.screen, GREEN, (self.gap_x + self.gap_width, self.finish_y,
                                              WIDTH - (self.gap_x + self.gap_width), self.finish_height))

        if self.game_over:
            label = self.font.render(
                "Перемога!" if self.victory else "Програш!", True, BLACK)
            self.screen.blit(label, (WIDTH // 2 - label.get_width() //
                             2, HEIGHT // 2 - label.get_height() // 2))

            mouse_pos = pygame.mouse.get_pos()
            pygame.draw.rect(self.screen, BLUE if self.button_rect.collidepoint(mouse_pos) else LIGHT_BLUE,
                             self.button_rect, border_radius=8)
            btn_text = self.font.render("Грати ще", True, WHITE)
            self.screen.blit(btn_text, (self.button_rect.centerx - btn_text.get_width() // 2,
                                        self.button_rect.centery - btn_text.get_height() // 2))

            for particle in self.particles[:]:
                particle.update()
                particle.draw(self.screen)
                if particle.life <= 0:
                    self.particles.remove(particle)
