#!/usr/bin/env python3
"""修复 GitHub Desktop 在 Windows 下出现的“can't find 7-Zip ...”配置错误。

该错误常见来源：
1) Git 配置中的 editor/difftool/mergetool 指向了无效路径。
2) GitHub Desktop 自身 settings.json 中仍保存了坏掉的 external editor/shell 路径。
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

SCOPES = ("--local", "--global", "--system")
PATTERN = "7-Zip"


@dataclass
class ConfigEntry:
    scope: str
    key: str
    value: str


def run_git(args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        capture_output=True,
        text=True,
        check=False,
    )


def list_entries(scope: str) -> list[ConfigEntry]:
    proc = run_git(["config", scope, "--list"])
    if proc.returncode != 0:
        return []

    out: list[ConfigEntry] = []
    for line in proc.stdout.splitlines():
        if "=" not in line:
            continue
        key, value = line.split("=", 1)
        if PATTERN.lower() in value.lower():
            out.append(ConfigEntry(scope=scope, key=key.strip(), value=value.strip()))
    return out


def unset_key(scope: str, key: str) -> bool:
    proc = run_git(["config", scope, "--unset-all", key])
    return proc.returncode == 0


def summarize(entries: Iterable[ConfigEntry]) -> str:
    lines = ["检测到以下疑似异常 Git 配置："]
    for entry in entries:
        lines.append(f"- {entry.scope} {entry.key} = {entry.value}")
    return "\n".join(lines)


def guess_desktop_settings_path() -> Path | None:
    appdata = os.environ.get("APPDATA")
    if appdata:
        p = Path(appdata) / "GitHub Desktop" / "settings.json"
        if p.exists():
            return p

    home = Path.home()
    candidates = [
        home / "AppData" / "Roaming" / "GitHub Desktop" / "settings.json",
        home / ".config" / "GitHub Desktop" / "settings.json",
    ]
    for p in candidates:
        if p.exists():
            return p
    return None


def scrub_7zip_strings(node: Any, breadcrumb: str = "$") -> tuple[Any, list[str], bool]:
    """递归清理 JSON 中包含 7-Zip 的字符串。返回(新对象, 命中路径, 是否变更)。"""
    hits: list[str] = []
    changed = False

    if isinstance(node, dict):
        out: dict[str, Any] = {}
        for key, value in node.items():
            new_value, sub_hits, sub_changed = scrub_7zip_strings(value, f"{breadcrumb}.{key}")
            hits.extend(sub_hits)
            changed = changed or sub_changed
            if sub_changed and isinstance(value, str) and PATTERN.lower() in value.lower():
                continue
            out[key] = new_value
        return out, hits, changed

    if isinstance(node, list):
        out_list: list[Any] = []
        for idx, value in enumerate(node):
            new_value, sub_hits, sub_changed = scrub_7zip_strings(value, f"{breadcrumb}[{idx}]")
            hits.extend(sub_hits)
            changed = changed or sub_changed
            if sub_changed and isinstance(value, str) and PATTERN.lower() in value.lower():
                continue
            out_list.append(new_value)
        return out_list, hits, changed

    if isinstance(node, str) and PATTERN.lower() in node.lower():
        hits.append(breadcrumb)
        return None, hits, True

    return node, hits, False


def clean_desktop_settings(path: Path, dry_run: bool) -> bool:
    raw = path.read_text(encoding="utf-8")
    data = json.loads(raw)
    cleaned, hits, changed = scrub_7zip_strings(data)

    if not changed:
        print(f"GitHub Desktop settings 未发现包含 '{PATTERN}' 的字段：{path}")
        return True

    print(f"检测到 GitHub Desktop settings 异常字段（{path}）：")
    for h in hits:
        print(f"- {h}")

    if dry_run:
        print("当前为 --dry-run，仅显示，不写回 settings.json")
        return True

    backup = path.with_suffix(path.suffix + ".bak")
    shutil.copy2(path, backup)
    path.write_text(json.dumps(cleaned, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"已写回清理后的 settings.json，备份文件：{backup}")
    return True


def main() -> int:
    dry_run = "--dry-run" in sys.argv

    # 1) 清理 Git config
    found: list[ConfigEntry] = []
    for scope in SCOPES:
        found.extend(list_entries(scope))

    if not found:
        print("未发现包含 '7-Zip' 的 Git 配置项。")
    else:
        print(summarize(found))
        if dry_run:
            print("\n当前为 --dry-run，仅显示，不改动 Git 配置。")
        else:
            for entry in found:
                if unset_key(entry.scope, entry.key):
                    print(f"已清理: {entry.scope} {entry.key}")
                else:
                    print(f"清理失败: {entry.scope} {entry.key}（可能需要管理员权限）")

    # 2) 清理 GitHub Desktop settings
    settings = guess_desktop_settings_path()
    if settings is None:
        print("未找到 GitHub Desktop settings.json（如果你是 Windows，请确认已安装并启动过 GitHub Desktop）。")
    else:
        clean_desktop_settings(settings, dry_run=dry_run)

    print("\n处理完成。建议重启 GitHub Desktop 后再次克隆。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
