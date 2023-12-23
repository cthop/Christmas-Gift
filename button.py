import pygame


class Button:
    def __init__(self, color, hover_color, x, y, width, height, text=''):
        self.color = color
        self.hover_color = hover_color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.shadow_offset = 5
        self.enlarge_offset = 10

    def draw(self, screen, is_change_color=True, is_shadow=True, is_raise_on_hover=True):
        is_hovered = self.is_over(pygame.mouse.get_pos())

        # Enlarge effect when hovered
        if is_raise_on_hover:
            new_width = self.width + (self.enlarge_offset if is_hovered else 0)
            new_height = self.height + (self.enlarge_offset if is_hovered else 0)
            new_x = self.x - (self.enlarge_offset // 2 if is_hovered else 0)
            new_y = self.y - (self.enlarge_offset // 2 if is_hovered else 0)
        else:
            new_width = self.width
            new_height = self.height
            new_x = self.x
            new_y = self.y

        # Shadow effect
        if is_shadow:
            if is_raise_on_hover and is_hovered:
                shadow_rect = (new_x + self.shadow_offset // 1.5, new_y + self.shadow_offset // 1.5,
                               new_width, new_height)

            else:
                shadow_rect = (new_x + self.shadow_offset, new_y + self.shadow_offset, new_width, new_height)
            pygame.draw.rect(screen, (50, 50, 50), shadow_rect)

        # Change color when hovered
        if is_change_color:
            current_color = self.hover_color if is_hovered else self.color
        else:
            current_color = self.color
        pygame.draw.rect(screen, current_color, (new_x, new_y, new_width, new_height), 0)

        # Draw text
        if self.text != '':
            font_size = 60 + self.enlarge_offset if is_hovered and is_raise_on_hover else 60
            font = pygame.font.SysFont('Arial', font_size, bold=True)
            text = font.render(self.text, 1, (0, 0, 0))
            screen.blit(text, (
                new_x + (new_width / 2 - text.get_width() / 2),
                new_y + (new_height / 2 - text.get_height() / 2)
            ))

    def is_over(self, pos):
        if self.x - self.enlarge_offset < pos[0] < self.x + self.width + self.enlarge_offset:
            if self.y - self.enlarge_offset < pos[1] < self.y + self.height + self.enlarge_offset:
                return True
        return False
