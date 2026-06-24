#!/usr/bin/env python3
"""Validate the mechanical parts of a Codex pet spritesheet and pet.json.

This cannot prove anatomy is correct. It catches the boring failures that make
the Codex UI drift: wrong dimensions, empty frames, missing alpha, opaque
backgrounds, edge contact, row-scale instability, and a malformed pet.json.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from PIL import Image


SHEET_WIDTH = 1536
SHEET_HEIGHT = 1872
COLS = 8
ROWS = 9
FRAME_WIDTH = SHEET_WIDTH // COLS
FRAME_HEIGHT = SHEET_HEIGHT // ROWS

PET_JSON_REQUIRED_FIELDS = ("id", "displayName", "description", "spritesheetPath")


def alpha_bbox(frame: Image.Image) -> tuple[int, int, int, int] | None:
    return frame.getchannel("A").getbbox()


def alpha_extrema(frame: Image.Image) -> tuple[int, int]:
    return frame.getchannel("A").getextrema()


def validate_pet_json(
    pet_json_path: Path, spritesheet_path: Path
) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []

    if not pet_json_path.is_file():
        errors.append(f"pet.json not found at {pet_json_path}")
        return errors, warnings

    try:
        data = json.loads(pet_json_path.read_text())
    except json.JSONDecodeError as exc:
        errors.append(f"pet.json: invalid JSON ({exc})")
        return errors, warnings

    if not isinstance(data, dict):
        errors.append("pet.json: top-level value must be an object")
        return errors, warnings

    for field in PET_JSON_REQUIRED_FIELDS:
        if field not in data:
            errors.append(f"pet.json: missing required field {field!r}")
        elif not isinstance(data[field], str) or not data[field].strip():
            errors.append(f"pet.json: field {field!r} must be a non-empty string")

    sheet_field = data.get("spritesheetPath")
    if isinstance(sheet_field, str) and sheet_field:
        as_path = Path(sheet_field)
        pet_dir = pet_json_path.parent.resolve()
        if as_path.is_absolute():
            errors.append(
                f"pet.json: spritesheetPath must be a relative filename inside the "
                f"pet directory, not an absolute path ({sheet_field!r})"
            )
        elif as_path.name != sheet_field or ".." in as_path.parts:
            errors.append(
                f"pet.json: spritesheetPath must be a single filename inside the "
                f"pet directory, not a nested or traversing path ({sheet_field!r})"
            )
        else:
            resolved = (pet_dir / sheet_field).resolve()
            try:
                resolved.relative_to(pet_dir)
            except ValueError:
                errors.append(
                    f"pet.json: spritesheetPath resolves outside the pet directory "
                    f"({resolved})"
                )
            if resolved != spritesheet_path.resolve():
                warnings.append(
                    f"pet.json: spritesheetPath points to {resolved}, "
                    f"but the sheet under validation is {spritesheet_path.resolve()}"
                )

    pet_id = data.get("id")
    parent_dir = pet_json_path.parent.name
    if isinstance(pet_id, str) and pet_id and parent_dir and pet_id != parent_dir:
        warnings.append(
            f"pet.json: id {pet_id!r} differs from parent directory {parent_dir!r}; "
            f"Codex resolves pets by the directory name under ~/.codex/pets/"
        )

    return errors, warnings


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("spritesheet", type=Path)
    parser.add_argument("--edge-padding", type=int, default=6)
    parser.add_argument("--max-row-height-drift", type=float, default=0.28)
    parser.add_argument(
        "--pet-json",
        type=Path,
        default=None,
        help="Path to pet.json. Defaults to <spritesheet-dir>/pet.json if present.",
    )
    parser.add_argument(
        "--no-pet-json",
        action="store_true",
        help="Skip pet.json validation entirely.",
    )
    args = parser.parse_args()

    image = Image.open(args.spritesheet).convert("RGBA")
    errors: list[str] = []
    warnings: list[str] = []

    if image.size != (SHEET_WIDTH, SHEET_HEIGHT):
        errors.append(
            f"expected {SHEET_WIDTH}x{SHEET_HEIGHT}, got {image.width}x{image.height}"
        )

    sheet_alpha_min, sheet_alpha_max = alpha_extrema(image)
    if sheet_alpha_min == 255 and sheet_alpha_max == 255:
        errors.append(
            "spritesheet has no transparent pixels; background was not removed"
        )

    for row in range(ROWS):
        heights: list[int] = []
        widths: list[int] = []
        for col in range(COLS):
            left = col * FRAME_WIDTH
            top = row * FRAME_HEIGHT
            frame = image.crop((left, top, left + FRAME_WIDTH, top + FRAME_HEIGHT))
            bbox = alpha_bbox(frame)
            label = f"row {row + 1}, col {col + 1}"
            if bbox is None:
                errors.append(f"{label}: empty frame")
                continue

            x0, y0, x1, y1 = bbox
            widths.append(x1 - x0)
            heights.append(y1 - y0)

            frame_alpha_min, _ = alpha_extrema(frame)
            if frame_alpha_min == 255:
                warnings.append(
                    f"{label}: frame is fully opaque; either the cell is filled "
                    f"edge-to-edge or the background was not removed"
                )

            if (
                x0 < args.edge_padding
                or y0 < args.edge_padding
                or FRAME_WIDTH - x1 < args.edge_padding
                or FRAME_HEIGHT - y1 < args.edge_padding
            ):
                warnings.append(f"{label}: sprite is close to the cell edge {bbox}")

        if heights:
            min_h = min(heights)
            max_h = max(heights)
            if min_h > 0 and (max_h - min_h) / min_h > args.max_row_height_drift:
                warnings.append(
                    f"row {row + 1}: frame height drift is high "
                    f"(min={min_h}, max={max_h})"
                )

        if widths:
            min_w = min(widths)
            max_w = max(widths)
            if min_w > 0 and (max_w - min_w) / min_w > 0.5:
                warnings.append(
                    f"row {row + 1}: frame width drift is high "
                    f"(min={min_w}, max={max_w})"
                )

    if not args.no_pet_json:
        pet_json_path = args.pet_json or (args.spritesheet.parent / "pet.json")
        if pet_json_path.exists() or args.pet_json is not None:
            pj_errors, pj_warnings = validate_pet_json(pet_json_path, args.spritesheet)
            errors.extend(pj_errors)
            warnings.extend(pj_warnings)
        else:
            warnings.append(
                f"pet.json not found next to spritesheet; pass --pet-json to validate "
                f"the install contract or --no-pet-json to suppress this warning"
            )

    if errors:
        print("ERRORS")
        for error in errors:
            print(f"- {error}")
    if warnings:
        print("WARNINGS")
        for warning in warnings:
            print(f"- {warning}")

    if not errors and not warnings:
        print("OK")

    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
