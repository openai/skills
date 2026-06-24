#!/usr/bin/env python3
"""Pack validated per-row frames into a Codex-compatible spritesheet.

Expected input layout:

  rows/
    01-idle/
      01.png
      ...
      08.png
    02-running-right/
      ...

Each row directory must contain exactly 8 RGBA-compatible images. The packer
uses one uniform scale per row, keeps a shared baseline inside that row, and
centers frames horizontally within each 192x208 cell.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path

from PIL import Image


SHEET_WIDTH = 1536
SHEET_HEIGHT = 1872
COLS = 8
ROWS = 9
FRAME_WIDTH = SHEET_WIDTH // COLS
FRAME_HEIGHT = SHEET_HEIGHT // ROWS
ROW_NAMES = [
    "idle",
    "running-right",
    "running-left",
    "waving",
    "jumping",
    "failed",
    "waiting",
    "running",
    "review",
]


@dataclass
class FrameAsset:
    path: Path
    image: Image.Image
    bbox: tuple[int, int, int, int]


def load_rgba(path: Path) -> Image.Image:
    return Image.open(path).convert("RGBA")


def alpha_bbox(image: Image.Image) -> tuple[int, int, int, int]:
    bbox = image.getchannel("A").getbbox()
    if bbox is None:
        raise ValueError(f"{path_label(image)} has empty alpha")
    return bbox


def path_label(image: Image.Image) -> str:
    filename = image.info.get("filename")
    return filename if filename else "<image>"


def discover_row_dir(rows_root: Path, row_index: int, row_name: str) -> Path:
    expected_prefix = f"{row_index + 1:02d}-"
    candidates = sorted(
        path
        for path in rows_root.iterdir()
        if path.is_dir() and path.name.startswith(expected_prefix)
    )
    if not candidates:
        fallback = rows_root / row_name
        if fallback.is_dir():
            return fallback
        raise FileNotFoundError(
            f"missing row directory for row {row_index + 1} ({row_name})"
        )
    if len(candidates) > 1:
        names = ", ".join(path.name for path in candidates)
        raise ValueError(
            f"row {row_index + 1} ({row_name}) is ambiguous — multiple directories "
            f"match prefix {expected_prefix!r}: {names}. "
            f"Keep only the approved variant in {rows_root} and move the rest aside."
        )
    return candidates[0]


def load_row_frames(row_dir: Path) -> list[FrameAsset]:
    frame_paths = sorted(
        [
            path
            for path in row_dir.iterdir()
            if path.is_file() and path.suffix.lower() in {".png", ".webp"}
        ]
    )
    if len(frame_paths) != COLS:
        raise ValueError(
            f"{row_dir} must contain exactly {COLS} frame images, found {len(frame_paths)}"
        )

    frames: list[FrameAsset] = []
    for path in frame_paths:
        image = load_rgba(path)
        image.info["filename"] = str(path)
        bbox = alpha_bbox(image)
        frames.append(FrameAsset(path=path, image=image, bbox=bbox))
    return frames


def scale_frame(
    image: Image.Image, bbox: tuple[int, int, int, int], scale: float
) -> tuple[Image.Image, tuple[int, int, int, int]]:
    x0, y0, x1, y1 = bbox
    cropped = image.crop((x0, y0, x1, y1))
    width = max(1, round(cropped.width * scale))
    height = max(1, round(cropped.height * scale))
    resized = cropped.resize((width, height), Image.Resampling.LANCZOS)
    return resized, (x0, y0, x1, y1)


def pack_sheet(rows_root: Path, output_path: Path, padding: int) -> None:
    canvas = Image.new("RGBA", (SHEET_WIDTH, SHEET_HEIGHT), (0, 0, 0, 0))

    for row_index, row_name in enumerate(ROW_NAMES):
        row_dir = discover_row_dir(rows_root, row_index, row_name)
        frames = load_row_frames(row_dir)

        widths = [bbox[2] - bbox[0] for bbox in (frame.bbox for frame in frames)]
        heights = [bbox[3] - bbox[1] for bbox in (frame.bbox for frame in frames)]
        max_width = max(widths)
        max_height = max(heights)
        available_width = FRAME_WIDTH - (padding * 2)
        available_height = FRAME_HEIGHT - (padding * 2)
        scale = min(available_width / max_width, available_height / max_height, 1.0)

        scaled_sizes: list[tuple[int, int]] = []
        scaled_bottoms: list[int] = []
        for frame in frames:
            bbox = frame.bbox
            scaled_sizes.append(
                (
                    max(1, round((bbox[2] - bbox[0]) * scale)),
                    max(1, round((bbox[3] - bbox[1]) * scale)),
                )
            )
            scaled_bottoms.append(max(1, round(bbox[3] * scale)))

        baseline = min(FRAME_HEIGHT - padding, max(scaled_bottoms) + padding)
        row_top = row_index * FRAME_HEIGHT

        for col_index, frame in enumerate(frames):
            sprite, _ = scale_frame(frame.image, frame.bbox, scale)
            x = col_index * FRAME_WIDTH + (FRAME_WIDTH - sprite.width) // 2
            y = row_top + baseline - sprite.height
            canvas.alpha_composite(sprite, (x, y))

    output_path.parent.mkdir(parents=True, exist_ok=True)
    suffix = output_path.suffix.lower()
    if suffix == ".png":
        canvas.save(output_path, lossless=True)
    elif suffix == ".webp":
        canvas.save(output_path, format="WEBP", lossless=True, quality=100)
    else:
        raise ValueError(
            f"output extension {suffix or '<none>'!r} is not supported; "
            f"use .png or .webp"
        )


MAX_PADDING = min(FRAME_WIDTH, FRAME_HEIGHT) // 2 - 1


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("rows_root", type=Path, help="Directory containing 9 row folders")
    parser.add_argument("output", type=Path, help="Output spritesheet path (.png or .webp)")
    parser.add_argument(
        "--padding",
        type=int,
        default=10,
        help=f"Edge padding inside each cell, in pixels (recommended 8-12, max {MAX_PADDING})",
    )
    args = parser.parse_args()
    if not 0 <= args.padding <= MAX_PADDING:
        parser.error(
            f"--padding must be between 0 and {MAX_PADDING}, got {args.padding}"
        )
    return args


def main() -> int:
    args = parse_args()
    pack_sheet(args.rows_root, args.output, args.padding)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
