import pygame
import typer

from config import Config
from content import Content

CONFIG = Config.load_from_ini()


def main(
    n: int | None = typer.Option(None, "--n"),
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
        n=n,
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


class Game:
    def __init__(self, config: Config):
        self.running = False
        self.config = config

    def __enter__(self):
        pygame.init()

        self.screen = pygame.display.set_mode(
            (self.config.window_width, self.config.window_height)
        )
        pygame.display.set_caption("Screensaver")

        self.clock = pygame.time.Clock()

        self.dt = 0.0

        self.bounces = 0
        self.corners = 0

        self._load_font()

        self.gui_temp = "Bounces: {0}. Corners: {1}"

        self.contents: list[Content] = [
            Content(
                self.config.content,
                self.content_font,
                self.config.window_width,
                self.config.window_height,
                self.config.speed,
            )
            for _ in range(self.config.n)
        ]

        self.gui = self.gui_font.render(
            self.gui_temp.format(self.bounces, self.corners),
            True,
            self.config.gui_text_color,
        )
        self.gui_rect = self.gui.get_rect(x=0, y=0)

        self.running = True

        return self

    def __exit__(self, *args):
        pygame.quit()

    def _load_font(self) -> None:
        self.gui_font = pygame.font.Font(
            self.config.font_path, self.config.gui_font_size
        )
        self.content_font = pygame.font.Font(
            self.config.font_path, self.config.content_font_size
        )

    def run(self):
        while self.running:
            self.dt = self.clock.tick(self.config.fps) / 1000
            self.watch_for_events()
            self.update()
            self.draw()

    def watch_for_events(self):
        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    self.running = False

    def update(self):
        self.gui = self.gui_font.render(
            self.gui_temp.format(self.bounces, self.corners),
            True,
            self.config.gui_text_color,
        )
        self.gui_rect = self.gui.get_rect(x=0, y=0)

        for content in self.contents:
            content.update(self.dt)
            self.bounces += content.bounced
            self.corners += content.cornered

    def draw(self):
        self.screen.fill(self.config.bg_color)
        self.screen.blit(self.gui, self.gui_rect)

        for content in self.contents:
            content.draw(self.screen)

        pygame.display.flip()


def run_game(config: Config):
    with Game(config) as game:
        game.run()


if __name__ == "__main__":
    typer.run(main)
