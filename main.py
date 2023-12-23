import random
import pygame
import math
from button import Button
from idle_ball import IdleBall
from flash import Flash
from sparkles import Sparkles
from ball import Ball
from shine import Shine
from falling_particle import FallingParticle
from glow import Glow
from animated_name import AnimatedName
import datetime

TWO_PI = 2 * math.pi


def idle_particles(time_seconds):
    border_padding = 0.2
    left_x, left_y = screen_width * border_padding, screen_height * (1 - border_padding)
    right_x, right_y = screen_width * (1 - border_padding), screen_height * (1 - border_padding)
    ball_size = 10
    balls = [IdleBall(left_x, left_y, (214, 0, 28), ball_size), IdleBall(right_x, right_y, (0, 135, 62), ball_size)]
    sparkles = [Sparkles(ball) for ball in balls]
    start_time = pygame.time.get_ticks()
    while pygame.time.get_ticks() - start_time < time_seconds * 1000:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        screen.fill((0, 0, 0))  # Clear the screen

        # Draw and update all balls
        for ball, sparkle in zip(balls, sparkles):
            sparkle.draw(screen)
            sparkle.update(0.1)
            ball.draw(screen)
            ball.update()

        pygame.display.update()
        clock.tick(60)

    balls = [Ball(ball.x, ball.y, ball.color, ball.size) for ball in balls]
    sparkles = [Sparkles(ball) for ball in balls]
    return balls, sparkles


def calculate_bezier_point(t, P0, P1, P2):
    """ Calculate a point on a quadratic Bezier curve """
    # Element-wise operations for each point
    x = ((1 - t) ** 2) * P0[0] + 2 * (1 - t) * t * P1[0] + (t ** 2) * P2[0]
    y = ((1 - t) ** 2) * P0[1] + 2 * (1 - t) * t * P1[1] + (t ** 2) * P2[1]
    return x, y


def lerp(start, end, t):
    """ Linearly interpolate between start and end values """
    return start + (end - start) * t


