import configparser
import typing
from pathlib import Path

import caep
from pydantic import BaseModel, Field, field_validator


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

    @field_validator(
        "bg_color", "content_text_color", "gui_text_color", mode="before"
    )
    @classmethod
    def validate_hex_color(cls, v: typing.Any) -> str:
        if not isinstance(v, str):
            raise TypeError("Допустимы только цвета в виде hex значений")

        v = v.strip()
        if not v.startswith("#"):
            raise ValueError('Цвет должен начинаться c "#"')

        hex_part = v[1:]
        if len(hex_part) not in (6, 8):
            raise ValueError("Hex-цвет должен иметь 6 или 8 символов после #")
        try:
            int(hex_part, 16)
        except ValueError:
            raise ValueError("Некорректные hex-символы в цвете")
        return v

    @field_validator("font_path")
    @classmethod
    def validate_font_exists(cls, v: str) -> str:
        if v and not Path(v).is_file():
            raise ValueError(f"Файл шрифта не найден: {v}")
        return v

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
