#!/usr/bin/env python3
"""
Small Pillow helpers for building Slack-oriented GIF frames.
"""

from __future__ import annotations

import math

from PIL import Image, ImageDraw, ImageFont


def create_blank_frame(
    width: int,
    height: int,
    color: tuple[int, int, int] = (255, 255, 255),
) -> Image.Image:
    """Create a blank RGB frame."""
    return Image.new("RGB", (width, height), color)


def create_gradient_background(
    width: int,
    height: int,
    top_color: tuple[int, int, int],
    bottom_color: tuple[int, int, int],
) -> Image.Image:
    """Create a simple vertical gradient background."""
    frame = Image.new("RGB", (width, height))
    draw = ImageDraw.Draw(frame)

    r1, g1, b1 = top_color
    r2, g2, b2 = bottom_color

    for y in range(height):
        ratio = y / height
        color = (
            int(r1 * (1 - ratio) + r2 * ratio),
            int(g1 * (1 - ratio) + g2 * ratio),
            int(b1 * (1 - ratio) + b2 * ratio),
        )
        draw.line([(0, y), (width, y)], fill=color)

    return frame


def draw_circle(
    frame: Image.Image,
    center: tuple[int, int],
    radius: int,
    fill_color: tuple[int, int, int] | None = None,
    outline_color: tuple[int, int, int] | None = None,
    outline_width: int = 1,
) -> Image.Image:
    """Draw a circle onto a frame."""
    draw = ImageDraw.Draw(frame)
    x, y = center
    bounds = [x - radius, y - radius, x + radius, y + radius]
    draw.ellipse(bounds, fill=fill_color, outline=outline_color, width=outline_width)
    return frame


def draw_text(
    frame: Image.Image,
    text: str,
    position: tuple[int, int],
    color: tuple[int, int, int] = (0, 0, 0),
    centered: bool = False,
) -> Image.Image:
    """Draw simple text using Pillow's default font."""
    draw = ImageDraw.Draw(frame)
    font = ImageFont.load_default()

    if centered:
        bbox = draw.textbbox((0, 0), text, font=font)
        width = bbox[2] - bbox[0]
        height = bbox[3] - bbox[1]
        position = (position[0] - width // 2, position[1] - height // 2)

    draw.text(position, text, fill=color, font=font)
    return frame


def draw_star(
    frame: Image.Image,
    center: tuple[int, int],
    size: int,
    fill_color: tuple[int, int, int],
    outline_color: tuple[int, int, int] | None = None,
    outline_width: int = 1,
) -> Image.Image:
    """Draw a five-pointed star."""
    draw = ImageDraw.Draw(frame)
    x, y = center
    points = []

    for index in range(10):
        angle = (index * 36 - 90) * math.pi / 180
        radius = size if index % 2 == 0 else size * 0.4
        points.append((x + radius * math.cos(angle), y + radius * math.sin(angle)))

    draw.polygon(points, fill=fill_color, outline=outline_color, width=outline_width)
    return frame
