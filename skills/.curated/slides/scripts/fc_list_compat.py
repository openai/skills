#!/usr/bin/env python3
import argparse
import os
import sys
import winreg
from fontTools.ttLib import TTCollection, TTFont


def norm_path(font_dir: str, value: str) -> str:
    value = value.strip()
    if not value:
        return ""
    if os.path.isabs(value):
        return value
    return os.path.join(font_dir, value)


def registry_font_paths() -> list[str]:
    results: list[str] = []
    font_dir = os.path.join(os.environ.get("WINDIR", r"C:\Windows"), "Fonts")
    keys = [
        (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Fonts"),
        (winreg.HKEY_CURRENT_USER, r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Fonts"),
    ]
    for hive, subkey in keys:
        try:
            with winreg.OpenKey(hive, subkey) as key:
                idx = 0
                while True:
                    try:
                        _, value, _ = winreg.EnumValue(key, idx)
                    except OSError:
                        break
                    idx += 1
                    path = norm_path(font_dir, str(value))
                    if os.path.isfile(path):
                        results.append(path)
        except OSError:
            continue
    # User-installed fonts may exist outside the registry view we need.
    user_font_dir = os.path.join(
        os.environ.get("LOCALAPPDATA", ""),
        "Microsoft",
        "Windows",
        "Fonts",
    )
    for extra_dir in [font_dir, user_font_dir]:
        if os.path.isdir(extra_dir):
            for name in os.listdir(extra_dir):
                lower = name.lower()
                if lower.endswith((".ttf", ".otf", ".ttc", ".otc")):
                    path = os.path.join(extra_dir, name)
                    if os.path.isfile(path):
                        results.append(path)
    dedup = []
    seen = set()
    for path in results:
        key = os.path.normcase(os.path.abspath(path))
        if key not in seen:
            seen.add(key)
            dedup.append(path)
    return dedup


def get_name(record_map: dict[int, str], *ids: int) -> str:
    for name_id in ids:
        value = record_map.get(name_id, "").strip()
        if value:
            return value
    return ""


def record_map_from_font(font: TTFont) -> dict[int, str]:
    names: dict[int, str] = {}
    for record in font["name"].names:
        try:
            value = record.toUnicode().strip()
        except Exception:
            continue
        if value and record.nameID not in names:
            names[record.nameID] = value
    return names


def iter_font_name_rows(path: str) -> list[tuple[str, str, str]]:
    rows: list[tuple[str, str, str]] = []
    lower = path.lower()
    try:
        if lower.endswith((".ttc", ".otc")):
            collection = TTCollection(path)
            fonts = collection.fonts
        else:
            fonts = [TTFont(path, lazy=True)]
    except Exception:
        return rows

    for font in fonts:
        try:
            names = record_map_from_font(font)
            family = get_name(names, 16, 21, 1)
            fullname = get_name(names, 18, 4)
            postscript = get_name(names, 6)
            if family or fullname or postscript:
                rows.append((family, fullname, postscript))
        finally:
            try:
                font.close()
            except Exception:
                pass
    return rows


def main() -> int:
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--format", default="%{family}\t%{fullname}\t%{postscriptname}\n")
    args, _ = parser.parse_known_args()

    template = args.format.encode("utf-8").decode("unicode_escape")
    for path in registry_font_paths():
        for family, fullname, postscript in iter_font_name_rows(path):
            line = template
            line = line.replace("%{family}", family)
            line = line.replace("%{fullname}", fullname)
            line = line.replace("%{postscriptname}", postscript)
            sys.stdout.write(line)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
