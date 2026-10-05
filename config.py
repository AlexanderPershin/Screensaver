import configparser
from pathlib import Path

import caep
from pydantic import BaseModel, Field


class Config(BaseModel):
    n: int = Field(default=1, gt=0, le=1000)

    window_width: int = Field(default=800, gt=0, le=3840)
    window_height: int = Field(default=600, gt=0, le=2160)

    fps: int = Field(default=60, ge=30, le=240)

    speed: int = Field(default=300, gt=0)

    content: str = Field(default="Stepik", min_length=1, max_length=12)

    font_path: str = Field(default="fonts/BlackOpsOne-Regular.ttf")

    content_font_size: int = Field(default=48, gt=0, le=200)
    gui_font_size: int = Field(default=24, gt=0, le=200)

    bg_color: str = Field(default="#006699")
    content_text_color: str = Field(default="#009900")
    gui_text_color: str = Field(default="#ffffff")

    @classmethod
    def load_from_ini(cls, path: Path = Path("settings.ini")) -> Config:
        if not path.exists():
            return cls()

        config = caep.load(
            cls,
            "Screensaver",
            "screensaver_config",
            "settings.ini",
            "Game",
            opts=["--config", str(path.resolve())],
        )

        return config

    def save_to_ini(self, path: Path = Path("settings.ini")) -> None:
        cp = configparser.ConfigParser()
        cp["Game"] = {k: str(v) for k, v in self.model_dump().items()}
        with open(path, "w", encoding="utf-8") as f:
            cp.write(f)

    def parse_cli(self, **overrides) -> Config:
        updates = {k: v for k, v in overrides.items() if v is not None}
        current_data = self.model_dump()
        current_data.update(updates)
        return Config(**current_data)


CONFIG = Config()
