#!/usr/bin/env python3
"""生成可复用的“手绘风”配色，并导出为 Origin 可读文本与预览图。"""

from __future__ import annotations

from pathlib import Path

PALETTE = [
    ("Rose", "#E67E80"),
    ("Honey", "#F7BF69"),
    ("Sage", "#8DC792"),
    ("ChalkBlue", "#7BAEE4"),
    ("Lavender", "#B49EDB"),
    ("Lake", "#71C4C9"),
    ("Apricot", "#F4A381"),
    ("Graphite", "#BCBCBC"),
]


def hex_to_rgb(hex_color: str) -> tuple[int, int, int]:
    hex_color = hex_color.strip().lstrip("#")
    if len(hex_color) != 6:
        raise ValueError(f"Invalid hex color: {hex_color}")
    return tuple(int(hex_color[i : i + 2], 16) for i in (0, 2, 4))


def export_origin_palette(path: Path) -> None:
    lines = ["# Hand-drawn palette for Origin bar charts", "# Name\tR\tG\tB"]
    for name, hex_color in PALETTE:
        r, g, b = hex_to_rgb(hex_color)
        lines.append(f"{name}\t{r}\t{g}\t{b}")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def export_markdown_preview(path: Path) -> None:
    lines = ["# 手绘风配色预览", ""]
    for name, hex_color in PALETTE:
        lines.append(f"- `{name}`: `{hex_color}`")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    out_palette = root / "origin" / "handdrawn_palette.txt"
    out_preview = root / "docs" / "handdrawn_palette.md"

    out_palette.parent.mkdir(parents=True, exist_ok=True)
    out_preview.parent.mkdir(parents=True, exist_ok=True)

    export_origin_palette(out_palette)
    export_markdown_preview(out_preview)
    print(f"Wrote: {out_palette}")
    print(f"Wrote: {out_preview}")


if __name__ == "__main__":
    main()
