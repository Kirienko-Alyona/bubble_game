import pygame
import sys
import random

from particle import Particle

# Ініціалізація
pygame.init()

# Розміри вікна
WIDTH, HEIGHT = 500, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Мильна бульбашка")

# Завантаження зображення бульбашки
bubble_img = pygame.image.load("bubble.png").convert_alpha()
background_img = pygame.image.load("background.png").convert_alpha()
background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))

victory_bg = pygame.image.load("victory_background.png").convert_alpha()
victory_bg = pygame.transform.scale(victory_bg, (WIDTH, HEIGHT))

defeat_bg = pygame.image.load("defeat_background.png").convert_alpha()
defeat_bg = pygame.transform.scale(defeat_bg, (WIDTH, HEIGHT))

# Кольори
WHITE = (255, 255, 255)
BLUE = (100, 200, 255)
BLACK = (0, 0, 0)
RED = (200, 50, 50)
GRAY = (200, 200, 200)
DARK_GRAY = (200, 200, 200)
GREEN = (50, 200, 50)
LIGHT_BLUE = (150, 220, 255)
PINK = (255, 182, 193)
YELLOW = (255, 252, 194)
# BEIGE = (255, 239, 213)
BEIGE = (252, 252, 252)


# Шрифт
font = pygame.font.SysFont("Arial", 36)

# Функція для створення перешкод


def generate_obstacles(bubble_radius, finish_y, finish_height, gap_x, gap_width, count=5):
    obstacles = []
    min_distance = bubble_radius * 4  # подвійний діаметр

    # Межі по вертикалі
    min_y = finish_y + finish_height
    max_y = HEIGHT - bubble_radius * 6

    gap_zone_top = finish_y
    gap_zone_bottom = finish_y + finish_height + bubble_radius * 4  # 2 діаметри

    attempts = 0
    max_attempts = 1000  # захист від зациклення

    while len(obstacles) < count and attempts < max_attempts:
        attempts += 1
        size = random.randint(40, 80)
        x = random.randint(0, WIDTH - size)
        y = random.randint(min_y, max_y - size)

        new_rect = pygame.Rect(x, y, size, size)

        # Перевірка: квадрат не повинен бути під розривом
        in_gap_x = gap_x < new_rect.centerx < gap_x + gap_width
        in_gap_y = gap_zone_top <= new_rect.centery <= gap_zone_bottom

        if in_gap_x and in_gap_y:
            continue  # пропускаємо цей квадрат

        # перевірка відстані до всіх існуючих квадратів
        valid = True
        for obs in obstacles:
            dx = (new_rect.centerx - obs.centerx)
            dy = (new_rect.centery - obs.centery)
            dist = (dx**2 + dy**2) ** 0.5
            if dist < min_distance + max(size, obs.width) / 2:
                valid = False
                break

        if valid:
            obstacles.append(new_rect)

    return obstacles


def circle_rect_collision(circle_x, circle_y, radius, rect):
    # Знаходимо найближчу точку на прямокутнику до центру кола
    closest_x = max(rect.left, min(circle_x, rect.right))
    closest_y = max(rect.top, min(circle_y, rect.bottom))

    # Відстань між центром кола і цією точкою
    dx = circle_x - closest_x
    dy = circle_y - closest_y

    return (dx**2 + dy**2) < radius**2


def create_circle_mask(radius):
    size = radius * 2
    surface = pygame.Surface((size, size), pygame.SRCALPHA)
    pygame.draw.circle(surface, (255, 255, 255, 255), (radius, radius), radius)
    return pygame.mask.from_surface(surface)


# Функція для запуску гри

