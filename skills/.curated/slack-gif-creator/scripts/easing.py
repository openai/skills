#!/usr/bin/env python3
"""
Easing and motion helpers for handcrafted GIF animation.
"""

from __future__ import annotations

import math


def linear(t: float) -> float:
    return t


def ease_in_quad(t: float) -> float:
    return t * t


def ease_out_quad(t: float) -> float:
    return t * (2 - t)


def ease_in_out_quad(t: float) -> float:
    if t < 0.5:
        return 2 * t * t
    return -1 + (4 - 2 * t) * t


def ease_in_bounce(t: float) -> float:
    return 1 - ease_out_bounce(1 - t)


def ease_out_bounce(t: float) -> float:
    if t < 1 / 2.75:
        return 7.5625 * t * t
    if t < 2 / 2.75:
        t -= 1.5 / 2.75
        return 7.5625 * t * t + 0.75
    if t < 2.5 / 2.75:
        t -= 2.25 / 2.75
        return 7.5625 * t * t + 0.9375
    t -= 2.625 / 2.75
    return 7.5625 * t * t + 0.984375


def ease_in_elastic(t: float) -> float:
    if t == 0 or t == 1:
        return t
    return -math.pow(2, 10 * (t - 1)) * math.sin((t - 1.1) * 5 * math.pi)


def ease_out_elastic(t: float) -> float:
    if t == 0 or t == 1:
        return t
    return math.pow(2, -10 * t) * math.sin((t - 0.1) * 5 * math.pi) + 1


def ease_back_in(t: float) -> float:
    c1 = 1.70158
    c3 = c1 + 1
    return c3 * t * t * t - c1 * t * t


def ease_back_out(t: float) -> float:
    c1 = 1.70158
    c3 = c1 + 1
    return 1 + c3 * pow(t - 1, 3) + c1 * pow(t - 1, 2)


EASING_FUNCTIONS = {
    "linear": linear,
    "ease_in": ease_in_quad,
    "ease_out": ease_out_quad,
    "ease_in_out": ease_in_out_quad,
    "bounce_in": ease_in_bounce,
    "bounce_out": ease_out_bounce,
    "elastic_in": ease_in_elastic,
    "elastic_out": ease_out_elastic,
    "back_in": ease_back_in,
    "back_out": ease_back_out,
    "anticipate": ease_back_in,
    "overshoot": ease_back_out,
}


def get_easing(name: str = "linear"):
    """Return an easing function by name."""
    return EASING_FUNCTIONS.get(name, linear)


def interpolate(start: float, end: float, t: float, easing: str = "linear") -> float:
    """Interpolate from start to end using an easing curve."""
    return start + (end - start) * get_easing(easing)(t)


def apply_squash_stretch(
    base_scale: tuple[float, float],
    intensity: float,
    direction: str = "vertical",
) -> tuple[float, float]:
    """Apply simple squash-and-stretch scaling."""
    width_scale, height_scale = base_scale

    if direction == "vertical":
        height_scale *= 1 - intensity * 0.5
        width_scale *= 1 + intensity * 0.5
    elif direction == "horizontal":
        width_scale *= 1 - intensity * 0.5
        height_scale *= 1 + intensity * 0.5
    elif direction == "both":
        width_scale *= 1 - intensity * 0.3
        height_scale *= 1 - intensity * 0.3

    return width_scale, height_scale


def calculate_arc_motion(
    start: tuple[float, float],
    end: tuple[float, float],
    height: float,
    t: float,
) -> tuple[float, float]:
    """Return a point along a simple parabolic arc."""
    x1, y1 = start
    x2, y2 = end
    x = x1 + (x2 - x1) * t
    arc_offset = 4 * height * t * (1 - t)
    y = y1 + (y2 - y1) * t - arc_offset
    return x, y
