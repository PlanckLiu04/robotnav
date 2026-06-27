"""Cross-platform font helpers for clear Pygame text rendering."""

from __future__ import annotations

from functools import lru_cache

import pygame


FONT_CANDIDATES = [
    "PingFang SC",
    "Microsoft YaHei",
    "SimHei",
    "Noto Sans CJK SC",
    "Noto Sans CJK",
    "WenQuanYi Micro Hei",
    "Arial",
    "Helvetica",
    "DejaVu Sans",
]


@lru_cache(maxsize=32)
def get_font(size: int, bold: bool = False) -> pygame.font.Font:
    for name in FONT_CANDIDATES:
        path = pygame.font.match_font(name, bold=bold)
        if path is not None:
            return pygame.font.Font(path, size)

    font = pygame.font.Font(None, size)
    font.set_bold(bold)
    return font