def run_game():
    particles = []

    # Налаштування бульбашки
    bubble_radius = 20
    bubble_mask = create_circle_mask(bubble_radius)
    bubble_size = bubble_radius * 2
    bubble_sprite = pygame.transform.smoothscale(
        bubble_img, (bubble_size, bubble_size))
    bubble_x = WIDTH // 2
    bubble_y = HEIGHT - bubble_radius - 10
    bubble_speed_y = -2
    bubble_speed_x = 0
    bubble_acceleration = 1

    # Мерехтіння кулі
    # rotation_angle = 0
    # rotation_speed = 1.5  # градусів за кадр
    # if bubble_speed_x != 0:
    #     rotation_speed = 6.0
    # else:
    #     rotation_speed = 2.0

    # Фінішна лінія з розривом
    gap_width = bubble_radius * 4   # подвійний діаметр
    gap_x = random.randint(50, WIDTH - gap_width - 50)
    finish_y = 30
    finish_height = 10

    # Генерація перешкод з урахуванням фінішної лінії
    obstacles = generate_obstacles(
        bubble_radius, finish_y, finish_height, gap_x, gap_width, count=5)

    running = True
    clock = pygame.time.Clock()
    game_over = False
    victory = False

    # Кнопка "Грати ще"
    button_width, button_height = 200, 50
    button_rect = pygame.Rect(
        WIDTH//2 - button_width//2, HEIGHT//2 + 60, button_width, button_height)

    passed_finish = False  # прапорець, що куля пройшла через розрив

    # Ефект згасання екрану
    fade_alpha = 0
    fade_speed = 5  # чим більше — тим швидше згасання

    while running:
        clock.tick(60)
        WIN.blit(background_img, (0, 0))

        game_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)

        fade_alpha = min(255, fade_alpha + fade_speed)
        fade_surface = pygame.Surface((WIDTH, HEIGHT))
        fade_surface.set_alpha(fade_alpha)

        if game_over and not victory:
            WIN.blit(defeat_bg, (0, 0))
        elif victory:
            WIN.blit(victory_bg, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if game_over:
                if event.type == pygame.MOUSEBUTTONDOWN and button_rect.collidepoint(event.pos):
                    return  # Перезапуск гри по кліку миші

                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    return  # Перезапуск гри по Enter

        keys = pygame.key.get_pressed()
        if not game_over:
            if keys[pygame.K_LEFT]:
                bubble_speed_x = -bubble_acceleration
            elif keys[pygame.K_RIGHT]:
                bubble_speed_x = bubble_acceleration
            else:
                bubble_speed_x = 0

            # Обробка клавіш
            ctrl_held = keys[pygame.K_LCTRL] or keys[pygame.K_RCTRL]

            if keys[pygame.K_LEFT]:
                bubble_speed_x = -bubble_acceleration
            elif keys[pygame.K_RIGHT]:
                bubble_speed_x = bubble_acceleration
            else:
                bubble_speed_x = 0

            # Якщо Ctrl натиснуто — вертикальний рух зупиняється
            if ctrl_held:
                bubble_speed_y_current = 0
            else:
                bubble_speed_y_current = bubble_speed_y

            # Рух бульбашки
            bubble_x += bubble_speed_x
            bubble_y += bubble_speed_y_current

            # Межі екрану
            if bubble_x - bubble_radius < 0:
                bubble_x = bubble_radius
            if bubble_x + bubble_radius > WIDTH:
                bubble_x = WIDTH - bubble_radius

            # Перевірка перетину з фінішною лінією
            if not passed_finish and bubble_y - bubble_radius <= finish_y + finish_height:
                # Якщо куля не у розриві → програш
                if not (gap_x < bubble_x < gap_x + gap_width):
                    game_over = True
                    victory = False
                else:
                    passed_finish = True  # куля пройшла крізь розрив

            # Якщо пройшла розрив і зникла за полем → перемога
            if passed_finish and bubble_y + bubble_radius < 0:
                game_over = True
                victory = True
                for _ in range(100):
                    particles.append(
                        Particle(WIDTH // 2, HEIGHT // 2))

            # Зіткнення з квадратами
            for obs in obstacles:
                obs_surface = pygame.Surface((obs.width, obs.height))
                obs_surface.fill(RED)
                obs_mask = pygame.mask.from_surface(obs_surface)

                offset_x = int(obs.left - (bubble_x - bubble_radius))
                offset_y = int(obs.top - (bubble_y - bubble_radius))

                if bubble_mask.overlap(obs_mask, (offset_x, offset_y)):
                    game_over = True
                    victory = False
                    break

            # # Оновлення позиції бульбашки МЕРЕХТІННЯ БУЛЬБАШКИ
            # rotation_angle = (rotation_angle + rotation_speed) % 360
            # rotated_sprite = pygame.transform.rotate(
            #     bubble_sprite, rotation_angle)

            # # Щоб центр залишався вірним, треба змістити позицію
            # rotated_rect = rotated_sprite.get_rect(center=(bubble_x, bubble_y))
            # WIN.blit(rotated_sprite, rotated_rect.topleft)

        # Малювання
        WIN.blit(bubble_sprite, (bubble_x -
                 bubble_radius, bubble_y - bubble_radius))

        for obs in obstacles:
            pygame.draw.rect(WIN, RED, obs)

        # Малюємо фінішну лінію з розривом
        pygame.draw.rect(WIN, GREEN, (0, finish_y, gap_x,
                         finish_height))  # ліва частина
        pygame.draw.rect(WIN, GREEN, (gap_x + gap_width, finish_y,
                         WIDTH - (gap_x + gap_width), finish_height))  # права частина

        if game_over:
            text = "Перемога!" if victory else "Програш!"
            label = font.render(text, True, BLACK)
            WIN.blit(label, (WIDTH // 2 - label.get_width() // 2,
                             HEIGHT // 2 - label.get_height() // 2))

            # Малюємо кнопку
            mouse_pos = pygame.mouse.get_pos()
            if button_rect.collidepoint(mouse_pos):
                pygame.draw.rect(WIN, BLUE, button_rect, border_radius=8)
            else:
                pygame.draw.rect(WIN, LIGHT_BLUE, button_rect, border_radius=8)

            btn_text = font.render("Грати ще", True, WHITE)
            WIN.blit(btn_text, (button_rect.centerx - btn_text.get_width() // 2,
                                button_rect.centery - btn_text.get_height() // 2))

            for particle in particles[:]:
                particle.update()
                particle.draw(WIN)
                if particle.life <= 0:
                    particles.remove(particle)

        pygame.display.update()


# Цикл запуску гри з кнопкою перезапуску
while True:
    run_game()
