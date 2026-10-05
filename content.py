import random

import pygame

from utils import gen_color


class Content:
    COLORS: list[pygame.Color] = tuple(gen_color(i % 3) for i in range(100))

    def __init__(
        self,
        text: str,
        font: pygame.Font,
        window_width: int,
        window_height: int,
        speed: int,
    ):
        self.font = font
        self.text = text

        self.window_width = window_width
        self.window_height = window_height

        self.speed = random.randint(300, speed)

        possible_directions = [-1, 1]
        self.direction = pygame.Vector2(
            random.choice(possible_directions),
            random.choice(possible_directions),
        )

        self.content = font.render(self.text, True, random.choice(self.COLORS))
        self.rect = self.content.get_rect(
            center=pygame.Vector2(
                random.randrange(self.window_width - self.content.width),
                random.randrange(self.window_height - self.content.height),
            )
        )

        self.prev_bounces = 0
        self.prev_corners = 0
        self.bounces = 0
        self.corners = 0

    @property
    def bounced(self) -> int:
        return self.bounces - self.prev_bounces

    @property
    def cornered(self) -> int:
        return self.corners - self.prev_corners

    def update(self, dt: int) -> None:
        self.prev_bounces = self.bounces
        self.prev_corners = self.corners

        is_horizontal = False
        if self.rect.left < 0 or self.rect.right >= self.window_width:
            self.direction.x = -self.direction.x
            self.bounces += 1

            is_horizontal = True

        is_vertical = False
        if self.rect.top < 0 or self.rect.bottom >= self.window_height:
            self.direction.y = -self.direction.y
            self.bounces += 1

            is_vertical = True

        if is_horizontal and is_vertical:
            self.corners += 1

        self.rect.left = self.rect.left + self.direction.x * self.speed * dt
        self.rect.top = self.rect.top + self.direction.y * self.speed * dt

    def draw(self, screen: pygame.Surface) -> None:
        screen.blit(self.content, self.rect)
