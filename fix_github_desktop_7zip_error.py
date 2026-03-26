#!/usr/bin/env python3
"""Root-level launcher for scripts/fix_github_desktop_7zip_error.py.

方便用户在仓库根目录直接执行：
    python fix_github_desktop_7zip_error.py --dry-run
"""

from __future__ import annotations

import runpy
from pathlib import Path


def main() -> None:
    target = Path(__file__).resolve().parent / "scripts" / "fix_github_desktop_7zip_error.py"
    if not target.exists():
        raise SystemExit(
            "未找到 scripts/fix_github_desktop_7zip_error.py。请先执行 `git pull`，或确认当前目录是仓库根目录。"
        )
    runpy.run_path(str(target), run_name="__main__")


if __name__ == "__main__":
    main()