def calculate_distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def start_helical_convergence(balls, sparkles, time_bezier, time_helical):
    start_time = pygame.time.get_ticks()
    total_time = time_bezier + time_helical

    first_x, first_y = screen_width // 2, screen_height * 0.9
    second_x, second_y = screen_width // 2, screen_height * 0.1

    P0 = [(ball.x, ball.y) for ball in balls]
    P1 = [(screen_width // 2, screen_height // 2) for _ in balls]
    P2 = [(first_x, first_y) for _ in balls]

    start_amplitude = 1000
    end_amplitude = 0
    start_frequency = 1
    end_frequency = 10
    phase = 0

    active_flashes = []

    while pygame.time.get_ticks() - start_time < total_time * 1000:
        current_time = pygame.time.get_ticks() - start_time

        bezier_end_time = time_bezier * 1000
        helical_start_time = bezier_end_time
        helical_end_time = bezier_end_time + time_helical * 1000

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        screen.fill((0, 0, 0))

        for index, (ball, sparkle) in enumerate(zip(balls, sparkles)):
            if current_time < bezier_end_time:
                bezier_t = current_time / bezier_end_time
                ball.x, ball.y = calculate_bezier_point(bezier_t, P0[index], P1[index], P2[index])

            elif helical_start_time <= current_time < helical_end_time:
                sinusoidal_t = (current_time - helical_start_time) / (time_helical * 1000)
                current_amplitude = lerp(start_amplitude, end_amplitude, sinusoidal_t)
                current_frequency = lerp(start_frequency, end_frequency, sinusoidal_t ** 0.5)
                sinusoidal_y = lerp(first_y, second_y, sinusoidal_t)
                sinusoidal_x = first_x + current_amplitude * math.sin(
                    2 * math.pi * current_frequency * sinusoidal_t + phase) * (-1 if index % 2 else 1)
                ball.x, ball.y = sinusoidal_x, sinusoidal_y

            sparkle.draw(screen)
            sparkle.update(0.1)
            ball.draw(screen)
            ball.update()

        if helical_start_time <= current_time < helical_end_time:
            for i in range(len(balls)):
                for j in range(i + 1, len(balls)):
                    if calculate_distance(balls[i].x, balls[i].y, balls[j].x, balls[j].y) < (balls[i].size * 10):
                        collision_x, collision_y = (balls[i].x + balls[j].x) / 2, (balls[i].y + balls[j].y) / 2
                        flash = Flash(collision_x, collision_y, 200)
                        active_flashes.append(flash)

        # Update and draw active flashes
        for flash in active_flashes[:]:
            flash.update()
            flash.draw(screen)
            if not flash.is_active():
                active_flashes.remove(flash)
        pygame.display.update()
        clock.tick(60)


def draw_christmas_tree(alpha, x, y):
    tree_image = pygame.image.load('tree.png')
    tree_image = pygame.transform.scale(tree_image, (screen_width, screen_height))
    tree_image.set_alpha(alpha)
    screen.blit(tree_image, (x, y))


def explosion_effect(time_seconds):
    flash_duration = time_seconds * 1000  # duration of the flash in milliseconds
    start_time = pygame.time.get_ticks()
    tree_x, tree_y = 0, 0

    while pygame.time.get_ticks() - start_time < flash_duration:
        elapsed_time = pygame.time.get_ticks() - start_time
        alpha = int(max(255 - (255 * (elapsed_time / flash_duration)), 0))

        reveal_scene(255 - alpha, tree_x, tree_y)

        # Create a flash bang
        flash_surface = pygame.Surface((screen.get_width(), screen.get_height()))
        flash_surface.set_alpha(alpha)
        flash_surface.fill((255, 255, 255))
        screen.blit(flash_surface, (0, 0))

        pygame.display.update()
        clock.tick(60)


def reveal_scene(alpha, x, y):
    screen.fill((255, 255, 255))  # Optional: Fill the screen to clear previous drawings
    draw_christmas_tree(alpha, x, y)


def load_tree_image():
    tree_image = pygame.image.load('tree.png')
    tree_image = pygame.transform.scale(tree_image, (screen_width, screen_height))
    return tree_image


def get_tree_coordinates(tree_image):
    tree_coordinates = []
    for x in range(tree_image.get_width()):
        for y in range(tree_image.get_height()):
            if tree_image.get_at((x, y)) != (0, 0, 0, 0):  # Assuming non-black pixels are part of the tree
                tree_coordinates.append((x, y))
    return tree_coordinates


def end_game():
    end_x = 1645
    end_y = 1028

    plushy_bounding_box = {
        "top_left": (int(534 / end_x * screen_width), int(802 / end_y * screen_height)),
        "top_right": (int(614 / end_x * screen_width), int(802 / end_y * screen_height)),
        "bottom_left": (int(534 / end_x * screen_width), int(909 / end_y * screen_height)),
        "bottom_right": (int(614 / end_x * screen_width), int(909 / end_y * screen_height)),
    }

    names = [
        "Dudu", "Doodoo", "Dudoo", "Doodu", "Doo-Doo", "Du-Du", "Doudou",
        "Doodo", "Duudo", "Doodou", "Duduoo", "Duudoo", "Doodoou",
        "Dooudoo", "Doudoo", "Duudou", "Duoodoo"
    ]

    tree_image = load_tree_image()
    tree_coordinates = get_tree_coordinates(tree_image)

    shines = [Shine(x, y) for x, y in random.sample(tree_coordinates, 5)]

    sparkles = [FallingParticle(random.randint(0, screen_width), random.randint(-screen_height, 0),
                                random.choice([(255, 0, 0), (0, 255, 0)]), random.uniform(1, 4)) for _ in range(100)]

    glow = Glow(screen_width // 2, screen_height * 0.1, 500, (255, 255, 0), 10)

    hover_effect_active = False
    hover_color_overlay = pygame.Surface((plushy_bounding_box["top_right"][0] - plushy_bounding_box["top_left"][0],
                                          plushy_bounding_box["bottom_left"][1] - plushy_bounding_box["top_left"][1]))
    hover_color_overlay.set_alpha(128)  # Adjust transparency
    hover_color_overlay.fill((200, 200, 200))  # Darkened color for hover effect

    animated_names = []

    while True:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        # Check if mouse is inside the bounding box
        inside_bounding_box = ((plushy_bounding_box["top_left"][0] <= mouse_x <= plushy_bounding_box["top_right"][0])
                               and
                               (plushy_bounding_box["top_left"][1] <= mouse_y <= plushy_bounding_box["bottom_left"][1]))

        if inside_bounding_box and not hover_effect_active:
            hover_effect_active = True
        elif not inside_bounding_box and hover_effect_active:
            hover_effect_active = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN and inside_bounding_box:
                spawn_x = random.randint(plushy_bounding_box["top_left"][0], plushy_bounding_box["top_right"][0])
                spawn_y = random.randint(plushy_bounding_box["top_left"][1], plushy_bounding_box["bottom_left"][1])
                spawn_position = (spawn_x, spawn_y)
                selected_name = random.choice(names) + '?'
                animated_names.append(AnimatedName(selected_name, spawn_position, duration=1000, font_size=36))

        reveal_scene(255, 0, 0)

        for sparkle in sparkles:
            sparkle.update(screen_width, screen_height)
            sparkle.draw(screen)

        for shine in shines[:]:
            shine.update()
            shine.draw(screen)
            if shine.dead:
                shines.remove(shine)

        if len(shines) < 2:
            shines.extend([Shine(x, y) for x, y in random.sample(tree_coordinates, random.randint(1, 10))])

        glow.draw(screen)

        if hover_effect_active:
            screen.blit(hover_color_overlay, plushy_bounding_box["top_left"])

        for animated_name in animated_names[:]:  # Iterate over a copy of the list
            animated_name.update()
            if animated_name.visible:
                animated_name.draw(screen)
            else:
                animated_names.remove(animated_name)

        pygame.display.update()
        clock.tick(60)


def start_animation():
    pygame.mixer.music.play(start=180, fade_ms=12000, loops=2)
    balls, sparkles = idle_particles(time_seconds=12 - 0.5)
    start_helical_convergence(balls, sparkles, time_bezier=2.7, time_helical=6)
    explosion_effect(time_seconds=6)
    end_game()


def intro_screen():
    def lerp(start, end, progress):
        return start + (end - start) * progress

    def update_button_size_and_color(start_time, duration, power_factor):
        current_time = pygame.time.get_ticks()
        elapsed_time = current_time - start_time

        if elapsed_time < duration:
            progress = (elapsed_time / duration) ** power_factor

            # Update size
            new_width = initial_button_width + (screen_width - initial_button_width) * progress
            new_height = initial_button_height + (screen_height - initial_button_height) * progress

            # Update color
            new_color = (
                int(lerp(initial_color[0], 0, progress)),
                int(lerp(initial_color[1], 0, progress)),
                int(lerp(initial_color[2], 0, progress))
            )

            return int(new_width), int(new_height), new_color, False
        else:
            return screen_width, screen_height, (0, 0, 0), True

    def handle_events():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.is_over(pygame.mouse.get_pos()):
                    return True
        return False

    intro = True
    enlarging = False
    start_time = None
    enlargement_duration = 1500
    power_factor = 4

    initial_button_width, initial_button_height = 300, 120
    initial_color = (231, 101, 253)

    today = datetime.date.today()
    is_christmas = today.month == 12 and today.day in [25, 26, 27]

    button_text = 'UNWRAP' if is_christmas else 'Not Yet Rach'

    start_button = Button(initial_color, (241, 158, 255),
                          (screen_width - initial_button_width) // 2, (screen_height - initial_button_height) // 2,
                          initial_button_width, initial_button_height, button_text)

    while intro:
        if handle_events() and is_christmas:
            enlarging = True
            start_time = pygame.time.get_ticks()

        screen.fill((255, 255, 255))

        if enlarging:
            start_button.text = ""
            new_width, new_height, new_color, finished = update_button_size_and_color(start_time,
                                                                                      enlargement_duration,
                                                                                      power_factor)
            start_button.width = new_width
            start_button.height = new_height
            start_button.color = new_color
            start_button.hover_color = new_color
            start_button.x = (screen_width - new_width) // 2
            start_button.y = (screen_height - new_height) // 2

            if finished:
                intro = False

        start_button.draw(screen)
        pygame.display.update()

    screen.fill((0, 0, 0))
    pygame.display.update()
    pygame.time.wait(1000)


def main():
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load("song.mp3")
    screen_info = pygame.display.Info()
    global screen, clock, screen_width, screen_height
    screen = pygame.display.set_mode((screen_info.current_w, screen_info.current_h))
    screen_width, screen_height = screen.get_width(), screen.get_height()
    clock = pygame.time.Clock()
    pygame.display.set_caption("Christmas Gift")

    intro_screen()
    start_animation()


if __name__ == "__main__":
    main()
