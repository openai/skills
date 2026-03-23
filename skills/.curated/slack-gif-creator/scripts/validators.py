#!/usr/bin/env python3
"""
Validate whether a GIF is ready for Slack-style use.
"""

from __future__ import annotations

from pathlib import Path

from PIL import Image


def validate_gif(
    gif_path: str | Path,
    is_emoji: bool = True,
    verbose: bool = True,
) -> tuple[bool, dict]:
    """Validate dimensions, size, frame count, and basic playback metadata."""
    gif_path = Path(gif_path)

    if not gif_path.exists():
        return False, {"error": f"File not found: {gif_path}"}

    size_bytes = gif_path.stat().st_size
    size_kb = size_bytes / 1024
    size_mb = size_kb / 1024

    try:
        with Image.open(gif_path) as image:
            width, height = image.size
            frame_count = 0
            try:
                while True:
                    image.seek(frame_count)
                    frame_count += 1
            except EOFError:
                pass

            duration_ms = image.info.get("duration", 100)
            total_duration = (duration_ms * frame_count) / 1000
            fps = frame_count / total_duration if total_duration > 0 else 0
    except Exception as exc:
        return False, {"error": f"Failed to read GIF: {exc}"}

    if is_emoji:
        optimal = width == height == 128
        acceptable = width == height and 64 <= width <= 128
        passes = acceptable
    else:
        min_side = min(width, height)
        aspect_ratio = max(width, height) / min_side if min_side > 0 else float("inf")
        optimal = None
        acceptable = None
        passes = aspect_ratio <= 2.0 and 320 <= min_side <= 640

    results = {
        "file": str(gif_path),
        "passes": passes,
        "width": width,
        "height": height,
        "size_kb": size_kb,
        "size_mb": size_mb,
        "frame_count": frame_count,
        "duration_seconds": total_duration,
        "fps": fps,
        "is_emoji": is_emoji,
        "optimal": optimal,
    }

    if verbose:
        status = ""
        if is_emoji and acceptable:
            status = " (optimal)" if optimal else " (acceptable)"
        print(f"Validating {gif_path.name}:")
        print(f"  Dimensions: {width}x{height}{status}")
        if size_mb >= 1.0:
            print(f"  Size: {size_kb:.1f} KB ({size_mb:.2f} MB)")
        else:
            print(f"  Size: {size_kb:.1f} KB")
        print(f"  Frames: {frame_count} @ {fps:.1f} fps ({total_duration:.1f}s)")
        if not passes:
            if is_emoji:
                print("  Note: emoji GIFs should be square and usually 128x128.")
            else:
                print("  Note: dimensions are unusual for a compact Slack message GIF.")
        if size_mb > 5.0:
            print("  Note: large file size; consider fewer frames or fewer colors.")

    return passes, results


def is_slack_ready(
    gif_path: str | Path,
    is_emoji: bool = True,
    verbose: bool = True,
) -> bool:
    """Return True when the GIF passes the validator."""
    passes, _ = validate_gif(gif_path, is_emoji=is_emoji, verbose=verbose)
    return passes
