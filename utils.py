import random

import pygame


def gen_color(k: int) -> pygame.Color:
    match k:
        case 0:
            return pygame.Color(
                255, random.randint(50, 220), random.randint(50, 220)
            )
        case 1:
            return pygame.Color(
                random.randint(50, 220), 255, random.randint(50, 220)
            )
        case _:
            return pygame.Color(
                random.randint(50, 220), random.randint(50, 220), 255
            )
