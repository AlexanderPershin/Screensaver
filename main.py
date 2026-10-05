import random

import pygame
import typer

from config import Config

CONFIG = Config.load_from_ini()


def main(
    width: int | None = typer.Option(CONFIG.window_width, "--width"),
    height: int | None = typer.Option(CONFIG.window_height, "--height"),
    fps: int | None = typer.Option(CONFIG.fps, "--fps"),
    speed: int | None = typer.Option(CONFIG.speed, "--speed"),
    content: str | None = typer.Option(CONFIG.content, "--content"),
    font_path: str | None = typer.Option(CONFIG.font_path, "--font-path"),
    content_font_size: int | None = typer.Option(
        CONFIG.content_font_size, "--content-font-size"
    ),
    gui_font_size: int | None = typer.Option(
        CONFIG.gui_font_size, "--gui-font-size"
    ),
    bg_color: str | None = typer.Option(CONFIG.bg_color, "--bg-color"),
    content_text_color: str | None = typer.Option(
        CONFIG.content_text_color, "--content-text-color"
    ),
    gui_text_color: str | None = typer.Option(
        CONFIG.gui_text_color, "--gui-text-color"
    ),
):
    config = CONFIG.parse_cli(
        window_width=width,
        window_height=height,
        fps=fps,
        speed=speed,
        content=content,
        font_path=font_path,
        content_font_size=content_font_size,
        gui_font_size=gui_font_size,
        bg_color=bg_color,
        content_text_color=content_text_color,
        gui_text_color=gui_text_color,
    )

    config.save_to_ini()

    run_game(config)


def run_game(config: Config):
    pygame.init()

    screen = pygame.display.set_mode(
        (config.window_width, config.window_height)
    )

    pygame.display.set_caption("Configuration")

    clock = pygame.time.Clock()

    font = pygame.font.Font(config.font_path, config.content_font_size)
    text = font.render(config.content, True, config.content_text_color)
    rect = text.get_rect(center=screen.get_rect().center)

    bounces = 0
    corners = 0

    gui_font = pygame.font.Font(config.font_path, config.gui_font_size)
    gui_temp = "Bounces: {0}. Corners: {1}"
    gui = gui_font.render(
        gui_temp.format(bounces, corners), True, config.gui_text_color
    )
    gui_rect = gui.get_rect(x=0, y=0)

    rect.left = random.randrange(config.window_width - rect.width)
    rect.top = random.randrange(config.window_height - rect.height)

    content_direction = pygame.Vector2(1, 1)

    dt = 0

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        is_horizontal = False
        if rect.left < 0 or rect.right >= config.window_width:
            content_direction.x = -content_direction.x
            bounces += 1

            is_horizontal = True

        is_vertical = False
        if rect.top < 0 or rect.bottom >= config.window_height:
            content_direction.y = -content_direction.y
            bounces += 1

            is_vertical = True

        if is_horizontal and is_vertical:
            corners += 1

        if is_horizontal or is_vertical:
            gui = gui_font.render(
                gui_temp.format(bounces, corners), True, config.gui_text_color
            )

        rect.left = rect.left + content_direction.x * config.speed * dt
        rect.top = rect.top + content_direction.y * config.speed * dt

        screen.fill(config.bg_color)

        screen.blit(gui, gui_rect)

        screen.blit(text, rect)

        pygame.display.flip()

        dt = clock.tick(config.fps) / 1000

    pygame.quit()


if __name__ == "__main__":
    typer.run(main)
