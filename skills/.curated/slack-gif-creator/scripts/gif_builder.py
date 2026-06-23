#!/usr/bin/env python3
"""
Build GIFs from generated frames and optimize them for Slack-friendly delivery.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
from PIL import Image


class GIFBuilder:
    """Assemble frames and save an optimized GIF."""

    def __init__(self, width: int = 480, height: int = 480, fps: int = 15):
        self.width = width
        self.height = height
        self.fps = fps
        self.frames: list[np.ndarray] = []

    def add_frame(self, frame: np.ndarray | Image.Image) -> None:
        """Add a single frame, resizing it if needed."""
        if isinstance(frame, Image.Image):
            frame = np.array(frame.convert("RGB"))

        if frame.shape[:2] != (self.height, self.width):
            resized = Image.fromarray(frame).resize(
                (self.width, self.height),
                Image.Resampling.LANCZOS,
            )
            frame = np.array(resized)

        self.frames.append(frame)

    def add_frames(self, frames: list[np.ndarray | Image.Image]) -> None:
        """Add multiple frames."""
        for frame in frames:
            self.add_frame(frame)

    def optimize_colors(
        self,
        num_colors: int = 128,
        use_global_palette: bool = True,
    ) -> list[np.ndarray]:
        """Quantize frames to reduce output size."""
        optimized: list[np.ndarray] = []

        if use_global_palette and len(self.frames) > 1:
            sample_size = min(5, len(self.frames))
            sample_indices = [
                int(i * len(self.frames) / sample_size) for i in range(sample_size)
            ]
            sample_frames = [self.frames[i] for i in sample_indices]

            all_pixels = np.vstack([frame.reshape(-1, 3) for frame in sample_frames])
            total_pixels = len(all_pixels)
            palette_width = min(512, int(np.sqrt(total_pixels)))
            palette_height = (total_pixels + palette_width - 1) // palette_width
            pixels_needed = palette_width * palette_height

            if pixels_needed > total_pixels:
                padding = np.zeros((pixels_needed - total_pixels, 3), dtype=np.uint8)
                all_pixels = np.vstack([all_pixels, padding])

            palette_image = Image.fromarray(
                all_pixels[:pixels_needed].reshape(palette_height, palette_width, 3),
                mode="RGB",
            )
            global_palette = palette_image.quantize(colors=num_colors, method=2)

            for frame in self.frames:
                quantized = Image.fromarray(frame).quantize(
                    palette=global_palette,
                    dither=1,
                )
                optimized.append(np.array(quantized.convert("RGB")))
            return optimized

        for frame in self.frames:
            quantized = Image.fromarray(frame).quantize(
                colors=num_colors,
                method=2,
                dither=1,
            )
            optimized.append(np.array(quantized.convert("RGB")))
        return optimized

    def deduplicate_frames(self, threshold: float = 0.9995) -> int:
        """Remove near-identical consecutive frames."""
        if len(self.frames) < 2:
            return 0

        deduplicated = [self.frames[0]]
        removed = 0

        for index in range(1, len(self.frames)):
            prev_frame = np.array(deduplicated[-1], dtype=np.float32)
            curr_frame = np.array(self.frames[index], dtype=np.float32)
            similarity = 1.0 - (np.mean(np.abs(prev_frame - curr_frame)) / 255.0)
            if similarity < threshold:
                deduplicated.append(self.frames[index])
            else:
                removed += 1

        self.frames = deduplicated
        return removed

    def save(
        self,
        output_path: str | Path,
        num_colors: int = 128,
        optimize_for_emoji: bool = False,
        remove_duplicates: bool = False,
    ) -> dict:
        """Write frames to disk as an optimized GIF."""
        if not self.frames:
            raise ValueError("No frames to save. Add frames first.")

        output_path = Path(output_path)

        if remove_duplicates:
            self.deduplicate_frames(threshold=0.9995)

        if optimize_for_emoji:
            if self.width > 128 or self.height > 128:
                self.width = 128
                self.height = 128
                self.frames = [
                    np.array(
                        Image.fromarray(frame).resize(
                            (128, 128),
                            Image.Resampling.LANCZOS,
                        )
                    )
                    for frame in self.frames
                ]
            num_colors = min(num_colors, 48)
            if len(self.frames) > 12:
                keep_every = max(1, len(self.frames) // 12)
                self.frames = [
                    self.frames[index]
                    for index in range(0, len(self.frames), keep_every)
                ]

        optimized_frames = self.optimize_colors(
            num_colors=num_colors,
            use_global_palette=True,
        )

        pil_frames = [Image.fromarray(frame) for frame in optimized_frames]
        pil_frames[0].save(
            output_path,
            save_all=True,
            append_images=pil_frames[1:],
            duration=int(1000 / self.fps),
            loop=0,
            optimize=False,
            disposal=2,
        )

        size_kb = output_path.stat().st_size / 1024
        return {
            "path": str(output_path),
            "size_kb": size_kb,
            "size_mb": size_kb / 1024,
            "dimensions": f"{self.width}x{self.height}",
            "frame_count": len(optimized_frames),
            "fps": self.fps,
            "duration_seconds": len(optimized_frames) / self.fps,
            "colors": num_colors,
        }

    def clear(self) -> None:
        """Remove all currently stored frames."""
        self.frames = []
