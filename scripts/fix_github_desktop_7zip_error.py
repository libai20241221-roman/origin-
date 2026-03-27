#!/usr/bin/env python3
"""修复 GitHub Desktop 在 Windows 下出现的“can't find 7-Zip ...”配置错误。

支持两种模式：
1) 普通模式（默认）：清理 Git config + 清理 settings.json 中包含 7-Zip 的字段。
2) 强制重置模式（--hard-reset-desktop）：备份后重置 GitHub Desktop 用户配置目录，
   用于“最新版仍反复弹窗”的情况。
"""

from __future__ import annotations

import argparse
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


def guess_desktop_base_dir() -> Path | None:
    appdata = os.environ.get("APPDATA")
    if appdata:
        p = Path(appdata) / "GitHub Desktop"
        if p.exists():
            return p

    home = Path.home()
    candidate = home / "AppData" / "Roaming" / "GitHub Desktop"
    if candidate.exists():
        return candidate
    return None


def scrub_7zip_strings(node: Any, breadcrumb: str = "$") -> tuple[Any, list[str], bool]:
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


def clean_desktop_settings(base_dir: Path, dry_run: bool) -> None:
    settings = base_dir / "settings.json"
    if not settings.exists():
        print(f"未找到 settings.json：{settings}")
        return

    data = json.loads(settings.read_text(encoding="utf-8"))
    cleaned, hits, changed = scrub_7zip_strings(data)

    if not changed:
        print(f"settings.json 未发现包含 '{PATTERN}' 的字段。")
        return

    print("检测到 settings.json 异常字段：")
    for h in hits:
        print(f"- {h}")

    if dry_run:
        print("当前为 --dry-run，仅显示，不写回 settings.json")
        return

    backup = settings.with_suffix(settings.suffix + ".bak")
    shutil.copy2(settings, backup)
    settings.write_text(json.dumps(cleaned, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"已写回清理后的 settings.json，备份：{backup}")


def hard_reset_desktop(base_dir: Path, dry_run: bool) -> None:
    targets = [
        base_dir / "settings.json",
        base_dir / "Local Storage",
        base_dir / "Session Storage",
    ]
    backup_root = base_dir / "backup_before_reset"

    print("将重置以下 GitHub Desktop 用户配置（会先备份）：")
    for t in targets:
        print(f"- {t}")

    if dry_run:
        print("当前为 --dry-run，仅显示，不执行重置。")
        return

    backup_root.mkdir(parents=True, exist_ok=True)
    for target in targets:
        if not target.exists():
            continue
        dst = backup_root / target.name
        if dst.exists():
            if dst.is_dir():
                shutil.rmtree(dst)
            else:
                dst.unlink()
        shutil.move(str(target), str(dst))
        print(f"已备份并移除：{target} -> {dst}")

    print("GitHub Desktop 配置重置完成。请重启 GitHub Desktop 并重新设置 Integrations。")


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true", help="只检测不修改")
    parser.add_argument(
        "--hard-reset-desktop",
        action="store_true",
        help="备份并重置 GitHub Desktop 用户配置（用于反复弹窗）",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv if argv is not None else sys.argv[1:])

    # 1) 清理 Git config
    found: list[ConfigEntry] = []
    for scope in SCOPES:
        found.extend(list_entries(scope))

    if not found:
        print("未发现包含 '7-Zip' 的 Git 配置项。")
    else:
        print(summarize(found))
        if args.dry_run:
            print("\n当前为 --dry-run，仅显示，不改动 Git 配置。")
        else:
            for entry in found:
                if unset_key(entry.scope, entry.key):
                    print(f"已清理: {entry.scope} {entry.key}")
                else:
                    print(f"清理失败: {entry.scope} {entry.key}（可能需要管理员权限）")

    # 2) 处理 GitHub Desktop 配置
    base_dir = guess_desktop_base_dir()
    if base_dir is None:
        print("未找到 GitHub Desktop 配置目录（请先启动过 GitHub Desktop）。")
    else:
        print(f"检测到 GitHub Desktop 配置目录：{base_dir}")
        if args.hard_reset_desktop:
            hard_reset_desktop(base_dir, dry_run=args.dry_run)
        else:
            clean_desktop_settings(base_dir, dry_run=args.dry_run)

    print("\n处理完成。建议重启 GitHub Desktop 后再次导入/克隆。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
