import logging
import os
from functools import lru_cache
from pathlib import Path
from typing import Optional
from urllib.parse import urljoin

from PIL.Image import Image

from bot.bpm_gifs.generator.adjust_video import adjust_video_tempo
from bot.bpm_gifs.generator.get_video_frame import get_first_frame


class GifTemplate:
    _preview: Optional[Image] = None

    def __init__(self, path: Path):
        self.path = path

    def get_preview_content(self):
        return self.preview.getdata()

    @property
    def preview(self):
        if self._preview is None:
            self._preview = get_first_frame(self.path)
        return self._preview

    @property
    def wh(self) -> tuple[int, int]:
        return self.preview.size

    @lru_cache(maxsize=50)
    def render_as_target_bpm(self, target_bpm: float):
        content = adjust_video_tempo(
            video_path=self.path,
            video_bpm=self.bpm,
            target_bpm=target_bpm
        )

        return content

    @property
    def key(self):
        return self.get_filename().split("_")[1].lower()

    def get_filename(self):
        return self.path.stem

    @property
    def bpm(self):
        file_bpm_part = self.get_filename().split("_")[0]
        return float(file_bpm_part)

    def build_preview_url(self):
        self_url = os.getenv("SPOTIFY_CLIENT_REDIRECT")
        template_url = urljoin(
            base=self_url,
            url=f"/gif/preview?t={self.key}"
        )
        return template_url

    def build_bpm_url(self, target_bpm: float):
        self_url = os.getenv("SPOTIFY_CLIENT_REDIRECT")
        template_url = urljoin(
            base=self_url,
            url=f"/gif/bpm?t={self.key}&bpm={target_bpm}"
        )
        return template_url


def init_warm_templates() -> dict[str, GifTemplate]:
    templates: dict[str, GifTemplate] = {}
    
    for path in Path("bot/bpm_gifs/generator/templates").glob("*.mp4"):
        template = GifTemplate(path)

        logging.info(f"Loaded template: {template.key}")
        template.get_preview_content()

        templates[template.key] = template

    return templates


TEMPLATES = init_warm_templates()
